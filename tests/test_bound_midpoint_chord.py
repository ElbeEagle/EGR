from copy import deepcopy
from dataclasses import replace
import json
from pathlib import Path
import pytest
import sympy as sp
from src.reasoning.bound_slice import solve_midpoint_chord_slice
from src.state.transition_state import TransitionState
from src.theorems.bound_application import BoundApplicator, enumerate_actions

FACTS = 'l: Line;G: Ellipse;Expression(G)=(x^2/4+y^2/16=1);Coordinate(MidPoint(InterceptChord(l,G)))=(1/2,1)'
QUERY = 'Expression(l)'


def test_original_initial_state_and_end_to_end():
    row = next(r for r in json.loads(Path('data/train_with_models_v3.json').read_text()) if r['id']==4795)
    s = TransitionState.from_facts(row['fact_expressions'], row['query_expressions'])
    assert len(s.chords)==len(s.chord_endpoint_pairs)==len(s.chord_midpoints)==1
    assert not s.coordinates and not s.properties and not s.intersection_reductions and s.revision==0
    before=deepcopy(s)
    assert s.extract_answer() is None and s==before
    r=solve_midpoint_chord_slice(row['fact_expressions'],row['query_expressions'])
    assert r.status=='solved',r.diagnostic
    assert [t.action.model_id for t in r.transitions]==[4,40]
    x,y=r.state.symbols['x'],r.state.symbols['y']
    assert sp.expand(2*r.answer-(2*x+y-2))==0
    curve=next(f.expression for f in r.state.equations.values() if f.owner=='G')
    # Independent verification only: runtime never generates endpoint coordinates.
    points=sp.solve([curve,r.answer],(x,y))
    assert len(points)==2 and points[0]!=points[1]
    assert all(sp.simplify((points[0][i]+points[1][i])/2-v)==0 for i,v in enumerate((sp.Rational(1,2),1)))
    assert not r.state.coordinates and not r.state.intersection_reductions
    before=deepcopy(r.state)
    assert r.state.extract_answer()==r.answer and r.state==before
    assert BoundApplicator().apply(r.state,r.transitions[-1].action).status=='no_op' and r.state==before


@pytest.mark.parametrize('equation,midpoint,standard,answer',[
    ('x^2/16+y^2/4=1','1,1/2',3,'x+2*y-2'),
    ('x^2/4+y^2/16=1','1,0',4,'x-1'),
    ('x^2/4+y^2/16=1','0,1',4,'y-1'),
    ('4*x^2+y^2=16','1/2,1',4,'x+y/2-1')])
def test_directions_and_scaled_equation(equation,midpoint,standard,answer):
    r=solve_midpoint_chord_slice(FACTS.replace('x^2/4+y^2/16=1',equation).replace('(1/2,1)',f'({midpoint})'),QUERY)
    assert r.status=='solved',r.diagnostic
    assert r.transitions[0].action.model_id==standard
    assert sp.simplify(r.answer-sp.sympify(answer,locals=r.state.symbols))==0


@pytest.mark.parametrize('midpoint,status',[('0,0','undetermined'),('2,0','conflict'),('3,0','conflict')])
def test_degenerate_midpoints(midpoint,status):
    r=solve_midpoint_chord_slice(FACTS.replace('(1/2,1)',f'({midpoint})'),QUERY)
    assert r.status==status and r.answer is None
    assert r.state.revision==1 and not any(f.owner=='l' for f in r.state.equations.values())


def test_source_merge_and_input_conflict():
    fact=FACTS.split(';')[-1]
    s=TransitionState.from_facts(FACTS+';'+fact,QUERY)
    assert len(s.chords)==1 and len(next(iter(s.chords.values())).sources)==2
    with pytest.raises(ValueError,match='Conflicting midpoint'):
        TransitionState.from_facts(FACTS+';'+fact.replace('(1/2,1)','(1,1)'),QUERY)


def test_missing_parameters_and_pair():
    s=TransitionState.from_facts(FACTS,QUERY);a=enumerate_actions(s,40)[0];before=deepcopy(s)
    assert BoundApplicator().apply(s,a).status=='inapplicable' and s==before
    r=solve_midpoint_chord_slice(FACTS,QUERY);r.state.chord_endpoint_pairs.clear();before=deepcopy(r.state)
    assert BoundApplicator().apply(r.state,r.transitions[-1].action).status=='inapplicable' and r.state==before


@pytest.mark.parametrize('change',[{'line':'G'},{'curve':'l'},{'relation_id':'bad'},{'mode':'bad'}, {'point':'A'}, {'equation_id':'bad'}])
def test_wrong_bindings(change):
    r=solve_midpoint_chord_slice(FACTS,QUERY);before=deepcopy(r.state)
    assert BoundApplicator().apply(r.state,replace(r.transitions[-1].action,**change)).status=='inapplicable'
    assert r.state==before


@pytest.mark.parametrize('line,status',[('4*x+2*y=4','solved'),('x+y=1','conflict'),('x^2+y=1','conflict')])
def test_existing_line_crosscheck(line,status):
    r=solve_midpoint_chord_slice(FACTS+f';Expression(l)=({line})',QUERY)
    assert r.status==status,r.diagnostic
    assert len([f for f in r.state.equations.values() if f.owner=='l'])==1
    if status!='solved': assert not any(k[0].startswith('@chord') for k in r.state.properties)


def test_output_conflict_rollback_and_query_isolation():
    r=solve_midpoint_chord_slice(FACTS,QUERY);s=r.state
    key=next(k for k in s.properties if k[1]=='normal_x');s.properties[key]=sp.Integer(99);before=deepcopy(s)
    assert BoundApplicator().apply(s,r.transitions[-1].action).status=='conflict' and s==before
    s.query=replace(s.query,line='other');before=deepcopy(s)
    assert s.extract_answer() is None and s==before


def test_symbolic_midpoint_is_explicitly_rejected():
    with pytest.raises(ValueError,match='numeric'):
        TransitionState.from_facts(FACTS.replace('l: Line','t: Real;l: Line').replace('(1/2,1)','(t,1)'),QUERY)


def test_chord_identity_is_scoped_by_both_objects():
    s=TransitionState.from_facts(FACTS+';J: Ellipse;Expression(J)=(x^2/9+y^2/4=1);Coordinate(MidPoint(InterceptChord(l,J)))=(1,0)',QUERY)
    assert len(s.chords)==2 and len(s.chord_endpoint_pairs)==2
    assert solve_midpoint_chord_slice(FACTS+';h: Line','Expression(h)').status=='undetermined'
