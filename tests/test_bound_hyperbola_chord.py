from copy import deepcopy
from dataclasses import replace
import json
from pathlib import Path
import pytest
import sympy as sp
from src.reasoning.bound_slice import solve_hyperbola_chord_slice
from src.state.transition_state import TransitionState
from src.theorems.bound_application import BoundApplicator,enumerate_actions

FACTS='G: Hyperbola;H: LineSegment;P: Point;Expression(G)=(x^2/4-y^2=1);Coordinate(P)=(4,1);IsChordOf(H,G);MidPoint(H)=P'
QUERY='Expression(OverlappingLine(H))'


@pytest.mark.parametrize('pid,status',[(1801,'solved'),(4359,'solved'),(3119,'conflict')])
def test_real_inputs(pid,status):
    row=next(r for r in json.loads(Path('data/train_with_models_v3.json').read_text()) if r['id']==pid)
    r=solve_hyperbola_chord_slice(row['fact_expressions'],row['query_expressions'])
    assert r.status==status,r.diagnostic
    assert [t.action.model_id for t in r.transitions]==[5,54,46]
    if status=='solved':
        assert sp.expand(r.answer-(r.state.symbols['x']-r.state.symbols['y']-3))==0
        assert not enumerate_actions(r.state,40) and not enumerate_actions(r.state,45)
        before=deepcopy(r.state)
        assert BoundApplicator().apply(r.state,r.transitions[-1].action).status=='no_op' and r.state==before
    else:assert r.answer is None and not any(k[1]=='midpoint_q' for k in r.state.properties)


@pytest.mark.parametrize('equation,point,standard,alpha,beta',[
 ('x^2/4-y^2=1','4,1',5,sp.Rational(1,4),-1),
 ('y^2/4-x^2=1','1,4',6,-1,sp.Rational(1,4)),
 ('x^2-4*y^2=4','4,1',5,sp.Rational(1,4),-1),
 ('x^2/4-y^2=1','-4,-1',5,sp.Rational(1,4),-1),
 ('x^2/4-y^2=1','0,1',5,sp.Rational(1,4),-1),
 ('y^2/4-x^2=1','1,0',6,-1,sp.Rational(1,4)),
 ('x^2-y^2=1','2,0',5,1,-1)])
def test_axes_signs_and_independent_intersections(equation,point,standard,alpha,beta):
    r=solve_hyperbola_chord_slice(FACTS.replace('x^2/4-y^2=1',equation).replace('(4,1)',f'({point})'),QUERY)
    assert r.status=='solved',r.diagnostic
    assert r.transitions[0].action.model_id==standard
    op=r.transitions[-1].operations[0];assert op['alpha']==alpha and op['beta']==beta
    x,y=r.state.symbols['x'],r.state.symbols['y'];curve=next(f.expression for f in r.state.equations.values() if f.owner=='G')
    pts=sp.solve([curve,r.answer],(x,y));assert len(pts)==2 and pts[0]!=pts[1]
    m=tuple(map(sp.Rational,point.split(',')))
    assert all(sp.simplify((pts[0][i]+pts[1][i])/2-m[i])==0 for i in range(2))
    assert len(r.state.coordinates)==1


@pytest.mark.parametrize('point,status,diagnostic',[
 ('1,0','conflict','no two distinct'),('2,0','conflict','Tangent'),
 ('2,1','conflict','q=0'),('0,0','undetermined','Center')])
def test_boundary_failures_are_atomic(point,status,diagnostic):
    r=solve_hyperbola_chord_slice(FACTS.replace('(4,1)',f'({point})'),QUERY)
    assert r.status==status and diagnostic in r.diagnostic
    assert r.answer is None and len(r.state.properties)==4
    before=deepcopy(r.state)
    assert BoundApplicator().apply(r.state,r.transitions[-1].action).status==status and r.state==before


@pytest.mark.parametrize('damage',['sums','source','parameters','frame','coordinate','line'])
def test_prerequisites_and_consistency(damage):
    r=solve_hyperbola_chord_slice(FACTS,QUERY);s=r.state;c=next(iter(s.chords.values()))
    if damage=='sums':del s.properties[c.pair_id,'x_sum']
    elif damage=='source':s.provenance[f'property:{c.pair_id}:x_sum']=()
    elif damage=='parameters':s.properties['G','a_sq']=sp.Integer(99)
    elif damage=='frame':s.frames.clear()
    elif damage=='coordinate':s.coordinates['P']=replace(s.coordinates['P'],xy=(sp.S.Zero,sp.S.One))
    else:
        key=f'derived:{c.chord_id}:line';s.equations[key]=replace(s.equations[key],expression=s.symbols['x'])
    before=deepcopy(s)
    assert BoundApplicator().apply(s,r.transitions[-1].action).status in ('inapplicable','conflict') and s==before


def test_type_isolation_and_missing_sums():
    s=TransitionState.from_facts(FACTS,QUERY);before=deepcopy(s)
    a=enumerate_actions(s,46)[0]
    assert BoundApplicator().apply(s,a).status=='inapplicable' and s==before
    assert BoundApplicator().apply(s,replace(a,model_id=45)).status=='inapplicable' and s==before
    e=TransitionState.from_facts(FACTS.replace('Hyperbola','Ellipse').replace('x^2/4-y^2','x^2/4+y^2'),QUERY)
    assert not enumerate_actions(e,46)
    assert BoundApplicator().apply(e,a).status=='inapplicable'


@pytest.mark.parametrize('equation',['x^2/4+y^2=1','(x-1)^2/4-y^2=1'])
def test_wrong_type_or_shifted_equation(equation):
    r=solve_hyperbola_chord_slice(FACTS.replace('x^2/4-y^2=1',equation),QUERY)
    assert r.status!='solved' and r.answer is None


def test_symbolic_midpoint_stays_undetermined():
    r=solve_hyperbola_chord_slice(FACTS.replace('Coordinate(P)=(4,1)','t: Real;Coordinate(P)=(t,1)'),QUERY)
    assert r.status=='undetermined' and r.answer is None


def test_named_input_reverse_order():
    rows=json.loads(Path('data/train_with_models_v3.json').read_text());row=next(r for r in rows if r['id']==4359)
    facts=row['fact_expressions'].replace('Intersection(H, G) = {A, B}','Intersection(G,H)={B,A}').replace('LineSegmentOf(A,B)','LineSegmentOf(B,A)')
    r=solve_hyperbola_chord_slice(';'.join(reversed(facts.split(';'))),row['query_expressions'])
    assert r.status=='solved',r.diagnostic
