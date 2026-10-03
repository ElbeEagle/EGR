from copy import deepcopy
from dataclasses import replace
import json
from pathlib import Path
import pytest
import sympy as sp
from src.state.transition_state import TransitionState, ChordLengthQuery
from src.theorems.bound_application import BoundApplicator, enumerate_actions
from src.reasoning.bound_slice import solve_chord_length_slice

FACTS = 'G: Parabola;H: Line;Expression(G)=(y^2=4*x);Expression(H)=(y=x-1)'
QUERY = 'Length(InterceptChord(H,G))'


def prepared():
    s = TransitionState.from_facts(FACTS, QUERY)
    assert BoundApplicator().apply(s, enumerate_actions(s,78)[0]).status == 'applied'
    return s


def test_original_and_readonly_query():
    row = next(r for r in json.loads(Path('data/train_with_models_v3.json').read_text()) if r['id']==6347)
    r = solve_chord_length_slice(row['fact_expressions'],row['query_expressions'])
    assert r.status == 'solved' and r.answer == 8
    assert [t.action.model_id for t in r.transitions] == [78,42,43,50]
    assert not r.state.coordinates and not r.state.values
    key, = r.state.intersection_reductions
    assert r.state.properties[(key,'root_sum')] == 4
    assert r.state.properties[(key,'root_product')] == -4
    assert r.state.properties[(key,'distinct_real_roots')] == 2
    assert f'property:{key}:root_sum' in r.transitions[-1].read_facts
    before = deepcopy(r.state)
    assert r.state.extract_answer()==8 and r.state==before
    for t in r.transitions:
        assert BoundApplicator().apply(r.state,t.action).status == 'no_op'
    assert r.state==before


def test_missing_relations_and_reverse_order():
    s=prepared(); app=BoundApplicator(); action=enumerate_actions(s,50)[0]
    for mid in (43,42):
        before=deepcopy(s)
        assert app.apply(s,action).status=='inapplicable' and s==before
        assert s.extract_answer() is None
        assert app.apply(s,enumerate_actions(s,mid)[0]).status=='applied'
    assert app.apply(s,action).status=='applied' and s.extract_answer()==8


@pytest.mark.parametrize('curve,line,expected',[
    ('y^2=4*x','x=1',4), ('y^2=-4*x','x=-1',4),
    ('x^2=4*y','y=1',4), ('x^2=-4*y','y=-1',4),
    ('y^2=4*x','y=2*x-1',sp.sqrt(15)),
])
def test_independent_coordinate_distance(curve,line,expected):
    r=solve_chord_length_slice(FACTS.replace('y^2=4*x',curve).replace('y=x-1',line),QUERY)
    assert r.status=='solved' and sp.simplify(r.answer-expected)==0
    s=r.state;x,y=s.symbols['x'],s.symbols['y']
    points=sp.solve([f.expression for f in s.equations.values()],(x,y))
    oracle=sp.sqrt(sum((a-b)**2 for a,b in zip(*points)))
    assert sp.simplify(r.answer-oracle)==0


@pytest.mark.parametrize('line,count',[('x=0',1),('x=-1',0)])
def test_no_ordinary_chord_for_tangent_or_no_real_roots(line,count):
    r=solve_chord_length_slice(FACTS.replace('y=x-1',line),QUERY)
    assert r.status=='inapplicable' and r.answer is None
    key,=r.state.intersection_reductions
    assert r.state.properties[(key,'distinct_real_roots')]==count
    assert (key,'root_sum') in r.state.properties and (key,'root_product') in r.state.properties
    assert r.transitions[-1].action.model_id==50


def test_linear_reduction_has_no_quadratic_relations():
    r=solve_chord_length_slice(FACTS.replace('y=x-1','y=1'),QUERY)
    assert r.status=='inapplicable' and r.answer is None
    assert r.transitions[-1].action.model_id==42 and not r.state.properties


@pytest.mark.parametrize('mid',[42,43,50])
@pytest.mark.parametrize('change',[{'relation_id':'bad'},{'line':'G'},{'point':'P'},{'mode':'bad'}])
def test_invalid_binding_rollback(mid,change):
    s=prepared();a=replace(enumerate_actions(s,mid)[0],**change);before=deepcopy(s)
    assert BoundApplicator().apply(s,a).status=='inapplicable' and s==before


@pytest.mark.parametrize('name',['root_sum','root_product','discriminant','chord_length'])
def test_conflict_rollback(name):
    r=solve_chord_length_slice(FACTS,QUERY);s=r.state;key,=s.intersection_reductions
    s.properties[(key,name)]=sp.Integer(999)
    before=deepcopy(s)
    assert BoundApplicator().apply(s,enumerate_actions(s,50)[0]).status=='conflict' and s==before


def test_line_isolation_and_ambiguous_query():
    s=TransitionState.from_facts(FACTS+';J: Line;Expression(J)=(x=1)',QUERY)
    app=BoundApplicator()
    for mid in (78,42,43,50):
        for a in enumerate_actions(s,mid): assert app.apply(s,a).status=='applied'
    assert s.extract_answer()==8
    s.query=ChordLengthQuery('J','G');assert s.extract_answer()==4
    f=s.equations['f3'];s.equations['other']=replace(f,fact_id='other')
    s.query=ChordLengthQuery('H','G');assert s.extract_answer() is None
