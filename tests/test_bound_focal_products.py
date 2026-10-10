from copy import deepcopy
from dataclasses import replace
import json
from pathlib import Path
import pytest
import sympy as sp
from src.state.transition_state import TransitionState
from src.theorems.bound_application import BoundApplicator,enumerate_actions

DATA=json.loads(Path('data/train_with_models_v3.json').read_text())
FACTS='G: Parabola;H: Line;O: Origin;A: Point;B: Point;Expression(G)=(y^2=4*x);PointOnCurve(Focus(G),H);Intersection(G,H)={A,B}'
QUERY='DotProduct(VectorOf(O,A),VectorOf(O,B))'


def run(state, mids):
    transitions=[]
    for mid in mids:
        action,=enumerate_actions(state,mid, "extract_parameters" if mid in (7,8,9,10) else None)
        result=BoundApplicator().apply(state,action)
        assert result.status=='applied', result.diagnostic
        transitions.append(result)
    return transitions


@pytest.mark.parametrize('order',['G,H','H,G'])
@pytest.mark.parametrize('points',['A,B','B,A'])
def test_original_and_order(order,points):
    row=next(r for r in DATA if r['id']==4373)
    s=TransitionState.from_facts(row['fact_expressions'],row['query_expressions'])
    run(s,[7,34,35,59]);assert s.extract_answer()==-3
    s=TransitionState.from_facts(FACTS.replace('Intersection(G,H)={A,B}',f'Intersection({order})={{{points}}}'),QUERY)
    assert s.extract_answer() is None and not s.properties
    run(s,[7,34]);assert s.extract_answer() is None
    before=deepcopy(s)
    assert BoundApplicator().apply(s,enumerate_actions(s,59)[0]).status=='inapplicable' and s==before
    ts=run(s,[35,59]);assert s.extract_answer()==-3
    n,=s.named_intersections.values()
    assert (s.properties[(n.fact_id,'x_product')],s.properties[(n.fact_id,'y_product')])==(1,-4)
    before=deepcopy(s)
    assert BoundApplicator().apply(s,ts[-1].action).status=='no_op' and s==before
    assert not s.intersection_reductions


def test_1191_projection():
    row=next(r for r in DATA if r['id']==1191)
    parts=row['fact_expressions'].split(';')
    facts=';'.join(p for p in parts if not p.strip().startswith('Abs('))
    s=TransitionState.from_facts(facts,None);ts=run(s,[9,34,35])
    n,=s.named_intersections.values()
    assert (s.properties[(n.fact_id,'y_product')],s.properties[(n.fact_id,'x_product')])==(4,-16)
    alias,=s.focus_aliases.values();assert alias.fact_id in ts[-1].read_facts
    assert s.extract_answer() is None


def test_6347_no_rm33_or_vieta():
    row=next(r for r in DATA if r['id']==6347)
    s=TransitionState.from_facts(row['fact_expressions'],None)
    run(s,[7,78,34,35]);n,=s.intersection_reductions.values()
    assert (s.properties[(n.fact_id,'x_product')],s.properties[(n.fact_id,'y_product')])==(1,-4)
    assert not any(k[1] in ('root_product','root_sum','chord_length') for k in s.properties)


@pytest.mark.parametrize('mid,expr,axis',[(7,'y^2=4*x','x'),(8,'y^2=-4*x','x'),(9,'x^2=4*y','y'),(10,'x^2=-4*y','y')])
def test_direction(mid,expr,axis):
    s=TransitionState.from_facts(FACTS.replace('y^2=4*x',expr),None)
    run(s,[mid,34,35]);n,=s.named_intersections.values()
    assert s.properties[(n.fact_id,axis+'_product')]==1
    assert s.properties[(n.fact_id,('y' if axis=='x' else 'x')+'_product')]==-4


@pytest.mark.parametrize('line',['y=x+1','y=0'])
def test_given_equation_conflict(line):
    s=TransitionState.from_facts(FACTS+f';Expression(H)=({line})',None);run(s,[7]);before=deepcopy(s)
    assert BoundApplicator().apply(s,enumerate_actions(s,34)[0]).status=='conflict' and s==before


