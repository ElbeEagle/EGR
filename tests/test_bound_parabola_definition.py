"""Independent directrix/definition replay and shared distance boundaries."""
from copy import deepcopy
from dataclasses import replace
import json
from pathlib import Path

import pytest
import sympy as sp
from src.reasoning.bound_slice import solve_parabola_definition_slice, solve_parabola_focal_slice
from src.solver.distance_operations import point_to_line_distance
from src.solver.transition_primitives import TransitionError
from src.state.transition_state import TransitionState
from src.theorems.bound_application import BoundApplicator, enumerate_actions
from src.theorems.models.model_017 import ParabolaFocalRadius

FACTS = ('G: Parabola;Expression(G)=(x^2=a*y);a: Number;A: Point;'
         'Coordinate(A)=(1,1/4);PointOnCurve(A,G)')
QUERY = 'Distance(A, Focus(G))'
x, y = sp.symbols('x y', real=True)


@pytest.mark.parametrize('line,point,expected', [
    (y+1, (1, sp.Rational(1,4)), sp.Rational(5,4)),
    (x-1, (4,7), 3), (3*x+4*y-5, (1,2), sp.Rational(6,5)),
    (-6*x-8*y+10, (1,2), sp.Rational(6,5)), (x-y,(1,1),0),
])
def test_general_distance(line, point, expected):
    assert point_to_line_distance(line, x, y, point) == expected


@pytest.mark.parametrize('line,point,status', [
    (sp.S.Zero,(1,2),'inapplicable'), (sp.S.One,(1,2),'inapplicable'),
    (x*y,(1,2),'inapplicable'), (1/x+y,(1,2),'inapplicable'),
    (sp.Symbol('k')*x+y,(1,2),'undetermined'),
    (x+y,(sp.oo,2),'undetermined'), (x+y,(sp.I,2),'undetermined'),
])
def test_distance_rejects_unsupported(line, point, status):
    with pytest.raises(TransitionError) as exc:
        point_to_line_distance(line, x, y, point)
    assert exc.value.status == status


def test_id5_without_rm17(monkeypatch):
    rows = json.loads(Path('data/train_with_models_v3.json').read_text())
    row = next(r for r in rows if r['id'] == 5)
    baseline = solve_parabola_focal_slice(row['fact_expressions'], row['query_expressions'])
    def forbidden(*args):
        raise AssertionError('Definition path must not call RM17')
    monkeypatch.setattr(ParabolaFocalRadius, 'propose_bound', forbidden)
    result = solve_parabola_definition_slice(row['fact_expressions'], row['query_expressions'])
    assert result.status == 'solved' and result.answer == baseline.answer == sp.Rational(5,4)
    assert [t.action.model_id for t in result.transitions] == [9,29,52,2]
    assert result.state.equations['derived:G:directrix'].expression == result.state.symbols['y']+1
    assert 'derived:G:directrix' in result.transitions[-1].read_facts
    assert 'property:G:point_line_distance:A:derived:G:directrix' in result.transitions[-1].read_facts


@pytest.mark.parametrize('equation,point,mid,line', [
    ('x^2=a*y','(1,1/4)',9,y+1), ('x^2=a*y','(1,-1/4)',10,y-1),
    ('y^2=a*x','(1/4,1)',7,x+1), ('y^2=a*x','(-1/4,1)',8,x-1),
])
def test_four_directions_and_noops(equation,point,mid,line):
    result = solve_parabola_definition_slice(FACTS.replace('x^2=a*y',equation).replace('(1,1/4)',point), QUERY)
    assert result.status == 'solved' and result.answer == sp.Rational(5,4)
    assert result.transitions[0].action.model_id == mid
    assert result.state.equations['derived:G:directrix'].expression == line
    app = BoundApplicator()
    for t in result.transitions:
        before = deepcopy(result.state)
        assert app.apply(result.state,t.action).status == 'no_op'
        assert result.state == before


def prepared():
    state = TransitionState.from_facts(FACTS, QUERY)
    app = BoundApplicator()
    standard = enumerate_actions(state,9,'recover_from_point')[0]
    directrix = enumerate_actions(state,29)[0]
    return state, app, standard, directrix


def test_dependencies_and_binding_rejection():
    s, app, standard, directrix = prepared()
    before = deepcopy(s)
    assert app.apply(s,directrix).status == 'inapplicable' and s == before
    assert not enumerate_actions(s,52)
    assert app.apply(s,standard).status == 'applied'
    assert app.apply(s,directrix).status == 'applied'
    distance, definition = enumerate_actions(s,52)[0], enumerate_actions(s,2)[0]
    before = deepcopy(s)
    assert app.apply(s,definition).status == 'inapplicable' and s == before
    for bad in (replace(distance,line_equation_id=standard.equation_id),
                replace(distance,coordinate_id='wrong'), replace(definition,relation_id='wrong'),
                replace(distance,curve='H')):
        assert app.apply(s,bad).status == 'inapplicable' and s == before
    assert app.apply(s,distance).status == 'applied' and s.extract_answer() is None
    assert app.apply(s,definition).status == 'applied'


@pytest.mark.parametrize('corruption', ['line','distance','incidence','focus','answer'])
def test_conflicts_rollback(corruption):
    s, app, standard, directrix = prepared()
    app.apply(s,standard); app.apply(s,directrix)
    distance, definition = enumerate_actions(s,52)[0], enumerate_actions(s,2)[0]
    app.apply(s,distance)
    action = definition
    if corruption == 'line':
        f = s.equations['derived:G:directrix']
        s.equations[f.fact_id] = replace(f,expression=s.symbols['y']+2)
    elif corruption == 'distance':
        s.properties['G','point_line_distance:A:derived:G:directrix'] = sp.Integer(9)
        action = distance
    elif corruption == 'incidence':
        s.coordinates['A'] = replace(s.coordinates['A'],xy=(sp.S.One,sp.S.One))
    elif corruption == 'focus':
        s.properties['G','focus_y'] = sp.Integer(2)
    else:
        s.properties['G','focal_radius:A'] = sp.Integer(7)
    before = deepcopy(s)
    assert app.apply(s,action).status == 'conflict' and s == before
