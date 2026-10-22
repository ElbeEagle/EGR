from copy import deepcopy
from dataclasses import replace
import json
from pathlib import Path
import pytest
import sympy as sp
from src.state.transition_state import TransitionState
from src.reasoning.bound_slice import solve_midpoint_chord_slice,solve_point_difference_slice
from src.theorems.bound_application import BoundApplicator,enumerate_actions

FACTS='G: Ellipse;H: LineSegment;M: Point;Expression(G)=(x^2/2+y^2/4=1);IsChordOf(H,G);MidPoint(H)=M;Coordinate(M)=(1,1)'
QUERY='Expression(OverlappingLine(H))'
SOLVERS=[solve_midpoint_chord_slice,solve_point_difference_slice]


@pytest.mark.parametrize('pid,standard,expected',[(2227,4,'x+y/2-3/2'),(2324,3,'x+9*y/5-14/5'),(3337,3,'x+2*y-2')])
@pytest.mark.parametrize('solve',SOLVERS)
def test_original_two_paths_and_sources(pid,standard,expected,solve):
    row=next(r for r in json.loads(Path('data/train_with_models_v3.json').read_text()) if r['id']==pid)
    s=TransitionState.from_facts(row['fact_expressions'],row['query_expressions'])
    alias=next(iter(s.midpoint_aliases.values()));mid=s.chord_midpoints[alias.chord_id]
    coord=s.coordinates[alias.point];relation=s.segment_chords[alias.segment]
    assert alias.coordinate_id==coord.fact_id and alias.xy==coord.xy==mid.xy
    assert set((*alias.sources,coord.fact_id))==set(mid.sources)
    assert set(relation.sources).isdisjoint(mid.sources)
    assert len(s.coordinates)==1 and not s.properties and s.revision==0
    before=deepcopy(s);assert s.extract_answer() is None and s==before
    r=solve(row['fact_expressions'],row['query_expressions']);assert r.status=='solved',r.diagnostic
    assert [t.action.model_id for t in r.transitions] in ([standard,40],[standard,54,45])
    assert sp.simplify(r.answer-sp.sympify(expected,locals=s.symbols))==0
    for step in r.transitions[1:]:assert set((*relation.sources,*alias.sources,coord.fact_id)).issubset(step.read_facts)
    before=deepcopy(r.state)
    for step in r.transitions[1:]:assert BoundApplicator().apply(r.state,step.action).status=='no_op' and r.state==before


@pytest.mark.parametrize('facts',[
 ';'.join(reversed(FACTS.split(';'))), FACTS+';MidPoint(H)=M',
 FACTS+';Coordinate(MidPoint(H))=(1,1)',
 FACTS.replace('Coordinate(M)=(1,1)','Coordinate(M)=(2/2,1)')])
def test_order_duplicates_and_composite_merge(facts):
    r=solve_point_difference_slice(facts,QUERY);assert r.status=='solved',r.diagnostic
    assert len(r.state.midpoint_aliases)==len(r.state.chords)==1


@pytest.mark.parametrize('remove,status',[
 ('Coordinate(M)=(1,1)','inapplicable'),
 ('symbolic','undetermined')])
@pytest.mark.parametrize('solve',SOLVERS)
def test_missing_and_symbolic_coordinate(remove,status,solve):
    facts=FACTS.replace('Coordinate(M)=(1,1)','t: Real;Coordinate(M)=(t,1)') if remove=='symbolic' else FACTS.replace(remove,'')
    r=solve(facts,QUERY);assert r.status==status,r.diagnostic
    assert r.answer is None and r.state.midpoint_aliases and not r.state.chord_midpoints
    assert not any(f.role=='line' for f in r.state.equations.values())


@pytest.mark.parametrize('extra',[
 ';N: Point;Coordinate(N)=(1,1);MidPoint(H)=N',
 ';Coordinate(MidPoint(H))=(0,1)', ';Coordinate(M)=(1,1)'])
def test_conflicting_or_duplicate_input(extra):
    with pytest.raises(ValueError):TransitionState.from_facts(FACTS+extra,QUERY)


@pytest.mark.parametrize('facts',[
 FACTS.replace('M: Point;',''),FACTS.replace('IsChordOf(H,G);',''),
 FACTS.replace('MidPoint(H)=M','MidPoint(LineSegmentOf(A,B))=M;A: Point;B: Point')])
def test_invalid_or_deferred_alias(facts):
    with pytest.raises(ValueError):TransitionState.from_facts(facts,QUERY)


@pytest.mark.parametrize('damage',['xy','id','point','missing','alias_missing','alias_point','alias_segment','midpoint','sources'])
@pytest.mark.parametrize('model',[40,54,45])
def test_stale_snapshot_and_binding_rollback(damage,model):
    r=solve_point_difference_slice(FACTS,QUERY);s=r.state;key=next(iter(s.midpoint_aliases));alias=s.midpoint_aliases[key]
    if damage=='xy':s.coordinates['M']=replace(s.coordinates['M'],xy=(sp.Integer(0),sp.Integer(1)))
    elif damage=='id':s.coordinates['M']=replace(s.coordinates['M'],fact_id='changed')
    elif damage=='point':s.coordinates['M']=replace(s.coordinates['M'],point='N')
    elif damage=='missing':s.coordinates.clear()
    elif damage=='alias_missing':s.midpoint_aliases.clear()
    elif damage=='alias_point':s.midpoint_aliases[key]=replace(alias,point='N')
    elif damage=='alias_segment':s.midpoint_aliases[key]=replace(alias,segment='wrong')
    elif damage=='midpoint':s.chord_midpoints[key]=replace(s.chord_midpoints[key],xy=(sp.Integer(0),sp.Integer(1)))
    else:s.chord_midpoints[key]=replace(s.chord_midpoints[key],sources=alias.sources)
    before=deepcopy(s)
    assert BoundApplicator().apply(s,enumerate_actions(s,model)[0]).status in ('conflict','inapplicable')
    assert s==before


def test_shared_point_does_not_merge_chords():
    facts=FACTS+';K: LineSegment;IsChordOf(K,G);MidPoint(K)=M'
    r=solve_midpoint_chord_slice(facts,QUERY);assert r.status=='solved'
    assert len(r.state.chords)==len(r.state.midpoint_aliases)==2
    r.state.query=replace(r.state.query,line='@overlap:K');assert r.state.extract_answer() is None
