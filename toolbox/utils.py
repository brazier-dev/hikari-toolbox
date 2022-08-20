import datetime
import re
import typing as t

import hikari

from .errors import CacheFailureError

__all__: t.Sequence[str] = (
    "format_dt",
    "utcnow",
    "get_member_color",
    "sort_roles",
    "is_above",
    "is_url",
    "is_invite",
    "fetch_message_from_link",
    "calculate_permissions",
    "can_moderate",
)

VALID_TIMESTAMP_STYLES: t.Sequence[str] = ("t", "T", "d", "D", "f", "F", "R")

MESSAGE_LINK_REGEX = re.compile(
    r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()!@:%_\+.~#?&\/\/=]*)channels[\/][0-9]{1,}[\/][0-9]{1,}[\/][0-9]{1,}"
)
LINK_REGEX = re.compile(
    r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()!@:%_\+.~#?&\/\/=]*)"
)
INVITE_REGEX = re.compile(r"(?:https?://)?discord(?:app)?\.(?:com/invite|gg)/[a-zA-Z0-9]+/?")


def format_dt(time: datetime.datetime, style: t.Optional[str] = None) -> str:
    """
    Convert a datetime into a Discord timestamp.
    For styling see this link: https://discord.com/developers/docs/reference#message-formatting-timestamp-styles

    Parameters
    ----------
    time : datetime.datetime
        The datetime to convert.
    style : str, optional
        The style to use for the timestamp, by default None.

    Returns
    -------
    str
        The formatted timestamp.
    """

    if style and style not in VALID_TIMESTAMP_STYLES:
        raise ValueError(f"Invalid style passed. Valid styles: {' '.join(VALID_TIMESTAMP_STYLES)}")

    if style:
        return f"<t:{int(time.timestamp())}:{style}>"

    return f"<t:{int(time.timestamp())}>"


def utcnow() -> datetime.datetime:
    """
    A short-hand function to return a timezone-aware utc datetime.

    Returns
    -------
    datetime.datetime
        The current timezone-aware utc datetime.
    """
    return datetime.datetime.now(datetime.timezone.utc)


def get_member_color(member: hikari.Member) -> hikari.Color:
    """Retrieves the color of a member based on the top colored role.

    Parameters
    ----------
    member : hikari.Member
        The member to get the color of.

    Returns
    -------
    hikari.Color
        The retrieved color object. If no color is found, it will return RGB(0, 0, 0).
    """
    roles = sort_roles(member.get_roles())
    if not roles:
        return hikari.Color(0)

    for role in roles:
        if role.color != hikari.Color.from_rgb(0, 0, 0):
            return role.color

    return hikari.Color(0)


def sort_roles(roles: t.Sequence[hikari.Role], ascending: bool = False) -> t.Sequence[hikari.Role]:
    """Sort a list of roles based on position. By default it is in a descending order.

    Parameters
    ----------
    roles : Sequence[hikari.Role]
        The list of roles to sort.
    ascending : bool, optional
        Whether to sort in ascending order, by default False.

    Returns
    -------
    Sequence[hikari.Role]
        The sorted list of roles.
    """
    return sorted(roles, key=lambda r: r.position, reverse=not ascending)


def is_above(member1: hikari.Member, member2: hikari.Member) -> bool:
    """
    Returns True if member1's top role's position is higher than member2's.

    Parameters
    ----------
    member1 : hikari.Member
        The first member to compare.
    member2 : hikari.Member
        The second member to compare.

    Returns
    -------
    bool
        Whether member1's top role's position is higher than member2's.
    """
    member1_top_role = member1.get_top_role()
    member2_top_role = member2.get_top_role()

    if not member1_top_role or not member2_top_role:
        raise CacheFailureError("Some objects could not be resolved from cache.")

    return member1_top_role.position > member2_top_role.position


