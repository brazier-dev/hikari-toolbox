import datetime
import re
import typing as t
from enum import IntFlag

__all__: t.Sequence[str] = (
    "format_dt",
    "utcnow",
    "is_url",
    "is_invite",
    "remove_markdown",
    "MarkdownFormat",
)

VALID_TIMESTAMP_STYLES: t.Sequence[str] = ("t", "T", "d", "D", "f", "F", "R")


LINK_REGEX = re.compile(
    r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()!@:%_\+.~#?&\/\/=]*)"
)
INVITE_REGEX = re.compile(r"(?:https?://)?discord(?:app)?\.(?:com/invite|gg)/[a-zA-Z0-9]+/?")


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

    SPOILER = 512
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
    # First value is the regex pattern of the affiliated enum flag, the match is WITHOUT the formatting that causes it.
    # Second value is the string that is being replaced in the originally sent string by the match alone.
    # {0} is a placeholder for the match.
    MarkdownFormat.MULTI_QUOTE: (re.compile(r"\s*\>>> ([\s\S]+?)"), ">>> {0}"),
    MarkdownFormat.QUOTE: (re.compile(r"\s*\> ([\s\S]+?)"), "> {0}"),
    MarkdownFormat.MULTI_CODE_BLOCK: (re.compile(r"`{3}([\S\s]+?)`{3}"), "```{0}```"),
    MarkdownFormat.CODE_BLOCK: (re.compile(r"`([^`]+?)`"), "`{0}`"),
    MarkdownFormat.BOLD: (re.compile(r"\*{2}([\s\S]+?)\*{2}"), "\*\*{0}\*\*"),
    MarkdownFormat.UNDERLINE: (re.compile(r"__([\s\S]+?)__"), "__{0}__"),
    MarkdownFormat.STRIKETHROUGH: (re.compile(r"~~([\S\s]+?)~~"), "~~{0}~~"),
    MarkdownFormat.ITALIC_UNDERSCORE: (re.compile(r"_([^_]+?)_"), "_{0}_"),
    MarkdownFormat.ITALIC_ASTERISK: (re.compile(r"\*([^*]+?)\*"), "\*{0}\*"),
    MarkdownFormat.SPOILER: (re.compile(r"\|{2}([\s\S]+?)\|{2}"), "\|\|{0}\|\|"),
}


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


def remove_markdown(content: str, formats: MarkdownFormat = MarkdownFormat.ALL) -> str:
    """
    Removes the markdown formatting from Discord messages.

    Parameters
    ----------
    content : str
        The `str` object, which needs their content cleaned from Discord's markdown formatting.
    formats : MarkdownFormat
        The `IntFlag` of the formatting that needs to be removed. Default is `MarkdownFormat.ALL`

    Returns
    -------
    str
        The cleaned string without markdown formatting.
    """
    for format, (regex, replace) in FORMAT_DICT.items():
        if formats & format:
            matches = re.findall(regex, content)
            for match in matches:
                content = re.sub(replace.format(match), match, content)
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
