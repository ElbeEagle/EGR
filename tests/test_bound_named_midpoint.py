from copy import deepcopy
import json
from pathlib import Path
import pytest
import sympy as sp
from src.state.transition_state import TransitionState
from src.reasoning.bound_slice import solve_midpoint_chord_slice, solve_point_difference_slice
from src.theorems.bound_application import BoundApplicator

FACTS='l: Line;G: Ellipse;A: Point;B: Point;Expression(G)=(x^2/4+y^2/9=1);Intersection(l,G)={A,B};Coordinate(MidPoint(LineSegmentOf(A,B)))=(1,3/2)'
SOLVERS=[solve_midpoint_chord_slice,solve_point_difference_slice]


@pytest.mark.parametrize('pid,answer',[(5644,'x+y-3/2'),(3682,'x-y+1'),(6164,'x-4*y-9/2')])
@pytest.mark.parametrize('solve',SOLVERS)
def test_real_initial_and_both_chains(pid,answer,solve):
    row=next(r for r in json.loads(Path('data/train_with_models_v3.json').read_text()) if r['id']==pid)
    s=TransitionState.from_facts(row['fact_expressions'],row['query_expressions'])
    assert len(s.chords)==len(s.chord_endpoint_names)==1 and not s.coordinates
    before=deepcopy(s);assert s.extract_answer() is None and s==before
    r=solve(row['fact_expressions'],row['query_expressions']);assert r.status=='solved',r.diagnostic
    assert sp.expand(r.answer-sp.sympify(answer,locals=s.symbols))==0
    assert [t.action.model_id for t in r.transitions] in ([3,40],[3,54,45])
    assert not r.state.coordinates
    names=next(iter(s.chord_endpoint_names.values()));mid=next(iter(s.chord_midpoints.values()))
    assert set(names.sources).isdisjoint(mid.sources)
    assert set((*names.sources,*mid.sources)).issubset(r.transitions[-1].read_facts)
    before=deepcopy(r.state)
    assert BoundApplicator().apply(r.state,r.transitions[-1].action).status=='no_op' and r.state==before


@pytest.mark.parametrize('facts',[
 FACTS.replace('Intersection(l,G)={A,B}','Intersection(G,l)={B,A}').replace('LineSegmentOf(A,B)','LineSegmentOf(B,A)'),
 ';'.join(reversed(FACTS.split(';'))),
 FACTS+';Intersection(G,l)={B,A}',
 FACTS+';Coordinate(MidPoint(InterceptChord(l,G)))=(1,3/2)'])
def test_reordering_and_source_merge(facts):
    r=solve_point_difference_slice(facts,'Expression(l)');assert r.status=='solved',r.diagnostic
    assert len(r.state.chords)==len(r.state.chord_endpoint_pairs)==1


@pytest.mark.parametrize('extra',[
 ';C: Point;Intersection(l,G)={A,C}',
 ';Intersection(l,G)={A,A}',
 ';h: Line;Intersection(h,G)={A,B}',
 ';Coordinate(MidPoint(InterceptChord(l,G)))=(0,1)',
 ';Coordinate(MidPoint(LineSegmentOf(B,A)))=(1,1)'])
def test_conflicting_inputs(extra):
    with pytest.raises(ValueError):TransitionState.from_facts(FACTS+extra,'Expression(l)')


@pytest.mark.parametrize('extra,status',[
 (';Coordinate(A)=(2,0);Coordinate(B)=(0,3)','solved'),
 (';Coordinate(A)=(2,0)','solved'),
 (';Coordinate(A)=(0,3);Coordinate(B)=(2,0)','solved'),
 (';Coordinate(A)=(0,0)','conflict'),
 (';Coordinate(A)=(-2,0)','conflict'),
 (';Coordinate(A)=(2,0);Coordinate(B)=(2,0)','conflict'),
 (';t: Real;Coordinate(A)=(t,0)','undetermined')])
@pytest.mark.parametrize('solve',SOLVERS)
def test_given_coordinates(extra,status,solve):
    r=solve(FACTS+extra,'Expression(l)');assert r.status==status,r.diagnostic
    if status!='solved':
        assert not any(f.owner=='l' for f in r.state.equations.values())
        before=deepcopy(r.state)
        assert BoundApplicator().apply(r.state,r.transitions[-1].action).status==status and r.state==before
    else:
        ids=[c.fact_id for c in r.state.coordinates.values()]
        assert set(ids).issubset(r.transitions[-1].read_facts)


def test_missing_association_and_undeclared_point():
    for facts in [FACTS.replace('Intersection(l,G)={A,B};',''),FACTS.replace('B: Point;','')]:
        with pytest.raises(ValueError):TransitionState.from_facts(facts,'Expression(l)')


def test_existing_wrong_line():
    r=solve_point_difference_slice(FACTS+';Expression(l)=(x+y=0)','Expression(l)')
    assert r.status=='conflict' and not any(k[1]=='normal_x' for k in r.state.properties)


def test_missing_name_record_rejected_without_mutation():
    r=solve_point_difference_slice(FACTS,'Expression(l)')
    r.state.chord_endpoint_names.clear();before=deepcopy(r.state)
    assert BoundApplicator().apply(r.state,r.transitions[-1].action).status=='inapplicable'
    assert r.state==before
