from copy import deepcopy
from dataclasses import replace
import json
from pathlib import Path
import pytest
import sympy as sp
from src.reasoning.bound_slice import solve_chord_length_slice
from src.state.transition_state import TransitionState
from src.theorems.bound_application import BoundApplicator, enumerate_actions

FACTS='G: Parabola;H: Line;Expression(G)=(y^2=4*x);Expression(H)=(y=x-1)'
QUERY='Length(InterceptChord(H,G))'


def prepared(facts=FACTS):
    s=TransitionState.from_facts(facts,QUERY)
    for a in enumerate_actions(s,78):
        assert BoundApplicator().apply(s,a).status=='applied'
    return s


@pytest.mark.parametrize('pid,expected',[(3057,sp.sqrt(15)),(6347,8)])
def test_real_cases(pid,expected):
    row=next(r for r in json.loads(Path('data/train_with_models_v3.json').read_text()) if r['id']==pid)
    r=solve_chord_length_slice(row['fact_expressions'],row['query_expressions'],joint_roots=True)
    old=solve_chord_length_slice(row['fact_expressions'],row['query_expressions'])
    assert r.status=='solved' and sp.simplify(r.answer-expected)==0 and r.answer==old.answer
    assert [t.action.model_id for t in r.transitions]==[78,41,50]
    assert r.state.properties==old.state.properties
    before=deepcopy(r.state)
    assert r.state.extract_answer()==expected and r.state==before
    assert BoundApplicator().apply(r.state,r.transitions[1].action).status=='no_op' and r.state==before
    key,=r.state.intersection_reductions
    for name in ('root_sum','root_product','discriminant','distinct_real_roots'):
        assert key in r.state.provenance[f'property:{key}:{name}']


@pytest.mark.parametrize('line,count',[('x=0',1),('x=-1',0)])
def test_no_real_chord(line,count):
    r=solve_chord_length_slice(FACTS.replace('y=x-1',line),QUERY,joint_roots=True)
    assert r.status=='inapplicable' and r.answer is None
    assert [t.status for t in r.transitions]==['applied','applied','inapplicable']
    key,=r.state.intersection_reductions
    assert r.state.properties[key,'distinct_real_roots']==count
    assert (key,'root_sum') in r.state.properties and (key,'root_product') in r.state.properties


def test_linear_reduction():
    r=solve_chord_length_slice(FACTS.replace('y=x-1','y=1'),QUERY,joint_roots=True)
    assert r.status=='inapplicable' and not r.state.properties
    assert r.transitions[-1].action.model_id==41


@pytest.mark.parametrize('poly',['0','1','y','y**3','y**2+k*y+1'])
def test_degenerate_or_symbolic_rejected(poly):
    s=prepared();key,=s.intersection_reductions;f=s.intersection_reductions[key]
    s.intersection_reductions[key]=replace(f,polynomial=sp.sympify(poly,locals={'y':f.variable,'k':sp.Symbol('k',real=True)}))
    before=deepcopy(s)
    assert BoundApplicator().apply(s,enumerate_actions(s,41)[0]).status in ('inapplicable','undetermined')
    assert s==before


@pytest.mark.parametrize('name',['root_sum','root_product','discriminant','distinct_real_roots'])
def test_partial_conflict_atomic(name):
    s=prepared();key,=s.intersection_reductions;s.properties[key,name]=sp.Integer(999)
    before=deepcopy(s)
    assert BoundApplicator().apply(s,enumerate_actions(s,41)[0]).status=='conflict' and s==before


@pytest.mark.parametrize('mid',[42,43])
def test_partial_completion(mid):
    s=prepared();app=BoundApplicator()
    assert app.apply(s,enumerate_actions(s,mid)[0]).status=='applied'
    assert app.apply(s,enumerate_actions(s,41)[0]).status=='applied'
    assert app.apply(s,enumerate_actions(s,50)[0]).status=='applied'
    assert s.extract_answer()==8


@pytest.mark.parametrize('change',[{'relation_id':'bad'},{'line':'G'},{'mode':'bad'},{'point':'P'}])
def test_bad_binding(change):
    s=prepared();before=deepcopy(s)
    assert BoundApplicator().apply(s,replace(enumerate_actions(s,41)[0],**change)).status=='inapplicable'
    assert s==before


def test_pair_isolation():
    s=prepared(FACTS+';J: Line;Expression(J)=(x=1)');app=BoundApplicator()
    actions=enumerate_actions(s,41);assert len(actions)==2
    assert app.apply(s,actions[0]).status=='applied'
    assert all(k[0]==actions[0].relation_id for k in s.properties)
    before=deepcopy(s)
    assert app.apply(s,replace(actions[0],relation_id=actions[1].relation_id)).status=='inapplicable' and s==before
    assert app.apply(s,actions[1]).status=='applied'
    assert len(s.properties)==8
