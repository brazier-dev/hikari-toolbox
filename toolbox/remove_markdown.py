import re
import typing as t
from enum import IntFlag

__all__: t.Sequence[str] = (
    "remove_markdown",
    "remove_strikethrough",
    "remove_code_block",
    "remove_multi_code_block",
    "remove_bold",
    "remove_underline",
    "remove_italic_underscore",
    "remove_italic_asterisk",
    "remove_spoiler",
    "remove_quote",
    "remove_multi_quote",
)


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


def remove_markdown(content: str) -> str:
    """Removes the markdown formatting from Discord messages.

    Parameters
    ----------
    content : str
        The `str` object, which needs their content cleaned from Discord's markdown formatting.

    Returns
    -------
    str
        The cleaned string without markdown formatting.
    """
    if content is None:
        return "Message is empty"


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
