"""Parabola point recovery and focal-radius contracts, including real ID 5."""
from copy import deepcopy
from dataclasses import replace
import json
from pathlib import Path

import pytest
import sympy as sp
from src.reasoning.bound_slice import solve_parabola_focal_slice
from src.state.transition_state import TransitionState
from src.theorems.bound_application import BoundApplicator, enumerate_actions

FACTS = ('G: Parabola;Expression(G)=(x^2=a*y);a: Number;A: Point;'
         'Coordinate(A)=(1,1/4);PointOnCurve(A,G)')
QUERY = 'Distance(A, Focus(G))'


def make_case(facts=FACTS):
    s = TransitionState.from_facts(facts, QUERY)
    app = BoundApplicator()
    return s, app, enumerate_actions(s, 9, 'recover_from_point')[0], enumerate_actions(s, 17)[0]


def test_real_id5_complete_transition_and_independent_geometry():
    rows = json.loads((Path(__file__).resolve().parents[1]/'data/train_with_models_v3.json').read_text())
    row = next(r for r in rows if r['id'] == 5)
    r = solve_parabola_focal_slice(row['fact_expressions'], row['query_expressions'])
    assert r.status == 'solved' and r.answer == sp.Rational(5, 4)
    assert [t.action.model_id for t in r.transitions] == [9, 17]
    assert r.state.values[r.state.symbols['a']] == 4
    assert r.state.properties['G', 'p'] == 2
    assert (r.state.properties['G', 'focus_x'], r.state.properties['G', 'focus_y']) == (0, 1)
    assert sp.sqrt(1+(sp.Rational(1,4)-1)**2) == r.answer
    assert r.transitions[0].operations[0]['operation'] == 'instantiate_point_incidence'
    assert r.transitions[1].action.coordinate_id in r.transitions[1].read_facts
    assert not any('directrix' in key[1] for key in r.state.properties)
    assert r.state.abstract('G').query_type.name == 'DISTANCE'


def test_initial_state_and_missing_model_dependency():
    s, app, _, radius = make_case()
    assert not s.properties and not s.values and not s.frames and s.extract_answer() is None
    before = deepcopy(s)
    assert app.apply(s, radius).status == 'inapplicable' and s == before


@pytest.mark.parametrize('equation,point,mid,focus', [
    ('x^2=a*y', '(1,1/4)', 9, (0,1)),
    ('x^2=a*y', '(1,-1/4)', 10, (0,-1)),
    ('y^2=a*x', '(1/4,1)', 7, (1,0)),
    ('y^2=a*x', '(-1/4,1)', 8, (-1,0)),
])
def test_four_directions_recover_before_direction_filter(equation, point, mid, focus):
    facts = FACTS.replace('x^2=a*y', equation).replace('(1,1/4)', point)
    result = solve_parabola_focal_slice(facts, QUERY)
    assert result.status == 'solved' and result.answer == sp.Rational(5,4)
    assert result.transitions[0].action.model_id == mid
    assert tuple(result.state.properties['G', k] for k in ('focus_x','focus_y')) == focus


def test_wrong_direction_cannot_commit_recovered_parameter():
    s, app, standard, _ = make_case(FACTS.replace('(1,1/4)','(1,-1/4)'))
    before = deepcopy(s)
    assert app.apply(s, standard).status == 'inapplicable' and s == before


@pytest.mark.parametrize('point,status', [('(0,0)','undetermined'), ('(1,0)','conflict'), ('(0,1)','inapplicable')])
def test_insufficient_inconsistent_or_degenerate_points(point, status):
    r = solve_parabola_focal_slice(FACTS.replace('(1,1/4)',point), QUERY)
    assert r.status == status and r.answer is None and not r.state.values


def test_multiple_parameter_roots_not_filtered_by_model_direction():
    s, app, standard, _ = make_case(FACTS.replace('a*y','a^2*y'))
    before = deepcopy(s)
    result = app.apply(s, standard)
    assert result.status == 'undetermined' and result.candidates == (-2,2) and s == before
    assert solve_parabola_focal_slice(FACTS.replace('a*y','a^2*y'), QUERY).answer is None


def test_repeat_both_actions_noop():
    s, app, standard, radius = make_case()
    assert app.apply(s, standard).status == 'applied'
    assert s.extract_answer() is None
    assert app.apply(s, radius).status == 'applied'
    before = deepcopy(s)
    for action in (standard, radius):
        assert app.apply(s, action).status == 'no_op' and s == before


