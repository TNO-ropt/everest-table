"""This module implements the everest_table plugin."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Final

from ropt.plugins.plan.base import EventHandlerPlugin

from ._results_table import EverestDefaultTableHandler

if TYPE_CHECKING:
    from ropt.plan import Plan
    from ropt.plugins.plan.base import EventHandler, PlanComponent


_EVENT_HANDLER_OBJECTS: Final[dict[str, type[EventHandler]]] = {
    "table": EverestDefaultTableHandler,
}


class EverestTableEventHandlerPlugin(EventHandlerPlugin):
    """The everest event handler class."""

    @classmethod
    def create(
        cls,
        name: str,
        plan: Plan,
        tags: set[str] | None = None,
        sources: set[PlanComponent | str] | None = None,
        **kwargs: dict[str, Any],
    ) -> EventHandler:
        """Create a event event handler.

        See the [ropt.plugins.plan.base.PlanPlugin][] abstract base class.

        # noqa
        """
        _, _, name = name.lower().rpartition("/")
        obj = _EVENT_HANDLER_OBJECTS.get(name)
        if obj is not None:
            return obj(plan, tags, sources, **kwargs)

        msg = f"Unknown event handler object type: {name}"
        raise TypeError(msg)

    @classmethod
    def is_supported(cls, method: str) -> bool:
        """Check if a method is supported.

        See the [ropt.plugins.base.Plugin][] abstract base class.

        # noqa
        """
        return method.lower() in _EVENT_HANDLER_OBJECTS
