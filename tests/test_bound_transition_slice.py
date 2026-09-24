"""Executable contract tests, including mutations and mathematical counterexamples."""
from copy import deepcopy
import json
from pathlib import Path

import pytest
import sympy as sp

from src.reasoning.bound_slice import solve_asymptote_slice
from src.state.transition_state import TransitionState
from src.theorems.bound_application import BoundAction, BoundApplicator, enumerate_actions

DATA = Path(__file__).resolve().parents[1] / 'data/train_with_models_v3.json'
FACTS = ('G: Hyperbola;m: Number;m>0;Expression(G) = (x^2/4 - y^2/m^2 = 1);'
         'Expression(OneOf(Asymptote(G))) = (5*x - 2*y = 0)')


def setup_state(facts=FACTS):
    state = TransitionState.from_facts(facts, 'm')
    app = BoundApplicator()
    forward = enumerate_actions(state, 5)[0]
    inverse = enumerate_actions(state, 21)[0]
    return state, app, forward, inverse


def test_real_id2_trace_and_terminal_read():
    record = next(p for p in json.loads(DATA.read_text()) if p['id'] == 2)
    result = solve_asymptote_slice(record['fact_expressions'], record['query_expressions'])
    assert result.status == 'solved'
    assert result.answer == 5
    assert [t.action.model_id for t in result.transitions] == [5, 21]
    assert all(t.status == 'applied' for t in result.transitions)
    assert result.state.properties == {('G', 'a_sq'): 4, ('G', 'b_sq'): 25}
    assert result.transitions[0].delta['properties'][('G', 'b_sq')] == sp.Symbol('m', real=True)**2
    assert any(op['operation'] == 'restricted_substitution' for op in result.transitions[1].operations)
    assert result.state.provenance['property:G:b_sq'][-1] == 'action:2'
    root_steps = result.transitions[1].operations
    assert next(op['roots'] for op in root_steps if op['operation'] == 'real_roots') == (-5, 5)
    assert any(op['operation'] == 'check_root' and op['root'] == -5
               and False in op['checks'] for op in root_steps)
    abstract = result.state.abstract('G')
    assert abstract.reasoning_depth == 2 and len(abstract.to_vector()) == 28


def test_initial_state_does_not_execute_models_or_extract_answer():
    state, _, _, _ = setup_state()
    assert state.properties == {} and state.history == []
    assert state.extract_answer() is None


def test_rm21_requires_parameter_transition():
    state, app, _, inverse = setup_state()
    before = deepcopy(state)
    assert app.apply(state, inverse).status == 'inapplicable'
    assert state == before


def test_rm5_and_rm21_are_idempotent():
    state, app, forward, inverse = setup_state()
    assert app.apply(state, forward).status == 'applied'
    before = deepcopy(state)
    assert app.apply(state, forward).status == 'no_op' and state == before
    assert app.apply(state, inverse).status == 'applied'
    before = deepcopy(state)
    assert app.apply(state, inverse).status == 'no_op' and state == before
    assert app.apply(state, forward).status == 'no_op' and state == before


def test_missing_positive_constraint_keeps_both_roots():
    state, app, forward, inverse = setup_state(FACTS.replace('m>0;', ''))
    assert app.apply(state, forward).status == 'applied'
    before = deepcopy(state)
    result = app.apply(state, inverse)
    assert result.status == 'undetermined' and result.candidates == (-5, 5)
    assert state == before and state.extract_answer() is None


@pytest.mark.parametrize('constraint,answer', [('m<0', -5), ('m>6', None)])
def test_constraint_filtering(constraint, answer):
    result = solve_asymptote_slice(FACTS.replace('m>0', constraint), 'm')
    assert result.answer == answer
    assert result.status == ('solved' if answer is not None else 'conflict')


@pytest.mark.parametrize('line', ['5*x - 2*y + 1 = 0', 'x = 0', 'x^2-y=0'])
def test_non_asymptote_geometry_rejected_without_mutation(line):
    state, app, forward, inverse = setup_state(FACTS.replace('5*x - 2*y = 0', line))
    assert app.apply(state, forward).status == 'applied'
    before = deepcopy(state)
    assert app.apply(state, inverse).status == 'inapplicable'
    assert state == before


