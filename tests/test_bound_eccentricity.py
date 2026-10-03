"""Forward RM13 contracts and four original dataset cases."""
from copy import deepcopy
from dataclasses import replace
import json
from pathlib import Path
import sympy as sp
import pytest
from src.state.transition_state import TransitionState,EccentricityQuery
from src.theorems.bound_application import BoundApplicator,BoundAction,enumerate_actions
from src.reasoning.bound_slice import solve_eccentricity_slice

FACTS='G: Ellipse;Expression(G)=(x^2/4+y^2=1)'


def prepared():
    s=TransitionState.from_facts(FACTS,'Eccentricity(G)');app=BoundApplicator()
    app.apply(s,BoundAction(3,'extract_parameters','G','f1'))
    app.apply(s,BoundAction(11,'derive_c_sq','G','f1'))
    return s,app,enumerate_actions(s,13)[0]


@pytest.mark.parametrize('pid,path,answer',[(5988,[3,11,13],sp.sqrt(3)/2),
    (7488,[4,11,13],sp.sqrt(2)/2),(1586,[5,12,13],sp.sqrt(5)/2),(4528,[6,12,13],2)])
def test_original_cases(pid,path,answer):
    row=next(r for r in json.loads(Path('data/train_with_models_v3.json').read_text()) if r['id']==pid)
    result=solve_eccentricity_slice(row['fact_expressions'],row['query_expressions'])
    assert result.status=='solved' and result.answer==answer
    assert [t.action.model_id for t in result.transitions]==path
    t=result.transitions[-1];curve=t.action.curve
    assert set(t.delta['properties'])=={(curve,'eccentricity')} and not t.delta['values']
    assert f'property:{curve}:c_sq' in t.read_facts
    before=deepcopy(result.state)
    assert BoundApplicator().apply(result.state,t.action).status=='no_op' and result.state==before


def test_missing_c_no_hidden_relation_and_read_only_query():
    s,app,a=prepared();del s.properties['G','c_sq'];before=deepcopy(s)
    assert s.extract_answer() is None and s==before
    assert app.apply(s,a).status=='inapplicable' and s==before
    app.apply(s,BoundAction(11,'derive_c_sq','G','f1'))
    assert s.extract_answer() is None
    assert app.apply(s,a).status=='applied' and s.extract_answer()==sp.sqrt(3)/2


@pytest.mark.parametrize('key,value',[('a_sq',0),('b_sq',-1),('c_sq',0),('c_sq',-3),('c_sq',4)])
def test_corrupt_parameters_rollback(key,value):
    s,app,a=prepared();s.properties['G',key]=sp.Integer(value);before=deepcopy(s)
    assert app.apply(s,a).status=='conflict' and s==before


@pytest.mark.parametrize('change',[{'curve':'H'},{'equation_id':'bad'},{'line':'L'},
                                  {'mode':'inverse'},{'point_role':'focus'}])
def test_binding_mode_guard(change):
    s,app,a=prepared();before=deepcopy(s)
    assert app.apply(s,replace(a,**change)).status=='inapplicable' and s==before


def test_frame_and_output_conflicts():
    s,app,a=prepared();s.frames['G']=replace(s.frames['G'],axis='y');before=deepcopy(s)
    assert app.apply(s,a).status=='inapplicable' and s==before
    s,app,a=prepared();s.properties['G','eccentricity']=sp.Integer(2);before=deepcopy(s)
    assert app.apply(s,a).status=='conflict' and s==before


def test_missing_frame():
    s,app,a=prepared();s.frames.clear();before=deepcopy(s)
    assert app.apply(s,a).status=='inapplicable' and s==before


def test_query_isolation():
    facts=FACTS+';H: Hyperbola;Expression(H)=(x^2/4-y^2=1)'
    r=solve_eccentricity_slice(facts,'Eccentricity(H)')
    assert r.status=='solved' and r.answer==sp.sqrt(5)/2
    assert all(k[0]=='H' for k in r.state.properties)
    r.state.query=EccentricityQuery('G');assert r.state.extract_answer() is None


def test_numeric_scope_and_circle():
    s=TransitionState.from_facts('G: Ellipse;t: Number;t>1;Expression(G)=(x^2/t+y^2=1)','Eccentricity(G)')
    app=BoundApplicator()
    assert app.apply(s,BoundAction(3,'extract_parameters','G','f3')).status=='applied'
    assert app.apply(s,BoundAction(11,'derive_c_sq','G','f3')).status=='applied'
    before=deepcopy(s)
    assert app.apply(s,enumerate_actions(s,13)[0]).status=='undetermined' and s==before
    r=solve_eccentricity_slice('G: Ellipse;Expression(G)=(x^2+y^2=1)','Eccentricity(G)')
    assert r.status!='solved'


def test_duplicate_equations_not_selected():
    r=solve_eccentricity_slice(FACTS+';Expression(G)=(x^2/4+y^2=1)','Eccentricity(G)')
    assert r.status=='undetermined' and not r.state.history
