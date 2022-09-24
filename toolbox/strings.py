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


class MarkdownFormat(IntFlag):
    NONE = 0
    STRIKETHROUGH = 1
    ITALIC_UNDERSCORE = 2
    ITALIC_ASTERISK = 4
    BOLD = 8
    UNDERLINE = 16
    CODE_BLOCK = 32
    MULTI_CODE_BLOCK = 64
    QUOTE = 128
    MULTI_QUOTE = 256
    SPOILER = 512
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


format_dict = {
    MarkdownFormat.MULTI_QUOTE: [r"\s*\>>> ([\s\S]+?)", ">>> {0}"],
    MarkdownFormat.QUOTE: [r"\s*\> ([\s\S]+?)", "> {0}"],
    MarkdownFormat.MULTI_CODE_BLOCK: [r"`{3}([\S\s]+?)`{3}", "```{0}```"],
    MarkdownFormat.CODE_BLOCK: [r"`([^`]+?)`", "`{0}`"],
    MarkdownFormat.BOLD: [r"\*{2}([\s\S]+?)\*{2}", "\*\*{0}\*\*"],
    MarkdownFormat.UNDERLINE: [r"__([\s\S]+?)__", "__{0}__"],
    MarkdownFormat.STRIKETHROUGH: [r"~~([\S\s]+?)~~", "~~{0}~~"],
    MarkdownFormat.ITALIC_UNDERSCORE: [r"_([^_]+?)_", "_{0}_"],
    MarkdownFormat.ITALIC_ASTERISK: [r"\*([^*]+?)\*", "\*{0}\*"],
    MarkdownFormat.SPOILER: [r"\|{2}([\s\S]+?)\|{2}", "\|\|{0}\|\|"],
}


def remove_markdown(content: str, formats: MarkdownFormat = MarkdownFormat.ALL) -> str:
    """Removes the markdown formatting from Discord messages.

    Parameters
    ----------
    content : str
        The `str` object, which needs their content cleaned from Discord's markdown formatting.
    formats : MarkdownFormat
        The `IntFlag` the of formatting that needs to be removed. Default is ALL.

    Returns
    -------
    str
        The cleaned string without markdown formatting.
    """
    match_list = []
    for format in format_dict:
        if formats & format:
            search = re.compile(format_dict[format][0])
            match_list.append(re.findall(search, content))
    for format in format_dict:
        if formats & format:
            for matches in match_list:
                if not matches:
                    continue
                for match in matches:
                    content = re.sub(format_dict[format][1].format(match), match, content)
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
