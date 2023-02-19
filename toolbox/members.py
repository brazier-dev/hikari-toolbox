from __future__ import annotations

import typing as t

import hikari

from .errors import CacheFailureError
from .roles import sort_roles

__all__: t.Sequence[str] = ("get_member_color", "is_above", "get_possessive", "calculate_permissions", "can_moderate")


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

    return (
        member1_top_role.position > member2_top_role.position
        if member1_top_role.position != member2_top_role.position
        else member1_top_role.id < member2_top_role.id
    )


def get_possessive(user: hikari.User) -> str:
    """Returns the possessive noun of a user or a member.

    If a `Member` is passed, the display name is used to form the
    possessive noun when possible. In all other situations, the username
    is used instead.

    Parameters
    ----------
    user : User
        The user or member to get the possessive noun of.

    Returns
    -------
    str
        The possessive noun of the user or member.
    """
    name = getattr(user, "display_name", user.username)
    return f"{name}'{'s' if not name.endswith('s') else ''}"


def calculate_permissions(
    member: hikari.Member, channel: t.Optional[hikari.PermissibleGuildChannel] = None
) -> hikari.Permissions:
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

    if overwrite_everyone := channel.permission_overwrites.get(channel.guild_id):
        permissions &= ~overwrite_everyone.deny
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

    mod_perms = calculate_permissions(moderator)

    if mod_perms & hikari.Permissions.ADMINISTRATOR:
        return True

    return bool(mod_perms & permissions)


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
