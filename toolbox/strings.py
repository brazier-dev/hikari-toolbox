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
    "remove_strikethrough",
    "remove_code_blocks",
    "remove_multi_code_blocks",
    "remove_bold",
    "remove_underlines",
    "remove_underscore_italics",
    "remove_asterisk_italics",
    "remove_spoilers",
    "remove_quotes",
    "remove_multi_quotes",
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

STRIKETHROUGH_REGEX = re.compile(r"~~([\S\s]*?)~~")
ITALIC_UNDERSCORE_REGEX = re.compile(r"_([^_]+)_")
ITALIC_ASTERISK_REGEX = re.compile(r"\*([^*]+)\*")
BOLD_REGEX = re.compile(r"\*{2}([\s\S]*?)\*{2}")
UNDERLINE_REGEX = re.compile(r"__([\s\S]*?)__")
SPOILER_REGEX = re.compile(r"\|{2}([\s\S]+?)\|{2}")
CODE_BLOCK_REGEX = re.compile(r"`([^`]+)`")
MULTI_CODE_BLOCK_REGEX = re.compile(r"`{3}([\S\s]*?)`{3}")
QUOTE_REGEX = re.compile(r"\s*\> (.*)", re.DOTALL)
MULTI_QUOTE_REGEX = re.compile(r"\s*\>>> (.*)", re.DOTALL)


class MarkdownFormat(IntFlag):
    NONE = 0
    STRIKETHROUGH = 1
    ITALIC = 2
    BOLD = 4
    UNDERLINE = 8
    CODE_BLOCK = 16
    MULTI_CODE_BLOCK = 32
    QUOTE = 64
    MULTI_QUOTE = 128
    SPOILER = 256
    ALL = STRIKETHROUGH | ITALIC | BOLD | UNDERLINE | CODE_BLOCK | MULTI_CODE_BLOCK | QUOTE | MULTI_QUOTE | SPOILER


def remove_markdown(content: str, 
formats: MarkdownFormat = MarkdownFormat.ALL
) -> str:
    """Removes the markdown formatting from Discord messages.

    Parameters
    ----------
    content : str
        The `str` object, which needs their content cleaned from Discord's markdown formatting.
    formats : MarkdownFormat
        The `IntFlag` of the kind of formatting that needs to be removed. Default is ALL.

    Returns
    -------
    str
        The cleaned string without markdown formatting.
    """
    if content is None:
        return "Message is empty"
    if (formats & MarkdownFormat.ALL):
        content = remove_spoilers(content)
        content = remove_multi_quotes(content)
        content = remove_quotes(content)
        content = remove_multi_code_blocks(content)
        content = remove_code_blocks(content)
        content = remove_underlines(content)
        content = remove_bold(content)
        content = remove_asterisk_italics(content)
        content = remove_underscore_italics(content)
        content = remove_strikethrough(content)
        return content


def remove_strikethrough(content: str) -> str:
    """Removes the strikethrough formatting from Discord messages.

    Parameters
    ----------
    content : str
        The `str` object to be cleaned from strikethrough.

    Returns
    -------
    str
        The cleaned string without strikethrough formatting.
    """
    matches = re.findall(STRIKETHROUGH_REGEX, content)
    if not matches:
        return content
    cleaned = re.sub(f"~~{matches[0]}~~", matches[0], content)
    for match in matches:
        cleaned = re.sub(f"~~{match}~~", match, cleaned)
    return cleaned


def remove_code_blocks(content: str) -> str:
    """Removes the code block formatting from Discord messages.

    Parameters
    ----------
    content : str
        The `str` object to be cleaned from code block formatting.

    Returns
    -------
    str
        The cleaned string without code block formatting.
    """
    matches = re.findall(CODE_BLOCK_REGEX, content)
    if not matches:
        return content
    cleaned = re.sub(f"`{matches[0]}`", matches[0], content)
    for match in matches:
        cleaned = re.sub(f"`{match}`", match, cleaned)
    return cleaned


