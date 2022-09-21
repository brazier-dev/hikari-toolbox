import datetime
import re
import typing as t

__all__: t.Sequence[str] = ("format_dt", "utcnow", "is_url", "is_invite")

VALID_TIMESTAMP_STYLES: t.Sequence[str] = ("t", "T", "d", "D", "f", "F", "R")


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
