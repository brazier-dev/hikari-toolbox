from __future__ import annotations

from unittest import mock

import toolbox


def test_user_possessive_no_s():
    user = mock.Mock(["username"])
    user.username = "RickAstley"
    assert toolbox.get_user_possessive(user) == "RickAstley's"


def test_user_possessive_s():
    user = mock.Mock(["username"])
    user.username = "BigChungus"
    assert toolbox.get_user_possessive(user) == "BigChungus'"


def test_member_possessive_no_s():
    member = mock.Mock(["username", "display_name"])
    member.username = "RickAstley"
    member.display_name = "NeverGonna"
    assert toolbox.get_user_possessive(member) == "NeverGonna's"


def test_member_possessive_s():
    member = mock.Mock(["username", "display_name"])
    member.username = "BigChungus"
    member.display_name = "HugeChungus"
    assert toolbox.get_user_possessive(member) == "HugeChungus'"
