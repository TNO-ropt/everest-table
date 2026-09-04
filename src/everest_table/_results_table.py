from __future__ import annotations

from typing import TYPE_CHECKING, Final, Literal

from ropt.components.event_handlers import DataFrameHandler
from ropt.exceptions import WorkflowError
from tabulate import tabulate

if TYPE_CHECKING:
    from pathlib import Path


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


class EverestDefaultTableHandler(DataFrameHandler):
    def __init__(self) -> None:
        super().__init__(sep="\n", engine="polars")
        self._path: Path | None = None

        for name, columns in _TABLE_COLUMNS.items():
            for scaled in (False, True):
                self.add_table(
                    f"{name}_scaled" if scaled else name,
                    columns=columns,
                    table_type=_TABLE_TYPE_MAP[name],
                    scaled=scaled,
                )
        self.set_callback(self._save)

    def _save(self, output_dir: Path | None) -> None:
        if output_dir is not None:
            if self._path is None:
                if output_dir.exists() and not output_dir.is_dir():
                    msg = f"Cannot write tables to: {output_dir}"
                    raise WorkflowError(msg)
                self._path = output_dir
            for name, data in self.get_tables().items():
                (self._path / name).with_suffix(".txt").write_text(
                    tabulate(
                        {str(column): data[column] for column in data.columns},
                        headers="keys",
                        tablefmt="simple",
                        showindex=False,
                    ),
                    encoding="utf-8",
                )
