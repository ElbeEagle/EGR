"""End-to-end replay benchmark and selector trajectory export."""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Sequence

from .complete_library import SupportLevel
from .goal_checker import GoalCheckerV3
from .macro_applicator import MacroApplicatorV2
from .quantity_closure import QuantityApplicatorV2, QuantityGeometryClosure
from .quantity_library import QuantityTheoremLibraryV2
from .quantity_raw_adapter import QuantityRawFactAdapter
from .schema import ApplicationStatus
from .serialization import serialize_state, serialize_value


_SUCCESS_VALUES = {
    ApplicationStatus.APPLIED.value,
    ApplicationStatus.ALREADY_KNOWN.value,
}


class ReplayBenchmarkV3:
    def __init__(
        self,
        assisted_apply: bool = False,
        max_support_steps: int = 12,
    ):
        self.adapter = QuantityRawFactAdapter()
        self.library = QuantityTheoremLibraryV2()
        self.closure = QuantityGeometryClosure()
        base_applicator = QuantityApplicatorV2(closure=self.closure)
        self.assisted_apply = assisted_apply
        self.applicator = (
            MacroApplicatorV2(
                self.library,
                applicator=base_applicator,
                max_support_steps=max_support_steps,
            )
            if assisted_apply
            else base_applicator
        )
        self.goal_checker = GoalCheckerV3()

    def evaluate_row(
        self,
        row: Dict[str, Any],
        sequence_field: str = "models_v3_observed",
        export_trajectory: bool = True,
    ) -> Dict[str, Any]:
        adaptation = self.adapter.adapt(
            row.get("fact_expressions", ""),
            row.get("query_expressions", ""),
        )
        sequence = tuple(
            row.get(sequence_field)
            or row.get("models")
            or ()
        )
        initial_state = self.closure.enrich(adaptation.state)
        initial_goal = self.goal_checker.check(
            initial_state,
            row.get("query_expressions", ""),
            row.get("answer_expressions", ""),
        )
        replay = self._replay(sequence, adaptation.state)
        final_state = self.closure.enrich(replay["state"])
        goal = self.goal_checker.check(
            final_state,
            row.get("query_expressions", ""),
            row.get("answer_expressions", ""),
        )
        sequence_success = bool(sequence) and replay["first_failure"] is None

        result = {
            "id": row.get("id"),
            "sequence_field": sequence_field,
            "sequence": list(sequence),
            "sequence_success": sequence_success,
            "step_statuses": replay["statuses"],
            "support_model_ids": replay["support_model_ids"],
            "first_failure": replay["first_failure"],
            "initial_goal": {
                "status": initial_goal.status.value,
                "query_kind": initial_goal.query_kind,
                "source_predicate": initial_goal.source_predicate,
                "actual_value": serialize_value(initial_goal.actual_value),
                "expected_value": serialize_value(initial_goal.expected_value),
                "detail": initial_goal.detail,
            },
            "goal": {
                "status": goal.status.value,
                "query_kind": goal.query_kind,
                "source_predicate": goal.source_predicate,
                "actual_value": serialize_value(goal.actual_value),
                "expected_value": serialize_value(goal.expected_value),
                "detail": goal.detail,
            },
            "unparsed_fact_count": len(adaptation.unparsed_facts),
            "unparsed_facts": list(adaptation.unparsed_facts[:10]),
            "adapter_errors": list(adaptation.errors),
            "selector_usable": (
                sequence_success
                and goal.status.value == "ANSWER_CORRECT"
                and initial_goal.status.value != "ANSWER_CORRECT"
            ),
            "goal_progress": (
                goal.status.value == "ANSWER_CORRECT"
                and initial_goal.status.value != "ANSWER_CORRECT"
            ),
        }
        if sequence_success and export_trajectory:
            result["trajectory"] = self._trajectory(
                sequence, adaptation.state
            )
        return result

    def _replay(self, sequence, initial_state):
        state = initial_state
        statuses = []
        support_model_ids = []
        first_failure = None
        for index, model_id in enumerate(sequence):
            capability = self.library.get_capability(model_id)
            if capability is None:
                status = "UNKNOWN_MODEL"
                result = None
            elif capability.support_level == SupportLevel.SPECIFICATION_ONLY:
                status = "SPECIFICATION_ONLY"
                result = None
            else:
                result = self.applicator.apply(
                    self.library.get_model(model_id), state
                )
                status = result.status.value
            statuses.append(status)
            support_model_ids.append(
                [
                    step.model_id
                    for step in (
                        result.support_applications
                        if result is not None
                        else ()
                    )
                ]
            )
            if status not in _SUCCESS_VALUES and first_failure is None:
                first_failure = self._failure(
                    index, model_id, status, state
                )
            if result is not None and result.state_after is not None:
                state = result.state_after
        return {
            "state": state,
            "statuses": statuses,
            "support_model_ids": support_model_ids,
            "first_failure": first_failure,
        }

    def _trajectory(self, sequence, initial_state):
        state = initial_state
        steps = []
        for index, model_id in enumerate(sequence):
            state = self.closure.enrich(state)
            before = serialize_state(state)
            unique, ambiguous = self._applicable_models(state)
            result = self.applicator.apply(
                self.library.get_model(model_id), state
            )
            after_state = result.state_after or state
            theorem_slots = {
                fact.slot_key for fact in result.delta.add_facts
            }
            for support in result.support_applications:
                theorem_slots.update(
                    fact.slot_key for fact in support.delta.add_facts
                )
            closure_added = [
                fact
                for slot, fact in after_state.facts.items()
                if slot not in state.facts and slot not in theorem_slots
            ]
            steps.append(
                {
                    "index": index,
                    "model_id": model_id,
                    "status": result.status.value,
                    "binding": serialize_value(
                        {
                            key: value
                            for key, value in result.binding.items()
                            if not key.startswith("_")
                        }
                    ),
                    "evidence_fact_ids": list(
                        result.evidence_fact_ids
                    ),
                    "delta": serialize_value(result.delta),
                    "support_applications": [
                        {
                            "model_id": support.model_id,
                            "status": support.status.value,
                            "binding": serialize_value(
                                {
                                    key: value
                                    for key, value in support.binding.items()
                                    if not key.startswith("_")
                                }
                            ),
                            "evidence_fact_ids": list(
                                support.evidence_fact_ids
                            ),
                            "delta": serialize_value(support.delta),
                        }
                        for support in result.support_applications
                    ],
                    "closure_delta": [
                        {
                            "fact_id": fact.fact_id,
                            "predicate": fact.predicate,
                            "arguments": serialize_value(fact.arguments),
                            "value": serialize_value(fact.value),
                            "provenance": serialize_value(fact.provenance),
                        }
                        for fact in closure_added
                    ],
                    "applicable_model_ids": unique,
                    "ambiguous_model_ids": ambiguous,
                    "state_before": before,
                    "state_after": serialize_state(after_state),
                }
            )
            state = after_state
        return steps

    def _applicable_models(self, state):
        unique = []
        ambiguous = []
        for model_id in self.library.get_executable_models():
            model = self.library.get_model(model_id)
            try:
                matches = model.match(state)
            except Exception:
                continue
            if len(matches) == 1:
                unique.append(model_id)
            elif len(matches) > 1:
                ambiguous.append(model_id)
        return unique, ambiguous

    def _failure(self, index, model_id, status, state):
        requirement = self.library.get_requirement(model_id)
        if requirement is None:
            return {
                "index": index,
                "model_id": model_id,
                "status": status,
                "missing_predicates": [],
                "missing_types": [],
            }
        missing_predicates = [
            predicate
            for predicate in requirement.required_predicates
            if not state.find(predicate)
        ]
        existing_types = {
            symbol.type_name
            for symbol in state.symbols.values()
        }
        missing_types = [
            type_name
            for type_name in requirement.required_types
            if type_name not in existing_types
        ]
        return {
            "index": index,
            "model_id": model_id,
            "status": status,
            "missing_predicates": missing_predicates,
            "missing_types": missing_types,
        }
