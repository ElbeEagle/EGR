from copy import deepcopy
from dataclasses import replace
import json
from pathlib import Path
import pytest
import sympy as sp
from src.state.transition_state import TransitionState
from src.theorems.bound_application import BoundApplicator, enumerate_actions
from src.reasoning.bound_slice import solve_focal_chord_slice,solve_chord_length_slice

FACTS='G: Parabola;H: Line;Expression(G)=(y^2=4*x);Expression(H)=(y=x-1)'
QUERY='Length(InterceptChord(H,G))'


def test_original_two_paths_and_no_product():
    row=next(r for r in json.loads(Path('data/train_with_models_v3.json').read_text()) if r['id']==6347)
    r=solve_focal_chord_slice(row['fact_expressions'],row['query_expressions'])
    assert r.status=='solved' and r.answer==8
    assert [t.action.model_id for t in r.transitions]==[7,78,42,33]
    f,=r.state.intersection_reductions.values()
    assert (f.fact_id,'root_product') not in r.state.properties
    assert r.state.properties[(f.fact_id,'focus_on_line')]==1
    assert r.transitions[-1].operations[0]['residual']==0
    assert solve_chord_length_slice(row['fact_expressions'],row['query_expressions']).answer==8
    before=deepcopy(r.state)
    assert BoundApplicator().apply(r.state,r.transitions[-1].action).status=='no_op' and r.state==before


@pytest.mark.parametrize('curve,line', [('y^2=4*x','x=1'),('y^2=-4*x','x=-1'),
                                      ('x^2=4*y','y=1'),('x^2=-4*y','y=-1')])
def test_four_directions_and_independent_distance(curve,line):
    facts=FACTS.replace('y^2=4*x',curve).replace('y=x-1',line)
    r=solve_focal_chord_slice(facts,QUERY);assert r.status=='solved' and r.answer==4
    s=r.state;x,y=s.symbols['x'],s.symbols['y']
    pts=sp.solve([f.expression for f in s.equations.values()],(x,y))
    assert sp.simplify(sp.sqrt(sum((a-b)**2 for a,b in zip(*pts)))-r.answer)==0


@pytest.mark.parametrize('line',['y=x','y=x-2','y=0'])
def test_not_a_finite_focal_chord(line):
    r=solve_focal_chord_slice(FACTS.replace('y=x-1',line),QUERY)
    assert r.status=='inapplicable' and r.answer is None
    assert not any(k[1]=='focus_on_line' for k in r.state.properties)


@pytest.mark.parametrize('missing',['frame','focus','root_sum'])
def test_missing_inputs_no_hidden_derivation(missing):
    s=TransitionState.from_facts(FACTS,QUERY);app=BoundApplicator()
    for mid in (7,78,42):assert app.apply(s,enumerate_actions(s,mid)[0]).status=='applied'
    if missing=='frame':s.frames.clear()
    elif missing=='focus':del s.properties[('G','focus_x')]
    else:del s.properties[(next(iter(s.intersection_reductions)),'root_sum')]
    before=deepcopy(s)
    assert app.apply(s,enumerate_actions(s,33)[0]).status=='inapplicable' and s==before


@pytest.mark.parametrize('change',[{'relation_id':'bad'},{'line':'G'},{'mode':'bad'}])
def test_wrong_bindings(change):
    r=solve_focal_chord_slice(FACTS,QUERY);before=deepcopy(r.state)
    assert BoundApplicator().apply(r.state,replace(r.transitions[-1].action,**change)).status=='inapplicable'
    assert r.state==before


def test_conflicting_length_rolls_back_focus_marker():
    s=TransitionState.from_facts(FACTS,QUERY);app=BoundApplicator()
    for mid in (7,78,42):assert app.apply(s,enumerate_actions(s,mid)[0]).status=='applied'
    key=next(iter(s.intersection_reductions));s.properties[(key,'chord_length')]=sp.S.One
    before=deepcopy(s)
    assert app.apply(s,enumerate_actions(s,33)[0]).status=='conflict' and s==before
