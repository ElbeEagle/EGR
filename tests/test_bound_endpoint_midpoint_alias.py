from copy import deepcopy
from dataclasses import replace
import json
from pathlib import Path
import pytest
import sympy as sp
from src.state.transition_state import TransitionState
from src.reasoning.bound_slice import solve_midpoint_chord_slice,solve_point_difference_slice
from src.theorems.bound_application import BoundApplicator,enumerate_actions

FACTS='l: Line;G: Ellipse;A: Point;B: Point;M: Point;Expression(G)=(x^2/4+y^2/9=1);Coordinate(M)=(1,1);PointOnCurve(M,l);Intersection(l,G)={A,B};MidPoint(LineSegmentOf(A,B))=M'
QUERY='Expression(l)'
SOLVERS=[solve_midpoint_chord_slice,solve_point_difference_slice]


@pytest.mark.parametrize('pid,standard,answer',[(2290,4,'x+4*y/9-13/9'),(4761,3,'x+2*y-2')])
@pytest.mark.parametrize('solve',SOLVERS)
def test_real_original_and_provenance(pid,standard,answer,solve):
    row=next(r for r in json.loads(Path('data/train_with_models_v3.json').read_text()) if r['id']==pid)
    s=TransitionState.from_facts(row['fact_expressions'],row['query_expressions']);a=next(iter(s.midpoint_aliases.values()))
    assert a.segment is None and a.endpoints==('A','B') and a.pair_id in s.chord_endpoint_pairs
    assert len(s.coordinates)==1 and not s.properties and s.revision==0
    before=deepcopy(s);assert s.extract_answer() is None and s==before
    r=solve(row['fact_expressions'],row['query_expressions']);assert r.status=='solved',r.diagnostic
    assert sp.simplify(r.answer-sp.sympify(answer,locals=s.symbols))==0
    assert [t.action.model_id for t in r.transitions] in ([standard,40],[standard,54,45])
    sources=(*s.chord_endpoint_names[a.pair_id].sources,*a.sources,a.coordinate_id)
    for t in r.transitions[1:]:assert set(sources).issubset(t.read_facts)
    before=deepcopy(r.state)
    for t in r.transitions[1:]:assert BoundApplicator().apply(r.state,t.action).status=='no_op' and r.state==before


@pytest.mark.parametrize('facts',[
 ';'.join(reversed(FACTS.split(';'))),
 FACTS.replace('Intersection(l,G)={A,B}','Intersection(G,l)={B,A}').replace('LineSegmentOf(A,B)','LineSegmentOf(B,A)'),
 FACTS+';MidPoint(LineSegmentOf(B,A))=M',
 FACTS+';Coordinate(MidPoint(LineSegmentOf(A,B)))=(1,1)'])
def test_order_and_merging(facts):
    r=solve_point_difference_slice(facts,QUERY);assert r.status=='solved',r.diagnostic
    assert len(r.state.chords)==len(r.state.midpoint_aliases)==1


@pytest.mark.parametrize('facts',[
 FACTS.replace('Intersection(l,G)={A,B};',''),
 FACTS.replace('M: Point;',''),
 FACTS.replace('LineSegmentOf(A,B)','LineSegmentOf(A,A)'),
 FACTS.replace('LineSegmentOf(A,B))=M','LineSegmentOf(A,B))=A'),
 FACTS+';h: Line;Intersection(h,G)={A,B}',
 FACTS+';N: Point;MidPoint(LineSegmentOf(A,B))=N',
 FACTS+';Coordinate(MidPoint(LineSegmentOf(A,B)))=(0,0)'])
def test_invalid_binding_or_conflict(facts):
    with pytest.raises(ValueError):TransitionState.from_facts(facts,QUERY)


@pytest.mark.parametrize('replacement,status',[('', 'inapplicable'),('t: Real;Coordinate(M)=(t,1)','undetermined')])
def test_missing_or_symbolic(replacement,status):
    r=solve_point_difference_slice(FACTS.replace('Coordinate(M)=(1,1)',replacement),QUERY)
    assert r.status==status and r.answer is None and not r.state.chord_midpoints


@pytest.mark.parametrize('damage',['pair','endpoints','names','coordinate','coordinate_id','segment'])
@pytest.mark.parametrize('model',[40,54,45])
def test_stale_identity_and_coordinate_rejected(damage,model):
    r=solve_point_difference_slice(FACTS,QUERY);s=r.state;k=next(iter(s.midpoint_aliases));a=s.midpoint_aliases[k]
    if damage=='pair':s.midpoint_aliases[k]=replace(a,pair_id='wrong')
    elif damage=='endpoints':s.midpoint_aliases[k]=replace(a,endpoints=('A','C'))
    elif damage=='names':s.chord_endpoint_names.clear()
    elif damage=='coordinate':s.coordinates['M']=replace(s.coordinates['M'],xy=(sp.S.Zero,sp.S.One))
    elif damage=='coordinate_id':s.coordinates['M']=replace(s.coordinates['M'],fact_id='changed')
    else:s.midpoint_aliases[k]=replace(a,segment='wrong')
    before=deepcopy(s)
    assert BoundApplicator().apply(s,enumerate_actions(s,model)[0]).status in ('inapplicable','conflict')
    assert s==before


def test_existing_endpoint_coordinates_still_checked():
    r=solve_midpoint_chord_slice(FACTS+';Coordinate(A)=(0,0)',QUERY)
    assert r.status=='conflict' and r.answer is None
    assert not any(f.owner=='l' for f in r.state.equations.values())


def test_same_midpoint_two_chords_not_merged():
    facts=FACTS+';h: Line;C: Point;D: Point;Intersection(h,G)={C,D};MidPoint(LineSegmentOf(C,D))=M'
    r=solve_point_difference_slice(facts,QUERY);assert r.status=='solved'
    assert len(r.state.chords)==len(r.state.midpoint_aliases)==2
    r.state.query=replace(r.state.query,line='h');assert r.state.extract_answer() is None