@pytest.mark.parametrize('change',[{'relation_id':'bad'},{'line':'G'},{'mode':'bad'},{'point':'A'},{'equation_id':'bad'}])
def test_wrong_binding(change):
    s=TransitionState.from_facts(FACTS,None);run(s,[7]);before=deepcopy(s)
    action=replace(enumerate_actions(s,34)[0],**change)
    assert BoundApplicator().apply(s,action).status=='inapplicable' and s==before


def test_conflict_and_duplicate():
    s=TransitionState.from_facts(FACTS,None);run(s,[7,34]);action=enumerate_actions(s,34)[0]
    before=deepcopy(s);assert BoundApplicator().apply(s,action).status=='no_op' and s==before
    s.properties[(action.relation_id,'y_product')]=sp.S.One;before=deepcopy(s)
    assert BoundApplicator().apply(s,enumerate_actions(s,35)[0]).status=='conflict' and s==before


def test_wrong_focus_curve():
    facts=FACTS.replace('PointOnCurve(Focus(G),H)','J: Parabola;PointOnCurve(Focus(J),H)')
    s=TransitionState.from_facts(facts,None);run(s,[7]);before=deepcopy(s)
    assert BoundApplicator().apply(s,enumerate_actions(s,34)[0]).status=='inapplicable' and s==before


def test_tampered_reduction():
    s=TransitionState.from_facts('G: Parabola;H: Line;Expression(G)=(y^2=4*x);Expression(H)=(y=x-1)',None)
    run(s,[7,78]);key=next(iter(s.intersection_reductions));f=s.intersection_reductions[key]
    s.intersection_reductions[key]=replace(f,xy=(sp.S.Zero,f.xy[1]));before=deepcopy(s)
    assert BoundApplicator().apply(s,enumerate_actions(s,34)[0]).status=='conflict' and s==before


def test_fixed_replay_and_read_only_query():
    from src.reasoning.bound_slice import solve_origin_dot_slice
    r=solve_origin_dot_slice(FACTS,QUERY)
    assert r.status=='solved' and r.answer==-3
    assert [t.action.model_id for t in r.transitions]==[7,34,35,59]
    before=deepcopy(r.state);assert r.state.extract_answer()==-3 and r.state==before
    q=replace(r.state.query,points=('A','O'));r.state.query=q
    assert r.state.extract_answer() is None
    assert BoundApplicator().apply(r.state,r.transitions[-1].action).status=='inapplicable'


@pytest.mark.parametrize('extra',['Coordinate(A)=(0,0)',
                                 'Coordinate(A)=(1,2);Coordinate(B)=(1,2)',
                                 'Coordinate(A)=(1,2);Coordinate(B)=(4,4)',
                                 'Coordinate(A)=(1,0)'])
def test_known_coordinates_conflict(extra):
    s=TransitionState.from_facts(FACTS+';'+extra,None);run(s,[7]);before=deepcopy(s)
    assert BoundApplicator().apply(s,enumerate_actions(s,34)[0]).status=='conflict' and s==before


def test_known_coordinates_consistent():
    s=TransitionState.from_facts(FACTS+';Coordinate(A)=(1,2);Coordinate(B)=(1,-2)',QUERY)
    run(s,[7,34,35,59]);assert s.extract_answer()==-3


def test_nonorigin_rejected():
    s=TransitionState.from_facts(FACTS.replace('O: Origin','O: Point;Coordinate(O)=(1,0)'),QUERY)
    run(s,[7,34,35]);before=deepcopy(s)
    assert BoundApplicator().apply(s,enumerate_actions(s,59)[0]).status=='inapplicable' and s==before


@pytest.mark.parametrize('missing',['frame','focus','p'])
def test_missing_geometry(missing):
    s=TransitionState.from_facts(FACTS,None);run(s,[7])
    if missing=='frame':s.frames.clear()
    else:del s.properties[('G','focus_x' if missing=='focus' else 'p')]
    before=deepcopy(s)
    assert BoundApplicator().apply(s,enumerate_actions(s,34)[0]).status=='inapplicable' and s==before
