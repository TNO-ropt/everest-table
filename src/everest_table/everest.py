"""This module implements the everest_table plugin."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Final

from ropt.plugins.event_handler.base import EventHandlerPlugin

from ._results_table import EverestDefaultTableHandler

if TYPE_CHECKING:
    from ropt.plugins.event_handler.base import EventHandler


_EVENT_HANDLER_OBJECTS: Final[dict[str, type[EventHandler]]] = {
    "table": EverestDefaultTableHandler,
}


class EverestTableEventHandlerPlugin(EventHandlerPlugin):
    """The everest event handler class."""

    @classmethod
    def create(
        cls,
        name: str,
        **kwargs: dict[str, Any],
    ) -> EventHandler:
        """Create a event event handler.

        # noqa
        """
        _, _, name = name.lower().rpartition("/")
        obj = _EVENT_HANDLER_OBJECTS.get(name)
        if obj is not None:
            return obj(**kwargs)

        msg = f"Unknown event handler object type: {name}"
        raise TypeError(msg)

    @classmethod
    def is_supported(cls, method: str) -> bool:
        """Check if a method is supported.

        # noqa
        """
        return method.lower() in _EVENT_HANDLER_OBJECTS