@pytest.mark.parametrize('edit', [dict(point='B'),dict(relation_id='missing'),dict(coordinate_id='wrong')])
def test_wrong_binding_is_atomic(edit):
    s, app, standard, _ = make_case()
    before = deepcopy(s)
    assert app.apply(s, replace(standard, **edit)).status == 'inapplicable' and s == before


def test_other_curve_incidence_cannot_be_used():
    facts=FACTS.replace('PointOnCurve(A,G)', 'H: Parabola;Expression(H)=(x^2=4*y);PointOnCurve(A,H)')
    assert solve_parabola_focal_slice(facts, QUERY).status == 'undetermined'


def test_property_conflict_rolls_back_parameter_assignment_and_frame():
    s, app, standard, _ = make_case()
    s.properties['G','p'] = sp.Integer(3)
    before = deepcopy(s)
    assert app.apply(s, standard).status == 'conflict' and s == before


def test_radius_rechecks_incidence_and_frame():
    s, app, standard, radius = make_case()
    app.apply(s, standard)
    s.coordinates['A'] = replace(s.coordinates['A'], xy=(sp.Integer(2),sp.Integer(1)))
    assert app.apply(s, radius).status == 'applied' and s.extract_answer() == 2
    s.coordinates['A'] = replace(s.coordinates['A'], xy=(sp.Integer(2),sp.Integer(2)))
    before = deepcopy(s)
    assert app.apply(s, radius).status == 'conflict' and s == before


@pytest.mark.parametrize('eq', ['(x-1)^2=a*y', 'x^2=a*y+x*y', 'a*x^2=4*a*y'])
def test_shift_rotation_and_unknown_common_factor_not_accepted(eq):
    result = solve_parabola_focal_slice(FACTS.replace('x^2=a*y',eq), QUERY)
    assert result.status in ('inapplicable','undetermined') and result.answer is None


def test_symbolic_point_and_multiple_unknown_coefficients_are_unresolved():
    for facts in (FACTS.replace('(1,1/4)','(a,1/4)'), FACTS.replace('a: Number','a: Number;b: Real').replace('a*y','(a+b)*y')):
        assert solve_parabola_focal_slice(facts, QUERY).status == 'undetermined'


def test_given_constant_parabola_can_use_extract_then_radius():
    s, app, _, radius = make_case(FACTS.replace('a*y','4*y'))
    extract = enumerate_actions(s, 9, 'extract_parameters')[0]
    assert app.apply(s, extract).status == 'applied'
    assert app.apply(s, radius).status == 'applied' and s.extract_answer() == sp.Rational(5,4)


def test_duplicate_coordinates_and_undeclared_incidence_rejected():
    with pytest.raises(ValueError):
        TransitionState.from_facts(FACTS+';Coordinate(A)=(2,1)', QUERY)
    with pytest.raises(ValueError):
        TransitionState.from_facts(FACTS.replace('PointOnCurve(A,G)','PointOnCurve(B,G)'), QUERY)


def test_given_constraint_is_used_without_direction_assumption():
    result = solve_parabola_focal_slice(FACTS+';a<0', QUERY)
    assert result.status == 'conflict' and result.answer is None and not result.state.values


def test_frame_tampering_is_rejected_by_radius():
    s, app, standard, radius = make_case()
    app.apply(s, standard)
    s.frames['G'] = replace(s.frames['G'], direction='down')
    before = deepcopy(s)
    assert app.apply(s, radius).status == 'inapplicable' and s == before


def test_rational_coefficient_preserves_denominator_domain():
    result = solve_parabola_focal_slice(FACTS.replace('a*y','((a^2-1)/(a-1))*y'), QUERY)
    assert result.status == 'solved' and result.state.values[result.state.symbols['a']] == 3
    assert any(':domain:' in key for key in result.state.constraints)


@pytest.mark.parametrize('mid,eq', [(7,'y^2=4*x'),(8,'y^2=-4*x'),(9,'x^2=4*y'),(10,'x^2=-4*y')])
def test_legacy_parabola_models_unchanged(mid,eq):
    from src.state.symbolic_state import SymbolicState
    from src.theorems.theorem_library import TheoremLibrary
    s = SymbolicState(entities={'G':'Parabola'},equations=[f'Expression(G) = ({eq})'])
    model = TheoremLibrary().get_model(mid)
    assert model.can_apply(s)
    model.apply(s)
    assert 'p' in s.parameters
