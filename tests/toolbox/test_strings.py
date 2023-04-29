import datetime

import pytest

import toolbox


def test_is_url():
    assert toolbox.is_url("https://somewebsite.com/")
    assert toolbox.is_url("https://somewebsite.com#123")
    assert toolbox.is_url("https://somewebsite.com/page")
    assert toolbox.is_url("https://somewebsite.com?a=2+b=3")


def test_is_not_url():
    assert not toolbox.is_url("not a url")


def test_is_invite_fullmatch():
    assert toolbox.is_invite("https://discord.gg/Jx4cNGG", fullmatch=True)
    assert not toolbox.is_invite("Jx4cNGG", fullmatch=True)


def test_is_invite_partial_match():
    assert toolbox.is_invite("https://discord.gg/Jx4cNGG", fullmatch=False)
    assert toolbox.is_invite("https://discord.gg/Jx4cNGG/RANDOM GARBAGE", fullmatch=False)


def test_no_style():
    time = datetime.datetime.now()
    assert toolbox.format_dt(time) == f"<t:{int(time.timestamp())}>"


def test_has_style():
    time = datetime.datetime.now()
    assert toolbox.format_dt(time, style=toolbox.TimestampStyle.SHORT_TIME) == f"<t:{int(time.timestamp())}:t>"
