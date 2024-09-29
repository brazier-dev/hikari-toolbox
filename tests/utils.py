from __future__ import annotations

import typing

import hikari

__all__: typing.Sequence[str] = (
    "make_role",
    "make_member",
)


def make_role(
    *,
    position: int = 0,
    name: str = "",
    color: hikari.Color = hikari.Color(0),
    permissions: hikari.Permissions = hikari.Permissions.NONE,
) -> hikari.Role:
    return hikari.Role(
        app=None,
        id=None,
        name=name,
        color=color,
        guild_id=None,
        is_hoisted=True,
        icon_hash=None,
        unicode_emoji=None,
        is_managed=False,
        is_mentionable=True,
        permissions=permissions,
        position=position,
        bot_id=None,
        integration_id=False,
        is_premium_subscriber_role=None,
        subscription_listing_id=None,
        is_available_for_purchase=None,
        is_guild_linked_role=None,
    )


GLOBAL_ROLES = {}


def make_member(roles: list[hikari.Role] = None):
    member = hikari.Member(
        guild_id=None,
        is_deaf=None,
        is_mute=None,
        is_pending=None,
        joined_at=None,
        nickname=None,
        premium_since=None,
        raw_communication_disabled_until=None,
        role_ids=[role.id for role in roles],
        user=None,
        guild_avatar_hash=None,
        guild_flags=None,
    )

    GLOBAL_ROLES[id(member)] = roles

    type(member).get_roles = lambda self: GLOBAL_ROLES[id(self)]

    return member
