from copy import deepcopy
from dataclasses import replace
import json
from pathlib import Path
import pytest
import sympy as sp
from src.reasoning.bound_slice import solve_ellipse_tangent_slice
from src.state.transition_state import TransitionState
from src.theorems.bound_application import BoundApplicator, enumerate_actions

FACTS='G: Ellipse;P: Point;Expression(G)=(x^2/4+y^2/3=1);Coordinate(P)=(1,3/2);PointOnCurve(P,G)'
QUERY='Expression(TangentOnPoint(P,G))'


def test_original_and_double_intersection():
    row=next(r for r in json.loads(Path('data/train_with_models_v3.json').read_text()) if r['id']==2126)
    r=solve_ellipse_tangent_slice(row['fact_expressions'],row['query_expressions'])
    assert r.status=='solved', r.diagnostic
    x,y=r.state.symbols['x'],r.state.symbols['y']
    assert sp.expand(4*r.answer-(x+2*y-4))==0
    assert [t.action.model_id for t in r.transitions]==[3,38]
    curve=next(f.expression for f in r.state.equations.values() if f.role=='curve')
    reduced=sp.Poly(curve.subs(y,sp.solve(r.answer,y)[0]),x)
    assert sp.discriminant(reduced)==0 and sp.solve(reduced.as_expr(),x)==[1]
    assert not any(k[1]=='c_sq' for k in r.state.properties)
    before=deepcopy(r.state)
    assert r.state.extract_answer()==r.answer and r.state==before
    assert BoundApplicator().apply(r.state,r.transitions[-1].action).status=='no_op' and r.state==before


@pytest.mark.parametrize('curve,point,mid,expected',[
    ('x^2/3+y^2/4=1','3/2,1',4,'x/2+y/4-1'),
    ('x^2/4+y^2/3=1','2,0',3,'x/2-1'),
    ('x^2/3+y^2/4=1','0,-2',4,'-y/2-1'),
    ('3*x^2+4*y^2=12','1,3/2',3,'x/4+y/2-1')])
def test_axes_vertical_horizontal_and_scaled_equation(curve,point,mid,expected):
    facts=f'G: Ellipse;P: Point;Expression(G)=({curve});Coordinate(P)=({point})'
    r=solve_ellipse_tangent_slice(facts,QUERY)
    assert r.status=='solved',r.diagnostic
    assert r.transitions[0].action.model_id==mid
    assert sp.simplify(r.answer-sp.sympify(expected,locals=r.state.symbols))==0


@pytest.mark.parametrize('point',['0,0','3,0','1,1'])
def test_off_curve_declared_incidence_is_not_enough(point):
    r=solve_ellipse_tangent_slice(FACTS.replace('1,3/2',point),QUERY)
    assert r.status=='conflict' and r.answer is None
    assert not any(f.role=='tangent' for f in r.state.equations.values())


def test_missing_standard_not_derived_implicitly():
    s=TransitionState.from_facts(FACTS,QUERY);before=deepcopy(s)
    assert BoundApplicator().apply(s,enumerate_actions(s,38)[0]).status=='inapplicable' and s==before


@pytest.mark.parametrize('change',[{'curve':'P'},{'coordinate_id':'bad'}, {'point':'G'},
                                   {'mode':'bad'},{'line':'H'},{'relation_id':'bad'}])
def test_wrong_binding(change):
    r=solve_ellipse_tangent_slice(FACTS,QUERY);before=deepcopy(r.state)
    assert BoundApplicator().apply(r.state,replace(r.transitions[-1].action,**change)).status=='inapplicable'
    assert r.state==before


def test_conflicting_output_and_parameters():
    for kind in ('parameters','equation'):
        r=solve_ellipse_tangent_slice(FACTS,QUERY);s=r.state
        if kind=='parameters':s.properties[('G','a_sq')]=sp.Integer(9)
        else:
            key='derived:G:tangent:P';s.equations[key]=replace(s.equations[key],expression=s.symbols['x'])
        before=deepcopy(s)
        assert BoundApplicator().apply(s,r.transitions[-1].action).status=='conflict' and s==before


def test_symbolic_point_stays_undetermined():
    r=solve_ellipse_tangent_slice(FACTS.replace('Coordinate(P)=(1,3/2)','t: Real;Coordinate(P)=(t,3/2)'),QUERY)
    assert r.status=='undetermined' and r.answer is None


def test_model_and_query_curve_isolation():
    s=TransitionState.from_facts(FACTS,QUERY)
    assert not enumerate_actions(s,39)
    facts=FACTS+';J: Ellipse;Expression(J)=(x^2/9+y^2/4=1)'
    r=solve_ellipse_tangent_slice(facts,QUERY)
    assert r.status=='solved'
    r.state.query=replace(r.state.query,curve='J')
    assert r.state.extract_answer() is None


@pytest.mark.parametrize('curve',['x^2/4+y^2/4=1','(x-1)^2/4+y^2/3=1'])
def test_circle_and_shifted_ellipse_outside_first_mode(curve):
    r=solve_ellipse_tangent_slice(FACTS.replace('x^2/4+y^2/3=1',curve),QUERY)
    assert r.status not in ('solved','failed') and r.answer is None
