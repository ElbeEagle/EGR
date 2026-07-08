"""Reproducible dataset-level audit for theorem v2."""

from __future__ import annotations

from collections import Counter
from dataclasses import asdict, dataclass
from typing import Any, Dict, Iterable, Mapping, Sequence

from .correction import SequenceCorrector
from .raw_adapter import RawFactAdapter


@dataclass(frozen=True)
class DatasetAuditReport:
    total_rows: int
    eligible_rows: int
    total_steps: int
    trace_statuses: Mapping[str, int]
    issue_counts: Mapping[str, int]
    operation_counts: Mapping[str, int]
    unparsed_fact_atoms: int
    adapter_errors: int

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class DatasetAuditor:
    def __init__(self):
        self.adapter = RawFactAdapter()
        self.corrector = SequenceCorrector()

    def audit(self, rows: Sequence[Mapping[str, Any]]) -> DatasetAuditReport:
        statuses: Counter[str] = Counter()
        issues: Counter[str] = Counter()
        operations: Counter[str] = Counter()
        eligible = 0
        total_steps = 0
        unparsed = 0
        errors = 0

        for row in rows:
            sequence = row.get("models") or []
            process = str(row.get("process") or "").strip()
            if not sequence or not process:
                continue
            eligible += 1
            total_steps += len(sequence)
            adaptation = self.adapter.adapt(
                str(row.get("fact_expressions") or ""),
                str(row.get("query_expressions") or ""),
            )
            unparsed += len(adaptation.unparsed_facts)
            errors += len(adaptation.errors)
            repair = self.corrector.repair(sequence, adaptation.state)
            statuses.update(step.status for step in repair.trace)
            issues.update(issue.kind.value for issue in repair.issues)
            operations.update(
                operation.operation for operation in repair.operations
            )

        return DatasetAuditReport(
            total_rows=len(rows),
            eligible_rows=eligible,
            total_steps=total_steps,
            trace_statuses=dict(statuses),
            issue_counts=dict(issues),
            operation_counts=dict(operations),
            unparsed_fact_atoms=unparsed,
            adapter_errors=errors,
        )