def test_multiple_curves_are_scoped_and_wrong_binding_rejected():
    facts = FACTS + ';H: Hyperbola;Expression(H) = (x^2/9-y^2/16=1)'
    state, app, _, inverse = setup_state(facts)
    for action in enumerate_actions(state, 5):
        assert app.apply(state, action).status == 'applied'
    assert state.properties[('G', 'a_sq')] == 4
    assert state.properties[('H', 'a_sq')] == 9
    h_eq = next(f.fact_id for f in state.equations.values() if f.owner == 'H')
    before = deepcopy(state)
    wrong = BoundAction(21, 'constrain_parameters', 'H', h_eq, inverse.line_equation_id)
    assert app.apply(state, wrong).status == 'inapplicable' and state == before
    assert app.apply(state, inverse).status == 'applied'
    assert state.properties[('H', 'b_sq')] == 16


def test_conflicting_property_rolls_back():
    state, app, forward, _ = setup_state()
    state.properties[('G', 'a_sq')] = sp.Integer(9)
    before = deepcopy(state)
    assert app.apply(state, forward).status == 'conflict' and state == before


def test_conflicting_value_rolls_back():
    state, app, forward, inverse = setup_state()
    app.apply(state, forward)
    state.values[state.query] = sp.Integer(6)
    before = deepcopy(state)
    assert app.apply(state, inverse).status == 'conflict' and state == before


@pytest.mark.parametrize('equation', ['y^2/4-x^2/m^2=1', '(x-1)^2/4-y^2/m^2=1'])
def test_wrong_axis_or_shifted_curve_not_silently_accepted(equation):
    state, app, forward, _ = setup_state(FACTS.replace('x^2/4 - y^2/m^2 = 1', equation))
    before = deepcopy(state)
    assert app.apply(state, forward).status == 'inapplicable' and state == before


def test_unknown_parameter_sign_is_not_assumed():
    state, app, forward, _ = setup_state(FACTS.replace('m>0;', '').replace('y^2/m^2', 'y^2/m'))
    before = deepcopy(state)
    assert app.apply(state, forward).status == 'undetermined' and state == before


@pytest.mark.parametrize('expression', ["__import__('os')", 'm.real', 'unknown+1', '1/0'])
def test_parser_rejects_unsupported_expressions(expression):
    with pytest.raises((ValueError, SyntaxError)):
        TransitionState.from_facts(FACTS.replace('5*x - 2*y', expression), 'm')


def test_proposal_failure_cannot_mutate_caller():
    state, app, forward, _ = setup_state()
    model = app.library.get_model(5)
    def broken(copy, action):
        copy.properties[('G', 'a_sq')] = sp.Integer(100)
        raise ValueError('test failure')
    model.propose_bound = broken
    before = deepcopy(state)
    assert app.apply(state, forward).status == 'failed' and state == before


@pytest.mark.parametrize('line,answer', [('3*x-2*y=0', 3), ('5*x+2*y=0', 5), ('10*x-4*y=0', 5)])
def test_same_contract_generalizes_to_other_asymptotes(line, answer):
    result = solve_asymptote_slice(FACTS.replace('5*x - 2*y = 0', line), 'm')
    assert result.status == 'solved' and result.answer == answer


def test_legacy_model_interfaces_remain_callable():
    from src.state.symbolic_state import SymbolicState
    from src.theorems.theorem_library import TheoremLibrary
    library = TheoremLibrary()
    legacy = SymbolicState(entities={'G': 'Hyperbola'},
                           equations=['Expression(G) = (x^2/4 - y^2/9 = 1)'])
    assert library.get_model(5).can_apply(legacy)
    assert library.get_model(5).apply(legacy)
    assert library.get_model(21).can_apply(legacy)
    assert library.get_model(21).apply(legacy)
    assert any('Asymptote(G)' in eq for eq in legacy.equations)
