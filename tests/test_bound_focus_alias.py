"""Focus identity instantiation is a standard-model output, not query inference."""
from copy import deepcopy
import json
from pathlib import Path

import pytest
import sympy as sp
from src.state.transition_state import TransitionState
from src.theorems.bound_application import BoundApplicator, enumerate_actions
from src.reasoning.bound_slice import solve_directrix_alias_distance_slice

FACTS='G: Parabola;F: Point;l: Line;Expression(G)=(y=4*x^2);Focus(G)=F;Directrix(G)=l'
QUERY='Distance(F, l)'


@pytest.mark.parametrize('pid,expected',[(946,sp.Rational(1,8)),(1793,sp.Rational(1,4))])
def test_original_problem_and_provenance(pid,expected):
    row=next(r for r in json.loads(Path('data/train_with_models_v3.json').read_text()) if r['id']==pid)
    r=solve_directrix_alias_distance_slice(row['fact_expressions'],row['query_expressions'])
    assert r.status=='solved' and r.answer==expected
    assert [t.action.model_id for t in r.transitions]==[9,29,52]
    c=r.state.coordinates['F']
    assert c.fact_id=='derived:G:focus:F'
    assert {'f3','f4','action:1'} <= set(r.state.provenance[c.fact_id])
    assert c.fact_id in r.transitions[2].read_facts
    assert r.transitions[0].delta['coordinates']['F']==c
    before=deepcopy(r.state)
    for t in r.transitions:
        assert BoundApplicator().apply(r.state,t.action).status=='no_op'
    assert r.state==before


def test_no_initial_inference_or_extra_models():
    s=TransitionState.from_facts(FACTS,QUERY)
    assert s.focus_aliases and not s.coordinates and not s.properties
    assert s.extract_answer() is None
    t=BoundApplicator().apply(s,enumerate_actions(s,9,'extract_parameters')[0])
    assert t.status=='applied' and s.coordinates['F'].xy==(0,sp.Rational(1,16))
    assert s.extract_answer() is None and len(s.history)==1


@pytest.mark.parametrize('eq,mid,xy',[('y^2=4*x',7,(1,0)),('y^2=-4*x',8,(-1,0)),
                                     ('x^2=4*y',9,(0,1)),('x^2=-4*y',10,(0,-1))])
def test_four_directions(eq,mid,xy):
    r=solve_directrix_alias_distance_slice(FACTS.replace('y=4*x^2',eq),QUERY)
    assert r.status=='solved' and r.answer==2
    assert r.state.coordinates['F'].xy==xy and r.transitions[0].action.model_id==mid


@pytest.mark.parametrize('xy,status',[('(0,1/16)','applied'),('(0,2)','conflict')])
def test_existing_coordinates_preserve_or_rollback(xy,status):
    s=TransitionState.from_facts(FACTS+';Coordinate(F)='+xy,QUERY)
    old=s.coordinates['F'];before=deepcopy(s)
    t=BoundApplicator().apply(s,enumerate_actions(s,9,'extract_parameters')[0])
    assert t.status==status and s.coordinates['F']==old
    if status=='conflict':assert s==before
    else:assert 'coordinates' not in t.delta and old.fact_id in t.read_facts


@pytest.mark.parametrize('extra',[';Focus(G)=F',';H: Parabola;Expression(H)=(x^2=4*y);Focus(H)=F'])
def test_multiple_focus_claims_unresolved(extra):
    s=TransitionState.from_facts(FACTS+extra,QUERY);before=deepcopy(s)
    t=BoundApplicator().apply(s,enumerate_actions(s,9,'extract_parameters')[0])
    assert t.status=='undetermined' and s==before


def test_other_curve_focus_not_materialized():
    s=TransitionState.from_facts(FACTS+';H: Parabola;Q: Point;Expression(H)=(x^2=4*y);Focus(H)=Q',QUERY)
    a=next(a for a in enumerate_actions(s,9,'extract_parameters') if a.curve=='G')
    assert BoundApplicator().apply(s,a).status=='applied'
    assert set(s.coordinates)=={'F'}


@pytest.mark.parametrize('facts',[FACTS.replace('G: Parabola','G: Ellipse'),
                                  FACTS.replace('Focus(G)=F','Focus(G)=missing')])
def test_type_rejection(facts):
    assert solve_directrix_alias_distance_slice(facts,QUERY).status=='failed'


def test_symbolic_focus_not_committed():
    s=TransitionState.from_facts(FACTS.replace('y=4*x^2','x^2=a*y')+';a: Number;a>0',QUERY)
    before=deepcopy(s)
    assert BoundApplicator().apply(s,enumerate_actions(s,9,'extract_parameters')[0]).status=='undetermined'
    assert s==before
