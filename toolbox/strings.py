import datetime
import re
import typing as t
from enum import Enum, IntFlag

__all__: t.Sequence[str] = (
    "format_dt",
    "TimestampStyle",
    "utcnow",
    "is_url",
    "is_invite",
    "remove_markdown",
    "MarkdownFormat",
)


LINK_REGEX = re.compile(
    r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()!@:%_\+.~#?&\/\/=]*)"
)
INVITE_REGEX = re.compile(r"(?:https?://)?discord(?:app)?\.(?:com/invite|gg)/[a-zA-Z0-9]+/?")


class TimestampStyle(str, Enum):
    """Enum of Discord timestamp styles"""

    RELATIVE = "R"
    """Ex: 3 minutes ago"""
    SHORT_TIME = "t"
    """Ex: 3:50 PM"""
    LONG_TIME = "T"
    """Ex: 3:50:25 PM"""
    SHORT_DATE = "d"
    """Ex: 2/16/23"""
    LONG_DATE = "D"
    """Ex: February 16, 2023"""
    LONG_DATE_SHORT_TIME = "f"
    """Ex: February 16, 2023 at 3:50 PM"""
    LONG_DATE_WITH_DOW_SHORT_TIME = "F"
    """Ex: Thursday, February 16, 2023, at 3:50 PM"""

    # Method to replicate Python 3.11's StrEnum
    def __str__(self) -> str:
        return self.value


class MarkdownFormat(IntFlag):
    """An Enum to flag strings with the types of formatting that should be removed."""

    NONE = 0
    """Refers to no formatting."""

    STRIKETHROUGH = 1 << 0
    """Used to remove strikethroughs caused by 2 tildes."""

    ITALIC_UNDERSCORE = 1 << 1
    """Used to remove italic caused by underscores."""

    ITALIC_ASTERISK = 1 << 2
    """Used to remove italic caused by asterisks."""

    BOLD = 1 << 3
    """Used to remove bold caused by 2 asterisks."""

    UNDERLINE = 1 << 4
    """Used to remove underlining caused by 2 underscores."""

    CODE_BLOCK = 1 << 5
    """Used to remove code blocks caused by backticks."""

    MULTI_CODE_BLOCK = 1 << 6
    """Used to remove multiline code blocks caused by 3 backticks."""

    QUOTE = 1 << 7
    """Used to remove quotes caused by a bigger than at the start of the line followed by a whitespace character."""

    MULTI_QUOTE = 1 << 8
    """Used to remove multiline quotes caused by 3 bigger thans at the start of the line followed by a whitespace character."""

    SPOILER = 1 << 9
    """Used to remove spoilers caused by 2 pipes."""

    ALL = (
        STRIKETHROUGH
        | ITALIC_UNDERSCORE
        | ITALIC_ASTERISK
        | BOLD
        | UNDERLINE
        | CODE_BLOCK
        | MULTI_CODE_BLOCK
        | QUOTE
        | MULTI_QUOTE
        | SPOILER
    )
    """Used to remove all possible formatting."""


FORMAT_DICT = {
    # First value is the regex pattern of the affiliated enum flag, the match includes the formatting that causes it.
    # Second value is the amount of characters that will be sliced off the match.
    MarkdownFormat.MULTI_CODE_BLOCK: (re.compile(r"(`{3}[^`]+`{3})"), 3),
    MarkdownFormat.CODE_BLOCK: (re.compile(r"(`[^`]+`)"), 1),
    MarkdownFormat.MULTI_QUOTE: (re.compile(r"\s*>{3} ([\s\S]+)"), 0),
    MarkdownFormat.QUOTE: (re.compile(r"\s*> ([\s\S]+)"), 0),
    MarkdownFormat.BOLD: (re.compile(r"(\*{2}[^*]+\*{2})"), 2),
    MarkdownFormat.UNDERLINE: (re.compile(r"(__[^_]+__)"), 2),
    MarkdownFormat.STRIKETHROUGH: (re.compile(r"(~~[^~]+~~)"), 2),
    MarkdownFormat.ITALIC_UNDERSCORE: (re.compile(r"(_[^_]+_)"), 1),
    MarkdownFormat.ITALIC_ASTERISK: (re.compile(r"(\*[^*]+\*)"), 1),
    MarkdownFormat.SPOILER: (re.compile(r"(\|{2}[^|]+\|{2})"), 2),
}


def format_dt(time: datetime.datetime, style: t.Optional[TimestampStyle] = None) -> str:
    """
    Convert a datetime into a Discord timestamp.
    For styling see this link: https://discord.com/developers/docs/reference#message-formatting-timestamp-styles

    Parameters
    ----------
    time : datetime.datetime
        The datetime to convert.
    style : TimestampStyle, optional
        The style to use for the timestamp, by default None.

    Returns
    -------
    str
        The formatted timestamp.
    """

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


def remove_markdown(content: str, formats: MarkdownFormat = MarkdownFormat.ALL) -> str:
    """
    Removes the markdown formatting from Discord messages.

    Parameters
    ----------
    content : str
        The `str` object, which needs their content cleaned from Discord's markdown formatting.
    formats : MarkdownFormat
        The `IntFlag` of the formatting that needs to be removed.
        Default is `MarkdownFormat.ALL`.
        Multiple can be supplied by using bitwise OR.
        Matches for `MarkdownFormat.MULTI_CODE_BLOCK` and `MarkdownFormat.CODE_BLOCK`
        don't remove other formatting found inside them.

    Returns
    -------
    str
        The cleaned string without markdown formatting.
    """
    code_block_matches = []
    for format, (regex, replace) in FORMAT_DICT.items():
        if formats & format:
            if format & MarkdownFormat.MULTI_CODE_BLOCK or format & MarkdownFormat.CODE_BLOCK:
                code_block_matches += re.findall(regex, content)
            matches = re.findall(regex, content)
            if not code_block_matches:
                for match in matches:
                    if format & MarkdownFormat.MULTI_QUOTE or format & MarkdownFormat.QUOTE:
                        content = _remove_quote(content, format)
                        continue
                    content = content.replace(match, match[replace:-replace], 1)
            else:
                for match in matches:
                    if format & MarkdownFormat.MULTI_CODE_BLOCK or format & MarkdownFormat.CODE_BLOCK:
                        content = content.replace(match, match[replace:-replace], 1)
                        continue
                    else:
                        ignore = False
                        for code_block_match in code_block_matches:
                            if match in code_block_match:
                                ignore = True
                        if not ignore:
                            content = content.replace(match, match[replace:-replace], 1)

    return content


def _remove_quote(content: str, formats: MarkdownFormat) -> str:
    """
    Helper function to remove quote formatting.

    Parameters
    ----------
    content : str
        The `str` object, which needs to be cleaned from quote formatting.
    format : MarkdownFormat
        The type of quote formatting that needs to be removed.

    Returns
    -------
    str
        The cleaned string without quote formatting.
    """
    if formats == MarkdownFormat.MULTI_QUOTE and ">>> " in content:
        content = content.replace(">>> ", "")
    if formats == MarkdownFormat.QUOTE and "> " in content:
        content = content.replace("> ", "")
    return content


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
