"""Auditable macro application for abstract natural-language theorem steps."""

from __future__ import annotations

from dataclasses import replace
from typing import List, Optional, Sequence, Set

from .base import TheoremModelV2
from .complete_library import SupportLevel
from .quantity_closure import QuantityApplicatorV2
from .schema import (
    ApplicationResult,
    ApplicationStatus,
    StateDelta,
    SupportApplication,
)
from .state import InformationState


_SUCCESS = {
    ApplicationStatus.APPLIED,
    ApplicationStatus.ALREADY_KNOWN,
}

_RETRYABLE = {
    ApplicationStatus.NO_MATCH,
    ApplicationStatus.PRECONDITION_UNRESOLVED,
    ApplicationStatus.SOLVER_UNRESOLVED,
}

# Text-level actions often omit these deterministic semantic prerequisites.
# Hints affect search order only: every helper is still provisionally applied
# and the chain is committed only if the requested action subsequently works.
_MACRO_SUPPORT_HINTS = {
    2: (29,),  # parabola definition needs a materialized directrix
}


class MacroApplicatorV2:
    """Treat one textual theorem label as a verified executable macro.

    A direct application is always preferred.  If it cannot match, helper
    theorems are provisionally applied and the requested theorem is retried
    after every helper.  The provisional chain is committed only when it
    actually unlocks the requested theorem; otherwise the original failure is
    returned and the input state is untouched.
    """

    def __init__(
        self,
        library,
        applicator: Optional[QuantityApplicatorV2] = None,
        max_support_steps: int = 12,
        allow_global_support: bool = True,
    ):
        self.library = library
        self.applicator = applicator or QuantityApplicatorV2()
        self.max_support_steps = max_support_steps
        self.allow_global_support = allow_global_support
        self._producers = self._build_producer_index()

    def apply(
        self,
        model: TheoremModelV2,
        state: InformationState,
        binding=None,
    ) -> ApplicationResult:
        enriched_state = self.applicator.closure.enrich(state)
        direct = self.applicator.apply_enriched(
            model, enriched_state, binding
        )
        if direct.status in _SUCCESS:
            return direct
        semantic = self._semantic_satisfaction(model.model_id, enriched_state)
        if semantic is not None:
            return semantic
        if binding is not None or direct.status not in _RETRYABLE:
            return direct

        # QuantityApplicatorV2 enriches before every attempted application.
        # Enrich once here as well so cheap matcher checks can reject the vast
        # majority of global helper candidates without repeatedly running the
        # coordinate/quantity/elimination closures.
        trial_state = enriched_state
        previous_state = trial_state
        support: List[SupportApplication] = []
        attempted_without_change: Set[int] = set()

        for _ in range(self.max_support_steps):
            helper = self._next_helper(
                model.model_id,
                trial_state,
                attempted_without_change,
            )
            if helper is None:
                break
            helper_id, helper_result = helper
            if helper_result.status != ApplicationStatus.APPLIED:
                attempted_without_change.add(helper_id)
                continue

            trial_state = helper_result.state_after
            support.append(
                SupportApplication(
                    model_id=helper_id,
                    status=helper_result.status,
                    binding=helper_result.binding,
                    delta=self._effective_delta(previous_state, trial_state),
                    evidence_fact_ids=helper_result.evidence_fact_ids,
                )
            )
            previous_state = trial_state
            attempted_without_change.clear()

            # A failed matcher cannot be repaired by another pass through the
            # same deterministic closure.  Avoid that expensive retry until a
            # helper has actually made the requested model match.
            if not self._has_match(model, trial_state):
                continue
            retried = self.applicator.apply_enriched(model, trial_state)
            if retried.status in _SUCCESS:
                return replace(
                    retried,
                    support_applications=tuple(support),
                )

        # Transactional rollback: helper facts are never returned unless the
        # requested textual action was genuinely unlocked.
        return direct

    @staticmethod
    def _semantic_satisfaction(model_id, state):
        # Legacy model 62 is used in the natural-language labels for both
        # simple proportional vectors and more general linear vector
        # identities.  If the latter has already been parsed and compiled, the
        # abstract textual action is satisfied even though the narrow concrete
        # collinearity executor has no VectorScaleRelation to consume.
        if model_id != 62:
            return None
        relations = state.find("VectorLinearRelation")
        compiled = [
            fact
            for fact in state.find("CompiledCoordinateEquation")
            if len(fact.arguments) >= 2
            and fact.arguments[1] == "vector_linear_relation"
        ]
        ratios = [
            fact
            for fact in state.find("ParameterRatioOf")
            if len(fact.arguments) == 2
            and fact.arguments[1] == "c_over_a"
        ]
        if not relations or not (compiled or ratios):
            return None
        evidence = tuple(
            fact.fact_id
            for fact in (*relations, *compiled, *ratios)
            if fact.fact_id is not None
        )
        return ApplicationResult(
            model_id=model_id,
            status=ApplicationStatus.ALREADY_KNOWN,
            binding={"mode": "compiled_vector_linear_relation"},
            evidence_fact_ids=evidence,
            state_after=state,
        )

    def _next_helper(self, target_id, state, excluded):
        for helper_id in self._candidate_ids(target_id, state):
            if helper_id == target_id or helper_id in excluded:
                continue
            capability = self.library.get_capability(helper_id)
            if (
                capability is None
                or capability.support_level != SupportLevel.CONCRETE
            ):
                continue
            helper_model = self.library.get_model(helper_id)
            if not self._has_unique_match(helper_model, state):
                excluded.add(helper_id)
                continue
            result = self.applicator.apply_enriched(helper_model, state)
            if result.status == ApplicationStatus.APPLIED:
                return helper_id, result
            excluded.add(helper_id)
        return None

    def _candidate_ids(self, target_id, state) -> Sequence[int]:
        requirement = self.library.get_requirement(target_id)
        if requirement is None:
            return ()

        ordered: List[int] = []
        ordered.extend(_MACRO_SUPPORT_HINTS.get(target_id, ()))
        ordered.extend(requirement.dependencies)
        for predicate in requirement.required_predicates:
            if not state.find(predicate):
                ordered.extend(self._producers.get(predicate, ()))
        if self.allow_global_support:
            ordered.extend(self.library.get_executable_models())

        result = []
        seen = set()
        for model_id in ordered:
            if model_id not in seen:
                seen.add(model_id)
                result.append(model_id)
        return result

    @staticmethod
    def _has_match(model, state) -> bool:
        try:
            return bool(model.match(state))
        except (ValueError, ZeroDivisionError):
            return False
        except Exception:  # pragma: no cover - defensive candidate filter
            return False

    @staticmethod
    def _has_unique_match(model, state) -> bool:
        try:
            return len(model.match(state)) == 1
        except (ValueError, ZeroDivisionError):
            return False
        except Exception:  # pragma: no cover - defensive candidate filter
            return False

    def _build_producer_index(self):
        result = {}
        for model_id in self.library.get_executable_models():
            requirement = self.library.get_requirement(model_id)
            if requirement is None:
                continue
            for predicate in requirement.produced_predicates:
                result.setdefault(predicate, []).append(model_id)
        return result

    @staticmethod
    def _effective_delta(before, after) -> StateDelta:
        symbols = tuple(
            symbol
            for name, symbol in after.symbols.items()
            if name not in before.symbols
        )
        facts = tuple(
            fact
            for slot, fact in after.facts.items()
            if slot not in before.facts
        )
        return StateDelta(add_symbols=symbols, add_facts=facts)
