"""Integrated entry point for v2 parsing, repair, and assisted closure."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Sequence, Tuple

from .assistant import AuxiliaryReasoner, ClosureResult, GoalEvaluator
from .complete_library import CompleteTheoremLibraryV2
from .correction import SequenceCorrector, SequenceRepairResult
from .raw_adapter import AdaptationResult, RawFactAdapter
from .state import InformationState


@dataclass(frozen=True)
class PipelineResult:
    adaptation: AdaptationResult
    repair: SequenceRepairResult
    closure: Optional[ClosureResult]
    final_state: InformationState
    goals_satisfied: bool
    unresolved_goal_count: int


class TheoremPipelineV2:
    """Run the auditable v2 chain without touching the legacy solver."""

    def __init__(self):
        self.library = CompleteTheoremLibraryV2()
        self.adapter = RawFactAdapter()
        self.corrector = SequenceCorrector(self.library)
        self.assistant = AuxiliaryReasoner(self.library)

    def run(
        self,
        fact_expressions: str,
        query_expressions: str,
        model_sequence: Sequence[int],
        enable_auxiliary_closure: bool = True,
    ) -> PipelineResult:
        adaptation = self.adapter.adapt(
            fact_expressions, query_expressions
        )
        repair = self.corrector.repair(
            model_sequence, adaptation.state
        )
        final_state = repair.state_after or adaptation.state
        closure = None
        if enable_auxiliary_closure:
            closure = self.assistant.saturate(final_state)
            final_state = closure.state
        unresolved = GoalEvaluator.unresolved_goals(final_state)
        return PipelineResult(
            adaptation=adaptation,
            repair=repair,
            closure=closure,
            final_state=final_state,
            goals_satisfied=GoalEvaluator.all_satisfied(final_state),
            unresolved_goal_count=len(unresolved),
        )
