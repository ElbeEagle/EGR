"""Known intersection parsing and parameter subchains, not ID7260 final solving."""
import json
from pathlib import Path
from copy import deepcopy
from dataclasses import replace
import pytest
import sympy as sp
from src.state.transition_state import TransitionState
from src.theorems.bound_application import BoundApplicator, enumerate_actions


def original():
    return next(r for r in json.loads(Path('data/train_with_models_v3.json').read_text()) if r['id']==7260)


@pytest.mark.parametrize('order',[(7,72),(72,7)])
def test_real_parameter_subchain(order):
    s=TransitionState.from_facts(original()['fact_expressions'],None)
    assert len(s.coordinates)==1 and len(s.incidences)==2 and not s.values
    assert s.query is None and s.extract_answer() is None
    point=next(iter(s.coordinates))
    assert point=='@intersection:f7'
    assert {i.curve for i in s.incidences.values()}=={'G','H'}
    for i in s.incidences.values():assert i.point==point and s.provenance[i.fact_id]==('f7',)
    app=BoundApplicator()
    for mid in order:
        action,=enumerate_actions(s,mid,'recover_from_point')
        t=app.apply(s,action)
        assert t.status=='applied',t.diagnostic
        assert 'f7' in t.read_facts
    assert s.values=={s.symbols['a']:2,s.symbols['p']:2}
    assert s.properties['G','focus_x']==1 and s.properties['H','slope']==-2
    assert s.extract_answer() is None
    before=deepcopy(s)
    for mid in order:assert app.apply(s,enumerate_actions(s,mid,'recover_from_point')[0]).status=='no_op'
    assert s==before


def case(eq='a*x+y-4=0',point='1,2',extra=''):
    return TransitionState.from_facts(f'H: Line;a: Number;Expression(H)=({eq});P: Point;Coordinate(P)=({point});PointOnCurve(P,H)'+extra,None)


@pytest.mark.parametrize('eq,point,extra,status',[
    ('a*x+y-4=0','1,2','','applied'),('y-a=0','0,2','','applied'),
    ('x-a=0','1,2','','inapplicable'),('x*y+a=0','1,2','','inapplicable'),
    ('a*x+y-2=0','0,2','','undetermined'),('a*x+y-4=0','0,2','','conflict'),
    ('a^2*x+y-6=0','1,2','','undetermined'),('a^2*x+y-6=0','1,2',';a>0','applied'),
    ('a*x+y-4=0','1,2',';a<0','conflict'),
    ('a*x+y-4=0','1,2',';p: Number;p>a','undetermined'),
    ('a*x+p*y-4=0','1,2',';p: Number;p>0','undetermined'),
    ('a*x+y-4=0','1,2',';p: Number;p>0','applied'),
])
def test_line_boundaries(eq,point,extra,status):
    s=case(eq,point,extra);before=deepcopy(s)
    t=BoundApplicator().apply(s,enumerate_actions(s,72)[0])
    assert t.status==status,t.diagnostic
    if status!='applied':assert s==before


def test_wrong_binding_and_existing_assignment_conflict():
    s=case();app=BoundApplicator();action,=enumerate_actions(s,72)
    for bad in [replace(action,relation_id='bad'),replace(action,line='G'),replace(action,coordinate_id='bad')]:
        before=deepcopy(s)
        assert app.apply(s,bad).status=='inapplicable' and s==before
    s.values[s.symbols['a']]=sp.Integer(3);before=deepcopy(s)
    assert app.apply(s,action).status=='conflict' and s==before


def test_witnesses_are_fact_scoped_and_typed():
    facts=original()['fact_expressions']
    s=TransitionState.from_facts(facts+';Coordinate(OneOf(Intersection(G,H)))=(2,3)',None)
    assert len(s.coordinates)==2 and len(s.incidences)==4
    with pytest.raises(ValueError):
        TransitionState.from_facts(facts.replace('Intersection(H, G)','Intersection(H, H)'),None)


def test_original_query_has_no_answer_before_execution():
    r=original()
    state = TransitionState.from_facts(r['fact_expressions'],r['query_expressions'])
    assert state.extract_answer() is None and not state.values
