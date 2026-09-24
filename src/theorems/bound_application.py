"""Transactional bound-model application, initially for RM5 and RM21 only."""
from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field

import sympy as sp

from src.solver.transition_primitives import TransitionError, truth
from src.state.transition_state import TransitionState


@dataclass(frozen=True)
class BoundAction:
    model_id: int
    mode: str
    curve: str
    equation_id: str
    line_equation_id: str | None = None


@dataclass
class Proposal:
    properties: dict = field(default_factory=dict)
    values: dict = field(default_factory=dict)
    read_facts: tuple[str, ...] = ()
    operations: list[dict] = field(default_factory=list)
    candidates: tuple = ()


@dataclass
class TransitionResult:
    status: str
    action: BoundAction
    before_revision: int
    after_revision: int
    delta: dict = field(default_factory=dict)
    read_facts: tuple[str, ...] = ()
    operations: list[dict] = field(default_factory=list)
    candidates: tuple = ()
    diagnostic: str = ''


def check_binding(state, action):
    if state.entities.get(action.curve) != 'Hyperbola':
        raise TransitionError('inapplicable', 'Binding requires a Hyperbola')
    fact = state.equations.get(action.equation_id)
    if fact is None or fact.owner != action.curve or fact.role != 'curve':
        raise TransitionError('inapplicable', 'Curve equation binding mismatch')
    if action.model_id == 21:
        line = state.equations.get(action.line_equation_id)
        if line is None or line.owner != action.curve or line.role != 'asymptote':
            raise TransitionError('inapplicable', 'Asymptote does not belong to bound curve')
    return fact


def enumerate_actions(state: TransitionState, model_id: int):
    if model_id not in (5, 21):
        return []
    actions = []
    for fact in state.equations.values():
        if fact.role != 'curve' or state.entities.get(fact.owner) != 'Hyperbola':
            continue
        if model_id == 5:
            actions.append(BoundAction(5, 'extract_parameters', fact.owner, fact.fact_id))
        else:
            for line in state.equations.values():
                if line.owner == fact.owner and line.role == 'asymptote':
                    actions.append(BoundAction(21, 'constrain_parameters', fact.owner,
                                               fact.fact_id, line.fact_id))
    return actions


class BoundApplicator:
    def __init__(self, library=None):
        if library is None:
            from .theorem_library import TheoremLibrary
            library = TheoremLibrary()
        self.library = library

    def apply(self, state: TransitionState, action: BoundAction) -> TransitionResult:
        result = TransitionResult('failed', action, state.revision, state.revision)
        try:
            check_binding(state, action)
            model = self.library.get_model(action.model_id)
            if model is None:
                raise TransitionError('inapplicable', 'Model is not registered')
            # Isolate even a misbehaving proposal method from the caller's state.
            proposal = model.propose_bound(deepcopy(state), action)
            result.read_facts = proposal.read_facts
            result.operations = proposal.operations
            result.candidates = proposal.candidates
            if len(proposal.candidates) > 1:
                result.status = 'undetermined'
                result.diagnostic = 'Multiple admissible roots; branch selection is not implemented'
                return result
            values = dict(state.values)
            for symbol, value in proposal.values.items():
                value = sp.simplify(value)
                if value.free_symbols or value.is_real is not True or value.is_finite is not True:
                    raise TransitionError('undetermined', 'Only finite real scalar assignments supported')
                if symbol in values and sp.simplify(values[symbol]-value) != 0:
                    raise TransitionError('conflict', 'Conflicting scalar assignment')
                values[symbol] = value
            for condition in state.constraints.values():
                valid = truth(condition.subs(values))
                if valid is False:
                    raise TransitionError('conflict', 'Assignment violates a given/domain constraint')
                if proposal.values and valid is None:
                    raise TransitionError('undetermined', 'Assignment has unresolved constraints')
            properties = dict(state.properties)
            for key, value in proposal.properties.items():
                value = sp.simplify(value.subs(values))
                if key in properties:
                    equal = truth(sp.Eq(properties[key].subs(values), value))
                    if equal is not True:
                        raise TransitionError('conflict' if equal is False else 'undetermined',
                                              'Object property is inconsistent or unresolved')
                properties[key] = value
            # Only substitute known scalar assignments into existing properties.
            # No new theorem, variable solving, or model choice occurs here.
            for key, value in list(properties.items()):
                reduced = sp.simplify(value.subs(values))
                if reduced != value:
                    result.operations.append({'operation': 'restricted_substitution',
                                              'property': key, 'before': value, 'after': reduced,
                                              'substitution': dict(values)})
                properties[key] = reduced
            changed_properties = {k: v for k, v in properties.items() if state.properties.get(k) != v}
            changed_values = {k: v for k, v in values.items() if state.values.get(k) != v}
            if not changed_properties and not changed_values:
                result.status = 'no_op'
                return result
            result.delta = {'properties': changed_properties, 'values': changed_values}
            result.status = 'applied'
            result.after_revision += 1
            provenance = dict(state.provenance)
            for key in changed_properties:
                source_key = f'property:{key[0]}:{key[1]}'
                provenance[source_key] = tuple(dict.fromkeys(
                    (*provenance.get(source_key, ()), *proposal.read_facts,
                     f'action:{result.after_revision}')))
            for key in changed_values:
                provenance[f'value:{key}'] = (*proposal.read_facts, f'action:{result.after_revision}')
            state.properties, state.values, state.provenance = properties, values, provenance
            state.revision = result.after_revision
            state.history.append(deepcopy(result))
        except TransitionError as exc:
            result.status, result.diagnostic = exc.status, str(exc)
        except (ValueError, TypeError, KeyError, NotImplementedError, sp.PolynomialError) as exc:
            result.status, result.diagnostic = 'failed', str(exc)
        return result
