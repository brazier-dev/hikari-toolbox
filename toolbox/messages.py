import re
import typing as t

import hikari

from .errors import EmbedValidationError

__all__: t.Sequence[str] = ("fetch_message_from_link", "validate_embed")

MESSAGE_LINK_REGEX = re.compile(
    r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()!@:%_\+.~#?&\/\/=]*)channels[\/][0-9]{1,}[\/][0-9]{1,}[\/][0-9]{1,}"
)


async def fetch_message_from_link(message_link: str, *, bot: hikari.RESTAware) -> hikari.Message:
    """Parse a message_link string into a message object.

    Parameters
    ----------
    message_link : str
        The message link.
    bot : RESTAware
        The bot object to execute REST calls with.

    Returns
    -------
    hikari.Message
        The message object

    Raises
    ------
    ValueError
        If the message link is invalid.
    """

    if not MESSAGE_LINK_REGEX.fullmatch(message_link):
        raise ValueError(
            "Invalid message link provided, should match the following regex: " + MESSAGE_LINK_REGEX.pattern
        )

    _, channel_id, message_id = message_link.split("/channels/")[1].split("/")

    return await bot.rest.fetch_message(int(channel_id), int(message_id))


def validate_embed(embed: hikari.Embed) -> hikari.Embed:
    """Validate an embed, checking the length of all fields.

    Parameters
    ----------
    embed : hikari.Embed
        The embed to validate.

    Raises
    ------
    EmbedValidationError
        Raised when the embed is invalid.

    Returns
    -------
    hikari.Embed
        The embed that was validated.
    """
    if (length := embed.total_length()) > 6000:
        raise EmbedValidationError(f"Embed total length must be less than 6000 characters, got {length}.")

    if embed.title and (length := len(embed.title)) > 256:
        raise EmbedValidationError(f"Embed title must be less than 256 characters, got {length}.")

    if embed.description and (length := len(embed.description)) > 4096:
        raise EmbedValidationError(f"Embed description must be less than 4096 characters, got {length}.")

    if embed.footer and embed.footer.text and (length := len(embed.footer.text)) > 2048:
        raise EmbedValidationError(f"Embed footer text must be less than 2048 characters, got {length}.")

    if embed.author and embed.author.name and (length := len(embed.author.name)) > 256:
        raise EmbedValidationError(f"Embed author name must be less than 256 characters, got {length}.")

    if embed.fields:
        if (field_count := len(embed.fields)) > 25:
            raise EmbedValidationError(f"Embed must have less than 25 fields, got {field_count}.")

        for i, field in enumerate(embed.fields):
            if (length := len(field.name)) > 256:
                raise EmbedValidationError(
                    f"Embed field {i} ({field.name}): name must be less than 256 characters, got {length}."
                )
            if (length := len(field.value)) > 1024:
                raise EmbedValidationError(
                    f"Embed field {i} ({field.name}): value must be less than 1024 characters, got {length}."
                )

    return embed


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
