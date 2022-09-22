import datetime
from unittest import mock

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


@pytest.mark.asyncio
async def test_fetch_message_from_link():
    link = "https://discord.com/channels/574921006817476608/1010666418007719956/1012539497415704636"
    channel_id = 1010666418007719956
    message_id = 1012539497415704636

    bot = mock.Mock()
    bot.rest = mock.Mock()
    bot.rest.fetch_message = mock.AsyncMock()

    await toolbox.fetch_message_from_link(link, bot=bot)
    bot.rest.fetch_message.assert_called_with(channel_id, message_id)


def test_no_style():
    time = datetime.datetime.now()
    assert toolbox.format_dt(time) == f"<t:{int(time.timestamp())}>"


def test_has_style():
    time = datetime.datetime.now()
    assert toolbox.format_dt(time, style="t") == f"<t:{int(time.timestamp())}:t>"


def test_invalid_style():
    with pytest.raises(ValueError):
        toolbox.format_dt(datetime.datetime.now(), "INVALID")