from copy import deepcopy
from dataclasses import replace
import json
from pathlib import Path
import pytest
import sympy as sp
from src.state.transition_state import TransitionState
from src.reasoning.bound_slice import solve_midpoint_chord_slice,solve_point_difference_slice
from src.theorems.bound_application import BoundApplicator

FACTS='G: Ellipse;H: LineSegment;Expression(G)=(x^2/4+y^2/2=1);Coordinate(MidPoint(H))=(1,1);IsChordOf(H,G)'
QUERY='Expression(OverlappingLine(H))'
SOLVERS=[solve_midpoint_chord_slice,solve_point_difference_slice]


@pytest.mark.parametrize('solve',SOLVERS)
def test_real_initial_and_closure(solve):
    row=next(r for r in json.loads(Path('data/train_with_models_v3.json').read_text()) if r['id']==7439)
    s=TransitionState.from_facts(row['fact_expressions'],row['query_expressions'])
    assert s.entities['H']=='LineSegment' and s.entities['@overlap:H']=='Line'
    assert not s.coordinates and not s.properties and s.revision==0
    before=deepcopy(s);assert s.extract_answer() is None and s==before
    r=solve(row['fact_expressions'],row['query_expressions']);assert r.status=='solved',r.diagnostic
    x,y=s.symbols['x'],s.symbols['y'];assert sp.expand(r.answer-(x+2*y-3))==0
    assert [t.action.model_id for t in r.transitions] in ([3,40],[3,54,45])
    relation=s.segment_chords['H'];mid=next(iter(s.chord_midpoints.values()))
    assert set((*relation.sources,*mid.sources)).issubset(r.transitions[-1].read_facts)
    curve=next(f.expression for f in s.equations.values())
    points=sp.solve([curve,r.answer],(x,y));assert len(points)==2 and points[0]!=points[1]
    assert all(sp.simplify((points[0][i]+points[1][i])/2-1)==0 for i in range(2))
    before=deepcopy(r.state)
    assert BoundApplicator().apply(r.state,r.transitions[-1].action).status=='no_op' and r.state==before


@pytest.mark.parametrize('facts',[
 ';'.join(reversed(FACTS.split(';'))),FACTS+';IsChordOf(H,G)',
 FACTS.replace('IsChordOf(H,G)','IsChordOf(H,G)=True'),
 FACTS+';Coordinate(MidPoint(H))=(1,1)'])
def test_order_and_duplicates(facts):
    r=solve_point_difference_slice(facts,QUERY);assert r.status=='solved',r.diagnostic
    assert len(r.state.chords)==len(r.state.chord_endpoint_pairs)==len(r.state.segment_chords)==1


@pytest.mark.parametrize('facts,query',[
 (FACTS.replace(';IsChordOf(H,G)',''),QUERY),
 (FACTS.replace('H: LineSegment;',''),QUERY),
 (FACTS.replace('H: LineSegment','H: Line'),QUERY),
 (FACTS+';J: Ellipse;IsChordOf(H,J)',QUERY),
 (FACTS+';Coordinate(MidPoint(H))=(0,1)',QUERY),
 (FACTS, 'Expression(OverlappingLine(G))'),
 (FACTS.replace('IsChordOf(H,G)','IsChordOf(H,G)=False'),QUERY),
 (FACTS.replace('G: Ellipse','G: Parabola'),QUERY)])
def test_unsupported_or_conflicting_inputs(facts,query):
    with pytest.raises(ValueError):TransitionState.from_facts(facts,query)


@pytest.mark.parametrize('xy,status',[('0,0','undetermined'),('2,0','conflict'),('3,0','conflict')])
def test_degenerate_geometry(xy,status):
    r=solve_point_difference_slice(FACTS.replace('(1,1)',f'({xy})'),QUERY)
    assert r.status==status and r.answer is None
    assert not any(f.owner=='@overlap:H' for f in r.state.equations.values())


def test_two_segments_on_same_curve_stay_distinct():
    facts=FACTS+';K: LineSegment;IsChordOf(K,G);Coordinate(MidPoint(K))=(1,0)'
    r=solve_point_difference_slice(facts,'Expression(OverlappingLine(K))')
    assert r.status=='solved' and r.answer==r.state.symbols['x']-1
    assert len(r.state.chords)==2
    r.state.query=replace(r.state.query,line='@overlap:H');assert r.state.extract_answer() is None


def test_missing_midpoint_does_not_produce_answer():
    r=solve_midpoint_chord_slice(FACTS.replace('Coordinate(MidPoint(H))=(1,1);',''),QUERY)
    assert r.status=='inapplicable' and r.answer is None


@pytest.mark.parametrize('damage',['remove','curve'])
def test_bad_identity_does_not_mutate(damage):
    r=solve_point_difference_slice(FACTS,QUERY)
    if damage=='remove':r.state.segment_chords.clear()
    else:r.state.segment_chords['H']=replace(r.state.segment_chords['H'],curve='other')
    before=deepcopy(r.state)
    assert BoundApplicator().apply(r.state,r.transitions[-1].action).status=='inapplicable' and r.state==before
