"""Atomic applicator for theorem v2."""

from __future__ import annotations

from typing import Any, Dict, Optional

from .base import TheoremModelV2
from .expressions import ConservativeSolver
from .schema import ApplicationResult, ApplicationStatus, StateDelta
from .state import InformationState


class ApplicatorV2:
    def __init__(self, solver: Optional[ConservativeSolver] = None):
        self.solver = solver or ConservativeSolver()

    def apply(
        self,
        model: TheoremModelV2,
        state: InformationState,
        binding: Optional[Dict[str, Any]] = None,
    ) -> ApplicationResult:
        try:
            matches = model.match(state)
            if binding is None:
                if not matches:
                    return ApplicationResult(
                        model.model_id, ApplicationStatus.NO_MATCH, {}
                    )
                if len(matches) > 1:
                    return ApplicationResult(
                        model.model_id,
                        ApplicationStatus.AMBIGUOUS_BINDING,
                        {},
                    )
                binding = matches[0]
            elif binding not in matches:
                return ApplicationResult(
                    model.model_id,
                    ApplicationStatus.PRECONDITION_UNRESOLVED,
                    binding,
                )

            derivation = model.derive(state, binding, self.solver)
            commit = state.commit_delta(derivation.delta, self.solver)
            if commit.conflicts:
                return ApplicationResult(
                    model_id=model.model_id,
                    status=ApplicationStatus.CONFLICT,
                    binding=binding,
                    delta=derivation.delta,
                    evidence_fact_ids=derivation.evidence_fact_ids,
                    conflicts=commit.conflicts,
                )

            if commit.added_count == 0:
                return ApplicationResult(
                    model_id=model.model_id,
                    status=ApplicationStatus.ALREADY_KNOWN,
                    binding=binding,
                    delta=derivation.delta,
                    evidence_fact_ids=derivation.evidence_fact_ids,
                    state_after=state,
                )

            errors = model.validate(
                state, commit.state, derivation, self.solver
            )
            if errors:
                return ApplicationResult(
                    model_id=model.model_id,
                    status=ApplicationStatus.POSTCONDITION_FAILED,
                    binding=binding,
                    delta=derivation.delta,
                    evidence_fact_ids=derivation.evidence_fact_ids,
                    postcondition_errors=errors,
                )

            commit.state.history.append(
                (model.model_id, ApplicationStatus.APPLIED.value, dict(binding))
            )
            return ApplicationResult(
                model_id=model.model_id,
                status=ApplicationStatus.APPLIED,
                binding=binding,
                delta=derivation.delta,
                evidence_fact_ids=derivation.evidence_fact_ids,
                state_after=commit.state,
            )
        except (ValueError, ZeroDivisionError) as exc:
            return ApplicationResult(
                model_id=model.model_id,
                status=ApplicationStatus.SOLVER_UNRESOLVED,
                binding=binding or {},
                conflicts=(str(exc),),
            )
        except Exception as exc:  # pragma: no cover - last-resort audit path
            return ApplicationResult(
                model_id=model.model_id,
                status=ApplicationStatus.EXCEPTION,
                binding=binding or {},
                conflicts=(f"{type(exc).__name__}: {exc}",),
            )
