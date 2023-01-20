from __future__ import annotations

import typing as t

import hikari
import functools

__all__: t.Sequence[str] = ["consume_event"]

if t.TYPE_CHECKING:
    P = t.ParamSpec("P")
    T = t.TypeVar("T")


def consume_event(callback: t.Callable[P, T]) -> t.Callable[t.Concatenate[hikari.Event, P], T]:
    """
    Consume the first argument of an event callback.

    .. code-block:: python

        import hikari
        import toolbox

        @toolbox.consume_event
        async def on_started():
            ...

        bot = hikari.GatewayBot("TOKEN")
        bot.subscribe(hikari.StartingEvent, on_started)
        bot.run()
    """

    @functools.wraps(callback)
    async def inner(_: hikari.Event, *args: P.args, **kwargs: P.kwargs) -> T:
        return await callback(*args, **kwargs)

    return inner
