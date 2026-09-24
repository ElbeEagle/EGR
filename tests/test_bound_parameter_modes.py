"""Ordinary parameter relations and forward asymptotes, without gold-driven decisions."""
from copy import deepcopy
from dataclasses import replace

import pytest
import sympy as sp

from src.state.transition_state import TransitionState, AsymptoteQuery, EquationFact
from src.theorems.bound_application import BoundAction, BoundApplicator, enumerate_actions


def parameters(kind, values, constraints=()):
    # Structured upstream facts: these are not claims about text-parser coverage.
    t = sp.Symbol('t', real=True)
    state = TransitionState({'G': kind}, {'x': sp.Symbol('x', real=True),
                             'y': sp.Symbol('y', real=True), 't': t}, {},
                            {f'given:{i}': c for i, c in enumerate(constraints)}, t)
    state.properties = {('G', k): sp.sympify(v) for k, v in values.items()}
    state.provenance = {f'property:G:{k}': ('fixture:explicit',) for k in values}
    return state


@pytest.mark.parametrize('kind,mid,full', [('Ellipse', 11, {'a_sq': 25, 'b_sq': 9, 'c_sq': 16}),
                                         ('Hyperbola', 12, {'a_sq': 9, 'b_sq': 16, 'c_sq': 25})])
@pytest.mark.parametrize('target', ['a_sq', 'b_sq', 'c_sq'])
def test_any_two_squared_parameters_derive_third(kind, mid, full, target):
    s = parameters(kind, {k: v for k, v in full.items() if k != target})
    app = BoundApplicator()
    action = BoundAction(mid, 'derive_' + target, 'G')
    result = app.apply(s, action)
    assert result.status == 'applied' and s.properties['G', target] == full[target]
    assert s.values == {} and s.equations == {}  # No unrelated unknown or curve construction.
    before = deepcopy(s)
    assert app.apply(s, action).status == 'no_op' and s == before
    assert action in enumerate_actions(s, mid, action.mode)


@pytest.mark.parametrize('kind,mid', [('Ellipse', 11), ('Hyperbola', 12)])
def test_missing_second_parameter_not_guessed(kind, mid):
    s = parameters(kind, {'a_sq': 25})
    before = deepcopy(s)
    assert BoundApplicator().apply(s, BoundAction(mid, 'derive_c_sq', 'G')).status == 'inapplicable'
    assert s == before


@pytest.mark.parametrize('kind,mid,known,target', [
    ('Ellipse', 11, {'a_sq': 9, 'b_sq': 16}, 'c_sq'),
    ('Ellipse', 11, {'a_sq': 9, 'b_sq': 9}, 'c_sq'),
    ('Hyperbola', 12, {'a_sq': 25, 'c_sq': 16}, 'b_sq'),
    ('Hyperbola', 12, {'a_sq': -1, 'b_sq': 9}, 'c_sq'),
])
def test_invalid_or_degenerate_parameters_roll_back(kind, mid, known, target):
    s = parameters(kind, known)
    before = deepcopy(s)
    assert BoundApplicator().apply(s, BoundAction(mid, 'derive_' + target, 'G')).status == 'conflict'
    assert s == before


def test_symbolic_parameter_requires_positive_conditions():
    t = sp.Symbol('t', real=True)
    s = parameters('Ellipse', {'a_sq': t+9, 'b_sq': 9})
    app, action = BoundApplicator(), BoundAction(11, 'derive_c_sq', 'G')
    before = deepcopy(s)
    assert app.apply(s, action).status == 'undetermined' and s == before
    s.constraints['given:positive'] = t > 0
    assert app.apply(s, action).status == 'applied' and s.properties['G', 'c_sq'] == t


@pytest.mark.parametrize('kind,mid,a,b,c,expected', [('Ellipse', 11, 25, 't', 16, 9),
                                                   ('Hyperbola', 12, 7, 't', 16, 9)])
