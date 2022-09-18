from __future__ import annotations

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
