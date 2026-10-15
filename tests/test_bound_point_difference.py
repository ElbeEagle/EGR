from copy import deepcopy
from dataclasses import replace
import json
from pathlib import Path
import pytest
import sympy as sp
from src.reasoning.bound_slice import solve_point_difference_slice, solve_midpoint_chord_slice
from src.state.transition_state import TransitionState
from src.theorems.bound_application import BoundApplicator, enumerate_actions

FACTS='l: Line;G: Ellipse;Expression(G)=(x^2/4+y^2/16=1);Coordinate(MidPoint(InterceptChord(l,G)))=(1/2,1)'
QUERY='Expression(l)'


def test_original_independent_chain():
    row=next(r for r in json.loads(Path('data/train_with_models_v3.json').read_text()) if r['id']==4795)
    r=solve_point_difference_slice(row['fact_expressions'],row['query_expressions'])
    assert r.status=='solved',r.diagnostic
    assert [t.action.model_id for t in r.transitions]==[4,54,45]
    s=r.state;pair=next(iter(s.chord_endpoint_pairs))
    assert (s.properties[pair,'x_sum'],s.properties[pair,'y_sum'])==(1,2)
    assert sp.expand(2*r.answer-(2*s.symbols['x']+s.symbols['y']-2))==0
    assert f'property:{pair}:x_sum' in r.transitions[-1].read_facts
    assert r.transitions[-1].operations[0]['difference_coefficients']==(sp.Rational(1,4),sp.Rational(1,8))
    assert not s.coordinates and not s.intersection_reductions
    before=deepcopy(s);assert s.extract_answer()==r.answer and s==before
    for a in (r.transitions[1].action,r.transitions[2].action,enumerate_actions(s,40)[0]):
        assert BoundApplicator().apply(s,a).status=='no_op' and s==before


def test_rm54_only_algebra_no_standard_or_line():
    s=TransitionState.from_facts(FACTS,QUERY)
    assert BoundApplicator().apply(s,enumerate_actions(s,54)[0]).status=='applied'
    assert len(s.properties)==2 and not s.frames and s.extract_answer() is None
    before=deepcopy(s)
    assert BoundApplicator().apply(s,enumerate_actions(s,45)[0]).status=='inapplicable' and s==before


def test_rm40_does_not_supply_endpoint_sums():
    r=solve_midpoint_chord_slice(FACTS,QUERY);s=r.state;before=deepcopy(s)
    assert BoundApplicator().apply(s,enumerate_actions(s,45)[0]).status=='inapplicable' and s==before
    assert BoundApplicator().apply(s,enumerate_actions(s,54)[0]).status=='applied'
    before=deepcopy(s)
    assert BoundApplicator().apply(s,enumerate_actions(s,45)[0]).status=='no_op' and s==before


@pytest.mark.parametrize('point,status',[('0,0','undetermined'),('2,0','conflict'),('3,0','conflict')])
def test_rm54_does_not_assert_chord_qualification(point,status):
    r=solve_point_difference_slice(FACTS.replace('(1/2,1)',f'({point})'),QUERY)
    assert r.status==status and r.answer is None
    assert [t.status for t in r.transitions]==['applied','applied',status]
    assert len(r.state.properties)==4  # two standard parameters and two sums
    assert not any(f.owner=='l' for f in r.state.equations.values())


@pytest.mark.parametrize('equation,point,answer',[
 ('x^2/16+y^2/4=1','1,1/2','x+2*y-2'),
 ('x^2/4+y^2/16=1','0,1','y-1'),
 ('x^2/4+y^2/16=1','1,0','x-1')])
def test_axis_and_zero_components(equation,point,answer):
    r=solve_point_difference_slice(FACTS.replace('x^2/4+y^2/16=1',equation).replace('(1/2,1)',f'({point})'),QUERY)
    assert r.status=='solved'
    assert sp.expand(r.answer-sp.sympify(answer,locals=r.state.symbols))==0


@pytest.mark.parametrize('damage,status', [('value','conflict'),('missing','inapplicable'),('source','inapplicable'),('other_pair','inapplicable')])
def test_wrong_or_missing_sums_rollback(damage,status):
    r=solve_point_difference_slice(FACTS,QUERY);s=r.state;pair=next(iter(s.chord_endpoint_pairs));key=(pair,'x_sum')
    if damage=='value':s.properties[key]=sp.Integer(99)
    elif damage=='missing':del s.properties[key]
    elif damage=='source':s.provenance[f'property:{pair}:x_sum']=('wrong',)
    else:s.properties['other','x_sum']=s.properties.pop(key)
    before=deepcopy(s)
    assert BoundApplicator().apply(s,r.transitions[-1].action).status==status and s==before


@pytest.mark.parametrize('mid,change',[(54,{'relation_id':'bad'}),(45,{'line':'G'}),(54,{'point':'A'}),(45,{'mode':'bad'})])
def test_wrong_bindings(mid,change):
    r=solve_point_difference_slice(FACTS,QUERY);s=r.state;before=deepcopy(s)
    assert BoundApplicator().apply(s,replace(enumerate_actions(s,mid)[0],**change)).status=='inapplicable' and s==before


def test_rm54_conflict_does_not_partially_write():
    s=TransitionState.from_facts(FACTS,QUERY);pair=next(iter(s.chord_endpoint_pairs))
    s.properties[pair,'y_sum']=sp.Integer(99);before=deepcopy(s)
    assert BoundApplicator().apply(s,enumerate_actions(s,54)[0]).status=='conflict' and s==before


@pytest.mark.parametrize('line,status',[('4*x+2*y=4','solved'),('x+y=1','conflict')])
def test_existing_line_preserved(line,status):
    r=solve_point_difference_slice(FACTS+f';Expression(l)=({line})',QUERY)
    assert r.status==status
    assert len([f for f in r.state.equations.values() if f.owner=='l'])==1
    if status=='conflict':assert not any(k[1]=='normal_x' for k in r.state.properties)
