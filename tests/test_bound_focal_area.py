from copy import deepcopy
from dataclasses import replace
import json
from pathlib import Path
import pytest
import sympy as sp
from src.state.transition_state import TransitionState
from src.theorems.bound_application import BoundApplicator,BoundAction,enumerate_actions
ROWS={r['id']:r for r in json.loads(Path('data/train_with_models_v3.json').read_text())}

def prepare(pid=3174,transform=lambda f:f,standard=3):
 r=ROWS[pid];s=TransitionState.from_facts(transform(r['fact_expressions']),r['query_expressions']);a=enumerate_actions(s,30)[0];app=BoundApplicator()
 assert s.extract_answer() is None
 assert app.apply(s,BoundAction(standard,'extract_parameters',a.curve,a.equation_id)).status=='applied'
 assert app.apply(s,enumerate_actions(s,11,'derive_c_sq')[0]).status=='applied'
 return s,a

@pytest.mark.parametrize('pid,value',[(3174,sp.sqrt(3)/3),(3900,1),(6748,sp.sqrt(3))])
def test_real(pid,value):
 s,a=prepare(pid);app=BoundApplicator();t=app.apply(s,a);assert t.status=='applied',t.diagnostic
 assert sp.simplify(s.extract_answer()-value)==0
 before=deepcopy(s);assert app.apply(s,a).status=='no_op' and s==before

@pytest.mark.parametrize('theta,ok',[('0',False),('pi',False),('5*pi/6',False),('2*pi/3',True)])
def test_boundaries(theta,ok):
 s,a=prepare(transform=lambda f:f.replace('=pi/3','='+theta));before=deepcopy(s);t=BoundApplicator().apply(s,a)
 assert t.status==('applied' if ok else 'conflict')
 if not ok:assert s==before

@pytest.mark.parametrize('variant',['swap','duplicate','reorder','y'])
def test_identity(variant):
 def transform(f):
  if variant=='swap':return f.replace('AngleOf(F1,P,F2)','AngleOf(F2,P,F1)')
  if variant=='duplicate':return f+';AngleOf(F2,P,F1)=pi/3'
  if variant=='reorder':return ';'.join(reversed(f.split(';')))
  return f.replace('x^2/4 + y^2','y^2/4 + x^2')
 s,a=prepare(transform=transform,standard=4 if variant=='y' else 3)
 assert BoundApplicator().apply(s,a).status=='applied'

def test_vertex_misplaced():
 r=ROWS[3174];s=TransitionState.from_facts(r['fact_expressions'].replace('AngleOf(F1,P,F2)','AngleOf(P,F1,F2)'),r['query_expressions'])
 assert not enumerate_actions(s,30)

@pytest.mark.parametrize('damage',['source','c','angle_source','curve','output'])
def test_atomic_failure(damage):
 s,a=prepare()
 if damage=='source':s.provenance['property:G:c_sq']=()
 if damage=='c':del s.properties['G','c_sq']
 if damage=='angle_source':k=next(iter(s.angle_facts));s.angle_facts[k]=replace(s.angle_facts[k],sources=())
 if damage=='curve':a=replace(a,curve='X')
 if damage=='output':s.properties[a.relation_id,'area']=sp.Integer(99)
 before=deepcopy(s);assert BoundApplicator().apply(s,a).status in ('conflict','inapplicable') and s==before

@pytest.mark.parametrize('coords',['Coordinate(P)=(0,0)','Coordinate(P)=(0,1)','Coordinate(F1)=(0,0)'])
def test_coordinates_contradict(coords):
 s,a=prepare(transform=lambda f:f+';'+coords);before=deepcopy(s)
 assert BoundApplicator().apply(s,a).status=='conflict' and s==before

def test_max_angle_matching_coordinate():
 s,a=prepare(transform=lambda f:f.replace('=pi/3','=2*pi/3')+';Coordinate(P)=(0,1)')
 assert BoundApplicator().apply(s,a).status=='applied'

def test_ambiguous_curve():
 s,a=prepare(transform=lambda f:f+';D: Ellipse;Expression(D)=(x^2/4+y^2=1);Focus(D)={F1,F2};PointOnCurve(P,D)')
 assert BoundApplicator().apply(s,a).status=='applied' and s.extract_answer() is None

def test_conflicting_angles():
 with pytest.raises(ValueError):prepare(transform=lambda f:f+';AngleOf(F2,P,F1)=pi/2')