def test_parameter_equation_solves_scalar(kind, mid, a, b, c, expected):
    t = sp.Symbol('t', real=True)
    s = parameters(kind, {'a_sq': a, 'b_sq': t, 'c_sq': c})
    result = BoundApplicator().apply(s, BoundAction(mid, 'constrain_parameters', 'G'))
    assert result.status == 'applied' and s.extract_answer() == expected
    assert s.properties['G', 'b_sq'] == expected


def test_multiple_roots_are_preserved_then_filtered():
    t = sp.Symbol('t', real=True)
    s = parameters('Hyperbola', {'a_sq': 7, 'b_sq': t**2, 'c_sq': 16})
    app, action = BoundApplicator(), BoundAction(12, 'constrain_parameters', 'G')
    before = deepcopy(s)
    result = app.apply(s, action)
    assert result.status == 'undetermined' and result.candidates == (-3, 3) and s == before
    s.constraints['given:positive'] = t > 0
    assert app.apply(s, action).status == 'applied' and s.extract_answer() == 3


def test_existing_property_conflict_and_other_curve_isolation():
    s = parameters('Hyperbola', {'a_sq': 9, 'b_sq': 16, 'c_sq': 100})
    s.entities['H'] = 'Ellipse'
    s.properties['H', 'c_sq'] = sp.Integer(25)
    before = deepcopy(s)
    assert BoundApplicator().apply(s, BoundAction(12, 'derive_c_sq', 'G')).status == 'conflict'
    assert s == before


def standard_state(query='Expression(Asymptote(G))', denominator='9'):
    return TransitionState.from_facts(
        f'G: Hyperbola;t: Real;t>0;Expression(G)=(x^2/4-y^2/{denominator}=1)', query)


def test_forward_asymptote_pair_query_and_repetition():
    s, app = standard_state(), BoundApplicator()
    action = enumerate_actions(s, 21, 'derive_asymptotes')[0]
    assert s.extract_answer() is None
    assert app.apply(s, action).status == 'inapplicable'
    assert app.apply(s, enumerate_actions(s, 5)[0]).status == 'applied'
    result = app.apply(s, action)
    assert result.status == 'applied' and len(result.delta['equations']) == 2
    x, y = s.symbols['x'], s.symbols['y']
    assert s.extract_answer() == (y-sp.Rational(3, 2)*x, y+sp.Rational(3, 2)*x)
    assert ('G', 'c_sq') not in s.properties and ('G', 'e') not in s.properties
    before = deepcopy(s)
    assert app.apply(s, action).status == 'no_op' and s == before


def test_known_one_asymptote_is_not_complete_pair():
    s = standard_state()
    s.equations['given:line'] = EquationFact('given:line', 'G', 'asymptote',
                                            s.symbols['y']-sp.Rational(3, 2)*s.symbols['x'], 'given')
    assert s.extract_answer() is None


def test_generated_equations_reduce_when_parameter_later_solved():
    s, app = standard_state('t', 't^2'), BoundApplicator()
    app.apply(s, enumerate_actions(s, 5)[0])
    action = enumerate_actions(s, 21, 'derive_asymptotes')[0]
    assert app.apply(s, action).status == 'applied'
    # An independent, explicit upstream focal-parameter fact closes the relation.
    s.properties['G', 'c_sq'] = sp.Integer(13)
    result = app.apply(s, BoundAction(12, 'constrain_parameters', 'G', action.equation_id))
    assert result.status == 'applied' and s.extract_answer() == 3
    assert any(op['operation'] == 'restricted_substitution' and 'equation' in op for op in result.operations)
    assert all(s.symbols['t'] not in f.expression.free_symbols for k, f in s.equations.items()
               if k.startswith('derived:'))
    assert app.apply(s, action).status == 'no_op'


def test_equation_conflict_rolls_back_pair():
    s, app = standard_state(), BoundApplicator()
    app.apply(s, enumerate_actions(s, 5)[0])
    key = 'derived:G:asymptote:1'
    s.equations[key] = EquationFact(key, 'G', 'asymptote', s.symbols['y']-s.symbols['x'], 'fixture')
    before = deepcopy(s)
    assert app.apply(s, enumerate_actions(s, 21, 'derive_asymptotes')[0]).status == 'conflict'
    assert s == before


