"""This module adds the table handler."""

from __future__ import annotations

from typing import TYPE_CHECKING

from ropt.plugins.plan.base import PlanStep

if TYPE_CHECKING:
    from everest.config import EverestConfig


class EverestConfigStep(PlanStep):
    def run(self, *, everest_config: EverestConfig) -> None:
        self.plan.add_handler("everest_table/table", everest_config=everest_config)
