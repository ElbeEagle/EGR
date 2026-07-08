"""Sequence validation and conservative repair for theorem v2."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Sequence, Tuple

from .applicator import ApplicatorV2
from .complete_library import CompleteTheoremLibraryV2, SupportLevel
from .schema import ApplicationStatus
from .state import InformationState


class IssueKind(str, Enum):
    DIRECTION_MISMATCH = "DIRECTION_MISMATCH"
    DEPENDENCY_REORDERED = "DEPENDENCY_REORDERED"
    DEPENDENCY_INSERTED = "DEPENDENCY_INSERTED"
    BRANCH_REQUIRED = "BRANCH_REQUIRED"
    SPECIFICATION_ONLY = "SPECIFICATION_ONLY"
    NO_MATCH = "NO_MATCH"
    AMBIGUOUS = "AMBIGUOUS"


@dataclass(frozen=True)
class SequenceIssue:
    kind: IssueKind
    index: int
    model_id: int
    message: str


@dataclass(frozen=True)
class RepairOperation:
    operation: str
    index: int
    before: Tuple[int, ...]
    after: Tuple[int, ...]


@dataclass(frozen=True)
class TraceStep:
    index: int
    model_id: int
    status: str


@dataclass(frozen=True)
class SequenceRepairResult:
    original_sequence: Tuple[int, ...]
    repaired_sequence: Tuple[int, ...]
    issues: Tuple[SequenceIssue, ...]
    operations: Tuple[RepairOperation, ...]
    trace: Tuple[TraceStep, ...]
    branches: Tuple[Tuple[int, ...], ...] = ()
    state_after: Optional[InformationState] = None
    confidence: float = 1.0


class SequenceCorrector:
    """Repair only cases supported by state evidence or dependency contracts."""

    DIRECTIONAL_PARABOLA_IDS = (7, 8, 9, 10)

    def __init__(
        self,
        library: Optional[CompleteTheoremLibraryV2] = None,
        applicator: Optional[ApplicatorV2] = None,
    ):
        self.library = library or CompleteTheoremLibraryV2()
        self.applicator = applicator or ApplicatorV2()

    def repair(
        self,
        sequence: Sequence[int],
        initial_state: InformationState,
    ) -> SequenceRepairResult:
        original = tuple(sequence)
        repaired = list(sequence)
        issues: List[SequenceIssue] = []
        operations: List[RepairOperation] = []

        self._reorder_directrix_before_definition(
            repaired, issues, operations
        )
        branches = self._detect_axis_branches(repaired, initial_state, issues)

        state = initial_state
        trace: List[TraceStep] = []
        index = 0
        insertion_budget = 16
        while index < len(repaired):
            model_id = repaired[index]
            if model_id not in self.library.models:
                issues.append(
                    SequenceIssue(
                        IssueKind.NO_MATCH,
                        index,
                        model_id,
                        "model id is outside the 0-79 catalog",
                    )
                )
                trace.append(TraceStep(index, model_id, "UNKNOWN_MODEL"))
                index += 1
                continue

            corrected_direction = self._direction_from_state(state)
            if (
                model_id in self.DIRECTIONAL_PARABOLA_IDS
                and corrected_direction is not None
                and corrected_direction != model_id
            ):
                before = tuple(repaired)
                repaired[index] = corrected_direction
                issues.append(
                    SequenceIssue(
                        IssueKind.DIRECTION_MISMATCH,
                        index,
                        model_id,
                        f"state matches model {corrected_direction}, not {model_id}",
                    )
                )
                operations.append(
                    RepairOperation(
                        "replace_directional_model",
                        index,
                        before,
                        tuple(repaired),
                    )
                )
                model_id = corrected_direction

            capability = self.library.get_capability(model_id)
            if capability.support_level == SupportLevel.SPECIFICATION_ONLY:
                issues.append(
                    SequenceIssue(
                        IssueKind.SPECIFICATION_ONLY,
                        index,
                        model_id,
                        "v2 requirement exists but concrete executor is pending",
                    )
                )
                trace.append(TraceStep(index, model_id, "SPECIFICATION_ONLY"))
                index += 1
                continue

            model = self.library.get_model(model_id)
            result = self.applicator.apply(model, state)
            if result.status in {
                ApplicationStatus.APPLIED,
                ApplicationStatus.ALREADY_KNOWN,
            }:
                trace.append(TraceStep(index, model_id, result.status.value))
                if result.state_after is not None:
                    state = result.state_after
                index += 1
                continue

            dependency = self._applicable_dependency(model_id, state)
            if dependency is not None and insertion_budget > 0:
                before = tuple(repaired)
                repaired.insert(index, dependency)
                insertion_budget -= 1
                issues.append(
                    SequenceIssue(
                        IssueKind.DEPENDENCY_INSERTED,
                        index,
                        model_id,
                        f"inserted applicable dependency model {dependency}",
                    )
                )
                operations.append(
                    RepairOperation(
                        "insert_dependency", index, before, tuple(repaired)
                    )
                )
                continue

            kind = (
                IssueKind.AMBIGUOUS
                if result.status == ApplicationStatus.AMBIGUOUS_BINDING
                else IssueKind.NO_MATCH
            )
            issues.append(
                SequenceIssue(
                    kind,
                    index,
                    model_id,
                    f"application status: {result.status.value}",
                )
            )
            trace.append(TraceStep(index, model_id, result.status.value))
            index += 1

        severe = sum(
            issue.kind
            in {IssueKind.NO_MATCH, IssueKind.AMBIGUOUS, IssueKind.SPECIFICATION_ONLY}
            for issue in issues
        )
        confidence = max(
            0.0,
            1.0 - 0.05 * len(operations) - 0.15 * severe - 0.1 * bool(branches),
        )
        return SequenceRepairResult(
            original_sequence=original,
            repaired_sequence=tuple(repaired),
            issues=tuple(issues),
            operations=tuple(operations),
            trace=tuple(trace),
            branches=branches,
            state_after=state,
            confidence=confidence,
        )

    def _direction_from_state(self, state: InformationState) -> Optional[int]:
        matches = []
        for model_id in self.DIRECTIONAL_PARABOLA_IDS:
            model = self.library.get_model(model_id)
            if model.match(state):
                matches.append(model_id)
        return matches[0] if len(matches) == 1 else None

    def _applicable_dependency(
        self, model_id: int, state: InformationState
    ) -> Optional[int]:
        requirement = self.library.get_requirement(model_id)
        if requirement is None:
            return None
        for dependency in requirement.dependencies:
            capability = self.library.get_capability(dependency)
            if capability.support_level != SupportLevel.CONCRETE:
                continue
            model = self.library.get_model(dependency)
            dependency_result = self.applicator.apply(model, state)
            if dependency_result.status == ApplicationStatus.APPLIED:
                return dependency
        return None

    @staticmethod
    def _reorder_directrix_before_definition(
        sequence: List[int],
        issues: List[SequenceIssue],
        operations: List[RepairOperation],
    ) -> None:
        if 2 not in sequence or 29 not in sequence:
            return
        definition_index = sequence.index(2)
        directrix_index = sequence.index(29)
        if definition_index >= directrix_index:
            return
        before = tuple(sequence)
        sequence.pop(directrix_index)
        sequence.insert(definition_index, 29)
        issues.append(
            SequenceIssue(
                IssueKind.DEPENDENCY_REORDERED,
                definition_index,
                2,
                "moved parabola directrix before definition",
            )
        )
        operations.append(
            RepairOperation(
                "move_dependency_before_consumer",
                definition_index,
                before,
                tuple(sequence),
            )
        )

    @staticmethod
    def _detect_axis_branches(
        sequence: Sequence[int],
        state: InformationState,
        issues: List[SequenceIssue],
    ) -> Tuple[Tuple[int, ...], ...]:
        for index, pair in enumerate(zip(sequence, sequence[1:])):
            if pair != (3, 4):
                continue
            ellipses = [
                symbol
                for symbol in state.symbols.values()
                if symbol.type_name == "Ellipse"
            ]
            if len(ellipses) != 1:
                continue
            left = tuple(sequence[:index]) + (3,) + tuple(sequence[index + 2 :])
            right = tuple(sequence[:index]) + (4,) + tuple(sequence[index + 2 :])
            issues.append(
                SequenceIssue(
                    IssueKind.BRANCH_REQUIRED,
                    index,
                    3,
                    "models 3 and 4 form alternative ellipse-axis branches",
                )
            )
            return (left, right)
        return ()