def calculate_permissions(member: hikari.Member, channel: t.Optional[hikari.GuildChannel] = None) -> hikari.Permissions:
    """Calculate the permissions of a member.
    If a channel is provided, channel overwrites will be taken into account.

    Parameters
    ----------
    member : hikari.Member
        The member to calculate the permissions of.
    channel : hikari.GuildChannel, optional
        The channel for permission overwrite calculations, by default None.

    Returns
    -------
    hikari.Permissions
        The calculated permissions.

    Raises
    ------
    CacheFailureError
        Some objects could not be resolved from cache to perform the operation.
    """

    guild = member.get_guild()
    if not guild:
        raise CacheFailureError("Guild could not be resolved from cache.")

    if guild.owner_id == member.id:
        return hikari.Permissions.all_permissions()

    guild_roles = guild.get_roles()
    member_roles = list(filter(lambda r: r.id in member.role_ids, guild_roles.values()))
    permissions: hikari.Permissions = guild_roles[guild.id].permissions  # Start with @everyone perms

    for role in member_roles:
        permissions |= role.permissions

    if permissions & hikari.Permissions.ADMINISTRATOR:
        return hikari.Permissions.all_permissions()

    if not channel:  # End of role-based permissions
        return permissions

    overwrite_everyone = channel.permission_overwrites.get(channel.guild_id)
    assert overwrite_everyone is not None
    permissions &= overwrite_everyone.deny
    permissions |= overwrite_everyone.allow

    overwrites = hikari.PermissionOverwrite(  # Collect role overwrites here
        id=hikari.Snowflake(69),
        type=hikari.PermissionOverwriteType.ROLE,
        allow=hikari.Permissions.NONE,
        deny=hikari.Permissions.NONE,
    )

    for role in member_roles:
        if overwrite := channel.permission_overwrites.get(role.id):
            overwrites.deny |= overwrite.deny
            overwrites.allow |= overwrite.allow

    permissions &= ~overwrites.deny
    permissions |= overwrites.allow

    if overwrite_member := channel.permission_overwrites.get(member.id):
        permissions &= ~overwrite_member.deny
        permissions |= overwrite_member.allow

    return permissions


def can_moderate(
    moderator: hikari.Member, member: hikari.Member, permissions: hikari.Permissions = hikari.Permissions.NONE
) -> bool:
    """
    Returns True if "moderator" can execute moderation actions on "member", also checks if "moderator" has "permissions".

    Parameters
    ----------
    moderator : hikari.Member
        The moderator to check.
    member : hikari.Member
        The member to check.
    permissions : hikari.Permissions
        The permissions `moderator` should have.

    Returns
    -------
    bool
        Whether "moderator" can execute moderation actions on "member".

    Raises
    ------
    CacheFailureError
        Some objects could not be resolved from cache to perform the operation.
    """

    if not is_above(moderator, member):
        return False

    guild = member.get_guild()
    if not guild:
        raise CacheFailureError("Guild could not be resolved from cache.")

    if guild.owner_id == member.id:
        return False

    if permissions is hikari.Permissions.NONE:
        return True

    if not (calculate_permissions(moderator) & permissions):
        return False

    return True


def is_url(string: str, *, fullmatch: bool = True) -> bool:
    """
    Returns True if the provided string is a valid http URL, otherwise False.

    Parameters
    ----------
    string : str
        The string to check.
    fullmatch : bool
        Whether to check if the string is a full match, by default True.

    Returns
    -------
    bool
        Whether the string is an URL.
    """

    if fullmatch and LINK_REGEX.fullmatch(string):
        return True
    elif not fullmatch and LINK_REGEX.match(string):
        return True

    return False


def is_invite(string: str, *, fullmatch: bool = True) -> bool:
    """
    Returns True if the provided string is a Discord invite, otherwise False.

    Parameters
    ----------
    string : str
        The string to check.
    fullmatch : bool
        Whether to check if the string is a full match, by default True.

    Returns
    -------
    bool
        Whether the string is a Discord invite.
    """

    if fullmatch and INVITE_REGEX.fullmatch(string):
        return True
    elif not fullmatch and INVITE_REGEX.match(string):
        return True

    return False


async def fetch_message_from_link(message_link: str, *, bot: hikari.RESTAware) -> hikari.Message:
    """Parse a message_link string into a message object.

    Parameters
    ----------
    message_link : str
        The message link.
    bot : RESTAware
        The bot object to execute REST calls with.

    Returns
    -------
    hikari.Message
        The message object

    Raises
    ------
    ValueError
        If the message link is invalid.
    """

    if not MESSAGE_LINK_REGEX.fullmatch(message_link):
        raise ValueError(
            "Invalid message link provided, should match the following regex: " + MESSAGE_LINK_REGEX.pattern
        )

    snowflakes = message_link.split("/channels/")[1].split("/")
    channel_id = hikari.Snowflake(snowflakes[1])
    message_id = hikari.Snowflake(snowflakes[2])

    return await bot.rest.fetch_message(channel_id, message_id)


# MIT License
#
# Copyright (c) 2022-present HyperGH
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
