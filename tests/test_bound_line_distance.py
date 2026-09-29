"""Independent-line binding; real-record projections are not whole-problem solves."""
from copy import deepcopy
from dataclasses import replace
import json
from pathlib import Path

import pytest
import sympy as sp
from src.state.transition_state import TransitionState, PointLineDistanceQuery
from src.theorems.bound_application import BoundApplicator, enumerate_actions
from src.reasoning.bound_slice import solve_point_line_distance_slice

FACTS = 'l: Line;Expression(l)=(3*x+4*y-5=0);A: Point;Coordinate(A)=(1,2)'
QUERY = 'Distance(A, l)'


def test_parse_apply_read_and_provenance():
    s = TransitionState.from_facts(FACTS, QUERY)
    assert s.query == PointLineDistanceQuery('A','l')
    assert s.extract_answer() is None and not s.properties and not s.history
    assert s.abstract('l').query_type.name == 'DISTANCE' and s.abstract('l').has_equation
    action, = enumerate_actions(s,52)
    assert action.curve is None and action.equation_id is None and action.line == 'l'
    app = BoundApplicator()
    t = app.apply(s,action)
    assert t.status == 'applied' and s.extract_answer() == sp.Rational(6,5)
    key = 'property:l:point_line_distance:A:f1'
    assert action.coordinate_id in s.provenance[key] and action.line_equation_id in s.provenance[key]
    before = deepcopy(s)
    assert app.apply(s,action).status == 'no_op' and s == before
    assert enumerate_actions(s,52,'bad') == []


@pytest.mark.parametrize('eq,point,expected', [
    ('x=3','(1,2)',2), ('y=-2','(1,2)',4), ('x-y=0','(1,1)',0),
    ('-6*x-8*y+10=0','(1,2)',sp.Rational(6,5)),
])
def test_orientation_scaling_zero(eq,point,expected):
    r=solve_point_line_distance_slice(FACTS.replace('3*x+4*y-5=0',eq).replace('(1,2)',point),QUERY)
    assert r.status == 'solved' and r.answer == expected


def test_multiple_points_lines_query_filters_and_isolation():
    facts=FACTS+';B: Point;Coordinate(B)=(0,0);h: Line;Expression(h)=(x=10)'
    r=solve_point_line_distance_slice(facts,'Distance(B, h)')
    assert r.status=='solved' and r.answer==10
    assert len(enumerate_actions(r.state,52))==4
    assert len(r.state.properties)==1
    r.state.query=PointLineDistanceQuery('A','l')
    assert r.state.extract_answer() is None


@pytest.mark.parametrize('change', [
    {'line':'h'}, {'line_equation_id':'f3'}, {'coordinate_id':'f1'},
    {'curve':'l'}, {'equation_id':'f1'}, {'point':'B'}, {'model_id':29},
])
def test_wrong_bindings_do_not_commit(change):
    s=TransitionState.from_facts(FACTS,QUERY)
    action,=enumerate_actions(s,52)
    before=deepcopy(s)
    assert BoundApplicator().apply(s,replace(action,**change)).status=='inapplicable'
    assert s==before


@pytest.mark.parametrize('equation,status', [
    ('x*y=1','inapplicable'), ('0=0','inapplicable'), ('0=1','inapplicable'),
    ('a*x+y=1','undetermined'),
])
def test_invalid_or_unresolved_line(equation,status):
    s=TransitionState.from_facts(FACTS.replace('3*x+4*y-5=0',equation)+';a: Number',QUERY)
    before=deepcopy(s)
    t=BoundApplicator().apply(s,enumerate_actions(s,52)[0])
    assert t.status==status and s==before


def test_missing_and_ambiguous_equation():
    for facts in ('l: Line;A: Point;Coordinate(A)=(1,2)',
                  FACTS+';Expression(l)=(x=4)'):
        r=solve_point_line_distance_slice(facts,QUERY)
        assert r.status=='undetermined' and r.answer is None and not r.state.history
    s=TransitionState.from_facts(FACTS+';Expression(l)=(x=4)',QUERY)
    assert BoundApplicator().apply(s,enumerate_actions(s,52)[0]).status=='applied'
    assert s.extract_answer() is None


def test_conflicting_distance_and_constraint_rollback():
    s=TransitionState.from_facts(FACTS,QUERY)
    action,=enumerate_actions(s,52)
    s.properties['l','point_line_distance:A:f1']=sp.Integer(99)
    before=deepcopy(s)
    assert BoundApplicator().apply(s,action).status=='conflict' and s==before
    r=solve_point_line_distance_slice(FACTS+';1=0',QUERY)
    assert r.status=='conflict' and not r.state.history


@pytest.mark.parametrize('query',['Distance(l, A)','Distance(A, missing)','Distance(A, A)'])
def test_query_type_guard(query):
    assert solve_point_line_distance_slice(FACTS,query).status=='failed'


@pytest.mark.parametrize('pid,point,line,expected',[(5882,'F','l',4),(1253,'F','l',10)])
def test_real_explicit_fact_projection(pid,point,line,expected):
    row=next(r for r in json.loads(Path('data/train_with_models_v3.json').read_text()) if r['id']==pid)
    parts=[p.strip() for p in row['fact_expressions'].split(';')]
    selected=[p for p in parts if p in (f'{point}: Point',f'{line}: Line')
              or p.startswith((f'Coordinate({point})',f'Expression({line})'))]
    assert len(selected)==4
    query=f'Distance({point}, {line})'
    assert query != row['query_expressions']  # Explicitly a diagnostic query.
    result=solve_point_line_distance_slice(';'.join(selected),query)
    assert result.status=='solved' and result.answer==expected
    assert [t.action.model_id for t in result.transitions]==[52]
    assert solve_point_line_distance_slice(row['fact_expressions'],row['query_expressions']).status=='failed'