def test_equation_binding_cannot_be_omitted_to_bypass_conflict():
    s, app = standard_state('t'), BoundApplicator()
    app.apply(s, enumerate_actions(s, 5)[0])
    before = deepcopy(s)
    assert app.apply(s, BoundAction(12, 'derive_c_sq', 'G')).status == 'inapplicable' and s == before


def test_wrong_curve_binding_does_not_generate_lines():
    s, app = standard_state(), BoundApplicator()
    s.entities['H'] = 'Hyperbola'
    action = replace(enumerate_actions(s, 21, 'derive_asymptotes')[0], curve='H')
    before = deepcopy(s)
    assert app.apply(s, action).status == 'inapplicable' and s == before


def test_forward_detects_numerically_incompatible_given_line():
    s, app = standard_state(), BoundApplicator()
    app.apply(s, enumerate_actions(s, 5)[0])
    s.equations['given:line'] = EquationFact('given:line', 'G', 'asymptote',
                                            s.symbols['y']-s.symbols['x'], 'given')
    before = deepcopy(s)
    assert app.apply(s, enumerate_actions(s, 21, 'derive_asymptotes')[0]).status == 'conflict'
    assert s == before


@pytest.mark.parametrize('problem_id,slope', [(65, sp.Rational(4, 3)), (200, 1), (353, sp.Rational(5, 4))])
def test_real_forward_asymptote_records(problem_id, slope):
    import json
    from pathlib import Path
    from src.reasoning.bound_slice import solve_forward_asymptote_slice
    records = json.loads((Path(__file__).resolve().parents[1] / 'data/train_with_models_v3.json').read_text())
    record = next(r for r in records if r['id'] == problem_id)
    result = solve_forward_asymptote_slice(record['fact_expressions'], record['query_expressions'])
    assert result.status == 'solved'
    x, y = result.state.symbols['x'], result.state.symbols['y']
    assert result.answer == (y-slope*x, y+slope*x)
    assert [r.action.mode for r in result.transitions] == ['extract_parameters', 'derive_asymptotes']


@pytest.mark.parametrize('values,status', [({'a_sq': 7, 'b_sq': 9, 'c_sq': 16}, 'no_op'),
                                         ({'a_sq': 7, 'b_sq': 9, 'c_sq': 17}, 'conflict')])
def test_all_numeric_parameters_check_identity(values, status):
    s = parameters('Hyperbola', values)
    before = deepcopy(s)
    assert BoundApplicator().apply(s, BoundAction(12, 'constrain_parameters', 'G')).status == status
    assert s == before


def test_negative_root_is_valid_when_squared_length_is_positive():
    t = sp.Symbol('t', real=True)
    s = parameters('Hyperbola', {'a_sq': 7, 'b_sq': t**2, 'c_sq': 16}, [t < 0])
    assert BoundApplicator().apply(s, BoundAction(12, 'constrain_parameters', 'G')).status == 'applied'
    assert s.extract_answer() == -3


def test_wrong_parameter_model_type_is_rejected():
    s = parameters('Ellipse', {'a_sq': 25, 'b_sq': 9})
    before = deepcopy(s)
    assert BoundApplicator().apply(s, BoundAction(12, 'derive_c_sq', 'G')).status == 'inapplicable'
    assert s == before


def test_unresolved_given_line_not_silently_accepted_by_forward_mode():
    s, app = standard_state('t', 't^2'), BoundApplicator()
    app.apply(s, enumerate_actions(s, 5)[0])
    s.equations['given:line'] = EquationFact('given:line', 'G', 'asymptote',
                                            s.symbols['y']-s.symbols['x'], 'given')
    before = deepcopy(s)
    assert app.apply(s, enumerate_actions(s, 21, 'derive_asymptotes')[0]).status == 'undetermined'
    assert s == before
