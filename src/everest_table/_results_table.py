from __future__ import annotations

from typing import TYPE_CHECKING, Final, Literal

from ropt.workflow.event_handlers import TableHandler
from tabulate import tabulate

if TYPE_CHECKING:
    from pathlib import Path

    from ropt.events import EnOptEvent


_TABLE_COLUMNS: Final[dict[str, dict[str, str]]] = {
    "results": {
        "batch_id": "Batch",
        "functions.target_objective": "Total-Objective",
        "functions.objectives": "Objective",
        "functions.constraints": "Constraint",
        "evaluations.variables": "Control",
    },
    "gradients": {
        "batch_id": "Batch",
        "gradients.target_objective": "Total-Gradient",
        "gradients.objectives": "Grad-objective",
        "gradients.constraints": "Grad-constraint",
    },
    "simulations": {
        "batch_id": "Batch",
        "realization": "Realization",
        "variable": "Control-name",
        "evaluations.variables": "Control",
        "evaluations.objectives": "Objective",
        "evaluations.constraints": "Constraint",
    },
    "perturbations": {
        "batch_id": "Batch",
        "realization": "Realization",
        "perturbation": "Perturbation",
        "evaluations.perturbed_variables": "Control",
        "evaluations.perturbed_objectives": "Objective",
        "evaluations.perturbed_constraints": "Constraint",
    },
    "constraints": {
        "batch_id": "Batch",
        "constraint_info.bound_lower": "BCD-lower",
        "constraint_info.bound_upper": "BCD-upper",
        "constraint_info.linear_lower": "ICD-lower",
        "constraint_info.linear_upper": "ICD-upper",
        "constraint_info.nonlinear_lower": "OCD-lower",
        "constraint_info.nonlinear_upper": "OCD-upper",
        "constraint_info.bound_violation": "BCD-violation",
        "constraint_info.linear_violation": "ICD-violation",
        "constraint_info.nonlinear_violation": "OCD-violation",
    },
}

_TABLE_TYPE_MAP: Final[dict[str, Literal["functions", "gradients"]]] = {
    "results": "functions",
    "gradients": "gradients",
    "simulations": "functions",
    "perturbations": "gradients",
    "constraints": "functions",
}


class EverestDefaultTableHandler(TableHandler):
    def __init__(self) -> None:
        super().__init__(sep="\n")
        self._path: Path | None = None

        for name, columns in _TABLE_COLUMNS.items():
            for domain in ("user", "optimizer"):
                self.add_table(
                    name if domain == "user" else f"{name}_scaled",
                    columns=columns,
                    table_type=_TABLE_TYPE_MAP[name],
                    domain=domain,
                )
        self.set_callback(self._save)

    def _save(self, event: EnOptEvent) -> None:
        if (parent_path := event.context.optimizer.output_dir) is not None:
            if self._path is None:
                if parent_path.exists() and not parent_path.is_dir():
                    msg = f"Cannot write tables to: {parent_path}"
                    raise RuntimeError(msg)
                self._path = parent_path
            for name, data in self.get_tables().items():
                (self._path / name).with_suffix(".txt").write_text(
                    tabulate(
                        {str(column): data[column] for column in data},
                        headers="keys",
                        tablefmt="simple",
                        showindex=False,
                    ),
                    encoding="utf-8",
                )
