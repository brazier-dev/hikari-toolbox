from __future__ import annotations

from unittest import mock

import hikari

import toolbox
from tests import utils


def test_no_roles():
    member = utils.make_member([])

    assert toolbox.get_member_color(member) == hikari.Color(0)


def test_highest_role_color():
    member = utils.make_member(
        [
            utils.make_role(position=2, color=hikari.Color(100)),
            utils.make_role(position=1, color=hikari.Color(200)),
        ]
    )

    assert toolbox.get_member_color(member) == hikari.Color(100)


def test_highest_role_no_color():
    member = utils.make_member(
        [
            utils.make_role(position=3, color=hikari.Color(0)),
            utils.make_role(position=2, color=hikari.Color(100)),
            utils.make_role(position=1, color=hikari.Color(200)),
        ]
    )

    assert toolbox.get_member_color(member) == hikari.Color(100)


def test_sort_roles():
    roles = [
        utils.make_role(position=1),
        utils.make_role(position=3),
        utils.make_role(position=2),
    ]

    roles = toolbox.sort_roles(roles)

    assert roles[0].position == 3
    assert roles[1].position == 2
    assert roles[2].position == 1


def test_user_possessive_no_s():
    user = mock.Mock(["username"])
    user.username = "RickAstley"
    assert toolbox.get_possessive(user) == "RickAstley's"


def test_user_possessive_s():
    user = mock.Mock(["username"])
    user.username = "BigChungus"
    assert toolbox.get_possessive(user) == "BigChungus'"


def test_member_possessive_no_s():
    member = mock.Mock(["username", "display_name"])
    member.username = "RickAstley"
    member.display_name = "NeverGonna"
    assert toolbox.get_possessive(member) == "NeverGonna's"


def test_member_possessive_s():
    member = mock.Mock(["username", "display_name"])
    member.username = "BigChungus"
    member.display_name = "HugeChungus"
    assert toolbox.get_possessive(member) == "HugeChungus'"
