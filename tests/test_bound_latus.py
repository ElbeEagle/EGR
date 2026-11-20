from copy import deepcopy
import json
from pathlib import Path
import pytest
import sympy as sp
from src.state.transition_state import TransitionState
from src.theorems.bound_application import BoundApplicator,enumerate_actions,BoundAction

ROWS={r['id']:r for r in json.loads(Path('data/train_with_models_v3.json').read_text())}

def prepare(pid,standard=None,transform=lambda s:s):
 r=ROWS[pid];s=TransitionState.from_facts(transform(r['fact_expressions']),r['query_expressions'])
 mid=19 if pid==6057 else 20;a=enumerate_actions(s,mid)[0];app=BoundApplicator()
 assert s.extract_answer() is None
 assert app.apply(s,a).status=='inapplicable'
 t=app.apply(s,BoundAction(standard or (5 if mid==19 else 7),'extract_parameters',a.curve,a.equation_id))
 assert t.status=='applied',t.diagnostic
 return s,a

@pytest.mark.parametrize('pid,expected',[(6057,8*sp.sqrt(3)/3),(6770,4)])
def test_real(pid,expected):
 s,a=prepare(pid);app=BoundApplicator();t=app.apply(s,a)
 assert t.status=='applied',t.diagnostic
 assert sp.simplify(s.extract_answer()-expected)==0 and not s.coordinates
 before=deepcopy(s);assert app.apply(s,a).status=='no_op' and s==before
 s.properties[a.relation_id,'chord_length']=sp.Integer(999);before=deepcopy(s)
 assert app.apply(s,a).status=='conflict' and s==before

@pytest.mark.parametrize('standard,old,new',[(8,'y^2 = 4*x','y^2 = -4*x'),(9,'y^2 = 4*x','x^2 = 4*y'),(10,'y^2 = 4*x','x^2 = -4*y')])
def test_parabola_direction(standard,old,new):
 s,a=prepare(6770,standard,lambda f:f.replace(old,new));assert BoundApplicator().apply(s,a).status=='applied';assert s.extract_answer()==4

def test_y_axis():
 s,a=prepare(6057,6,lambda f:f.replace('x^2/3 - y^2/4','y^2/3 - x^2/4').replace('xAxis','yAxis'))
 assert BoundApplicator().apply(s,a).status=='applied'

@pytest.mark.parametrize('kind',['focus','perpendicular'])
def test_missing_evidence(kind):
 s,a=prepare(6057);s.latus_evidence={k:v for k,v in s.latus_evidence.items() if v.kind!=kind};before=deepcopy(s)
 assert BoundApplicator().apply(s,a).status=='inapplicable' and s==before

def test_wrong_axis():
 s,a=prepare(6057,transform=lambda f:f.replace('xAxis','yAxis'));before=deepcopy(s)
 assert BoundApplicator().apply(s,a).status=='conflict' and s==before

def test_reorder_duplicate():
 s,a=prepare(6770,transform=lambda f:';'.join(reversed((f+';PointOnCurve(Focus(G),L)=True').split(';'))))
 assert BoundApplicator().apply(s,a).status=='applied' and s.extract_answer()==4

@pytest.mark.parametrize('pid,key',[(6057,'a_sq'),(6770,'p')])
def test_missing_standard_source(pid,key):
 s,a=prepare(pid);s.provenance[f'property:{a.curve}:{key}']=();before=deepcopy(s)
 assert BoundApplicator().apply(s,a).status=='inapplicable' and s==before
