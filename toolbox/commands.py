import typing as t

import hikari

__all__: t.Sequence[str] = ["as_command_choices"]

ChoiceTypes = t.Union[str, int, float]


def _dict_to_command_choices(choices: t.Dict[str, ChoiceTypes]) -> t.Sequence[hikari.CommandChoice]:
    return tuple(hikari.CommandChoice(name=k, value=v) for k, v in choices.items())


def _list_to_command_choices(
    choices: t.Union[t.Sequence[ChoiceTypes], t.Sequence[t.Sequence[ChoiceTypes]]],
) -> t.Sequence[hikari.CommandChoice]:
    if isinstance(choices[0], list):
        return tuple(
            hikari.CommandChoice(name=str(name), value=value)
            for name, value in t.cast(t.Sequence[t.Sequence[ChoiceTypes]], choices)
        )
    else:
        return tuple(
            hikari.CommandChoice(name=str(item), value=item) for item in t.cast(t.Sequence[ChoiceTypes], choices)
        )


@t.overload
def as_command_choices(choices: t.Sequence[ChoiceTypes]) -> t.Sequence[hikari.CommandChoice]:
    ...


@t.overload
def as_command_choices(choices: t.Sequence[t.Sequence[ChoiceTypes]]) -> t.Sequence[hikari.CommandChoice]:
    ...


@t.overload
def as_command_choices(choices: t.Dict[str, ChoiceTypes]) -> t.Sequence[hikari.CommandChoice]:
    ...


@t.overload
def as_command_choices(*args: ChoiceTypes) -> t.Sequence[hikari.CommandChoice]:
    ...


@t.overload
def as_command_choices(*args: t.Sequence[ChoiceTypes]) -> t.Sequence[hikari.CommandChoice]:
    ...


@t.overload
def as_command_choices(**kwargs: ChoiceTypes) -> t.Sequence[hikari.CommandChoice]:
    ...


def as_command_choices(*args: t.Any, **kwargs: t.Any) -> t.Sequence[hikari.CommandChoice]:
    """Convert the arguments to `typing.Sequence[hikari.CommandChoice]`.

    Parameters
    ----------
    choices : typing.Sequence[typing.Union[str, int, float]] or typing.Sequence[typing.Sequence[typing.Union[str, int, float]]] or dict[str, typing.Union[str, int, float]]
        A sequence or dict to use to generate the `typing.Sequence[hikari.CommandChoice]`.

        .. code-block:: python

            # Returns `(CommandChoice(name='a', value='a'), CommandChoice(name='b', value='b'), CommandChoice(name='c', value='c'))`
            toolbox.as_command_choices(["a", "b", "c"])

            # Returns `(CommandChoice(name='a', value='e'), CommandChoice(name='b', value='f'), CommandChoice(name='c', value='g'))`
            toolbox.as_command_choices({"a": "e", "b": "f", "c": "g"})
            toolbox.as_command_choices([["a", "d"], ["b", "e"], ["c", "f"]])

    *args : typing.Union[str, int, float] or typing.Sequence[typing.Union[str, int, float]], optional
        The parameters to make the `typing.Sequence[CommandChoice]` with with.

        *args can be provided in any of the following ways:

        .. code-block:: python

            # Returns `(CommandChoice(name='a', value='a'), CommandChoice(name='b', value='b'), CommandChoice(name='c', value='c'))`
            toolbox.as_command_choices("a", "b", "c")

            # Returns `(CommandChoice(name='a', value='e'), CommandChoice(name='b', value='f'), CommandChoice(name='c', value='g'))`
            toolbox.as_command_choices(["a", "e"], ["b", "f"], ["c", "g"])

    **kwargs : str, optional
        If provided, use kwargs as the (name, value) for each `hikari.Commandchoice`.

        .. code-block:: python

            # Returns `(CommandChoice(name='a', value='e'), CommandChoice(name='b', value='f'), CommandChoice(name='c', value='g'))`
            toolbox.as_command_choices(a="e", b="f", c="g")

    Returns
    -------
    typing.Sequence[hikari.CommandChoice]
        The generated `hikari.CommandChoice` objects.

    """
    if kwargs:
        return _dict_to_command_choices(kwargs)

    if len(args) != 1:
        return _list_to_command_choices(args)

    (choices,) = args

    if isinstance(choices, dict):
        return _dict_to_command_choices(choices)
    return _list_to_command_choices(choices)


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