def remove_multi_code_blocks(content: str) -> str:
    """Removes the multiline codeblock formatting from Discord messages.

    Parameters
    ----------
    content : str
        The `str` object to be cleaned from multiline codeblock formatting.

    Returns
    -------
    str
        The cleaned string without multiline codeblock formatting.
    """

    matches = re.findall(MULTI_CODE_BLOCK_REGEX, content)
    if not matches:
        return content
    cleaned = re.sub(f"```{matches[0]}```", matches[0], content)
    for match in matches:
        cleaned = re.sub(f"```{match}```", match, cleaned)
    return cleaned


def remove_bold(content: str) -> str:
    """Removes the bold formatting from Discord messages.

    Parameters
    ----------
    content : str
        The `str` object to be cleaned from bold formatting.

    Returns
    -------
    str
        The cleaned string without bold formatting.
    """
    matches = re.findall(BOLD_REGEX, content)
    if not matches:
        return content
    cleaned = re.sub(f"\*\*{matches[0]}\*\*", matches[0], content)
    for match in matches:
        cleaned = re.sub(f"\*\*{match}\*\*", match, cleaned)
    return cleaned


def remove_underlines(content: str) -> str:
    """Removes the underlining from Discord messages.

    Parameters
    ----------
    content : str
        The `str` object to be cleaned from underlining.

    Returns
    -------
    str
        The cleaned string without underlining.
    """
    matches = re.findall(UNDERLINE_REGEX, content)
    if not matches:
        return content
    cleaned = re.sub(f"__{matches[0]}__", matches[0], content)
    for match in matches:
        cleaned = re.sub(f"__{match}__", match, cleaned)
    return cleaned


def remove_underscore_italics(content: str) -> str:
    """Removes the italic formatting from Discord messages caused by single underscores.

    Parameters
    ----------
    content : str
        The `str` object to be cleaned from italic formatting.

    Returns
    -------
    str
        The cleaned string without italic formatting.
    """
    matches = re.findall(ITALIC_UNDERSCORE_REGEX, content)
    if not matches:
        return content
    cleaned = re.sub(f"_{matches[0]}_", matches[0], content)
    for match in matches:
        cleaned = re.sub(f"_{match}_", match, cleaned)
    return cleaned


def remove_asterisk_italics(content: str) -> str:
    """Removes the italic formatting from Discord messages caused by single asterisks.

    Parameters
    ----------
    content : str
        The `str` object to be cleaned from italic formatting.

    Returns
    -------
    str
        The cleaned string without italic formatting.
    """
    matches = re.findall(ITALIC_ASTERISK_REGEX, content)
    if not matches:
        return content
    cleaned = re.sub(f"\*{matches[0]}\*", matches[0], content)
    for match in matches:
        cleaned = re.sub(f"\*{match}\*", match, cleaned)
    return cleaned


def remove_spoilers(content: str) -> str:
    """Removes the spoiler from Discord messages.

    Parameters
    ----------
    content : str
        The `str` object to be cleaned from spoilers.

    Returns
    -------
    str
        The cleaned string without spoilers.
    """
    matches = re.findall(SPOILER_REGEX, content)
    if not matches:
        return content
    cleaned = re.sub(f"\|\|{matches[0]}\|\|", matches[0], content)
    for match in matches:
        cleaned = re.sub(f"\|\|{match}\|\|", match, cleaned)
    return cleaned


def remove_quotes(content: str) -> str:
    """Removes the quote formatting from Discord messages.

    Parameters
    ----------
    content : str
        The `str` object to be cleaned from quote formatting.

    Returns
    -------
    str
        The cleaned string without quote formatting.
    """
    matches = re.findall(QUOTE_REGEX, content)
    if not matches:
        return content
    cleaned = re.sub(f"> {matches[0]}", matches[0], content)
    for match in matches:
        cleaned = re.sub(f"> {match}", match, cleaned)
    return cleaned


def remove_multi_quotes(content: str) -> str:
    """Removes the multiline quote formatting from Discord messages.

    Parameters
    ----------
    content : str
        The `str` object to be cleaned from multiline quote formatting.

    Returns
    -------
    str
        The cleaned string without multiline quote formatting.
    """
    matches = re.findall(MULTI_QUOTE_REGEX, content)
    if not matches:
        return content
    cleaned = re.sub(f">>> {matches[0]}", matches[0], content)
    for match in matches:
        cleaned = re.sub(f">>> {match}", match, cleaned)
    return cleaned
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
