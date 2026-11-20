from copy import deepcopy
from dataclasses import replace
import json
from pathlib import Path
import pytest
import sympy as sp
from src.state.transition_state import TransitionState
from src.theorems.bound_application import BoundApplicator,BoundAction,enumerate_actions
ROWS={r['id']:r for r in json.loads(Path('data/train_with_models_v3.json').read_text())}

def prepare(pid=998,transform=lambda f:f,axis=3,query=None):
 r=ROWS[pid];s=TransitionState.from_facts(transform(r['fact_expressions']),query or r['query_expressions']);app=BoundApplicator();a=enumerate_actions(s,32)[0]
 assert s.extract_answer() is None
 assert app.apply(s,BoundAction(axis,'extract_parameters',a.curve,a.equation_id)).status=='applied'
 assert app.apply(s,enumerate_actions(s,11,'derive_c_sq')[0]).status=='applied'
 return s,a

@pytest.mark.parametrize('pid,expected',[(998,16),(1552,18)])
def test_real(pid,expected):
 s,a=prepare(pid);app=BoundApplicator();t=app.apply(s,a);assert t.status=='applied',t.diagnostic
 assert s.extract_answer()==expected
 before=deepcopy(s);assert app.apply(s,a).status=='no_op' and s==before

@pytest.mark.parametrize('transform,axis',[(lambda f:';'.join(reversed(f.split(';'))),3),(lambda f:f+';Focus(C)={F2,F1}',3),(lambda f:f.replace('x^2/25 + y^2/16','y^2/25 + x^2/16'),4)])
def test_order_and_axis(transform,axis):
 s,a=prepare(transform=transform,axis=axis,query='Perimeter(TriangleOf(F2,P,F1))');assert BoundApplicator().apply(s,a).status=='applied';assert s.extract_answer()==16

@pytest.mark.parametrize('damage',['c','source','value','binding','conflict'])
def test_failure_atomic(damage):
 s,a=prepare()
 if damage=='c':del s.properties['C','c_sq']
 if damage=='source':s.provenance['property:C:c_sq']=()
 if damage=='value':s.properties['C','c_sq']=sp.Integer(99)
 if damage=='binding':a=replace(a,curve='other')
 if damage=='conflict':s.properties[a.relation_id,'perimeter']=sp.Integer(99)
 before=deepcopy(s);assert BoundApplicator().apply(s,a).status in ('inapplicable','conflict') and s==before

@pytest.mark.parametrize('coords,good',[('Coordinate(P)=(5,0)',True),('Coordinate(P)=(0,4);Coordinate(F1)=(3,0);Coordinate(F2)=(-3,0)',True),('Coordinate(P)=(0,0)',False),('Coordinate(F1)=(4,0)',False),('Coordinate(F1)=(3,0);Coordinate(F2)=(3,0)',False)])
def test_coordinates(coords,good):
 s,a=prepare(transform=lambda f:f+';'+coords);before=deepcopy(s);t=BoundApplicator().apply(s,a)
 assert t.status==('applied' if good else 'conflict')
 if not good:assert s==before

def test_ambiguous_pair():
 with pytest.raises(ValueError):prepare(transform=lambda f:f+';X: Point;Focus(C)={F1,X}')

def test_cross_curve_and_ambiguous_query():
 s,a=prepare(transform=lambda f:f+';D: Ellipse;Expression(D)=(x^2/25+y^2/9=1);Focus(D)={F1,F2};PointOnCurve(P,D)')
 app=BoundApplicator();assert app.apply(s,a).status=='applied'
 assert s.extract_answer() is None
 other=next(x for x in enumerate_actions(s,32) if x.curve=='D')
 before=deepcopy(s)
 assert app.apply(s,replace(a,equation_id=other.equation_id)).status=='inapplicable' and s==before
 assert app.apply(s,replace(a,incidence_id=other.incidence_id)).status=='inapplicable' and s==before
