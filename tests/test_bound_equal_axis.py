from copy import deepcopy
from dataclasses import replace
import json
from pathlib import Path
import pytest
import sympy as sp
from src.state.transition_state import TransitionState,EccentricityQuery
from src.theorems.bound_application import BoundApplicator,BoundAction,enumerate_actions
from src.reasoning.bound_slice import solve_eccentricity_slice
from src.solver.equal_axis_operations import equal_axis_eccentricity
from src.solver.transition_primitives import TransitionError
ROWS={r['id']:r for r in json.loads(Path('data/train_with_models_v3.json').read_text())}

def prepare(pid=650,facts=None,standard=5):
 r=ROWS[pid];s=TransitionState.from_facts(facts or r['fact_expressions'],r['query_expressions']);a=enumerate_actions(s,24)[0];app=BoundApplicator()
 assert app.apply(s,a).status=='inapplicable'
 assert app.apply(s,BoundAction(standard,'extract_parameters',a.curve,a.equation_id)).status=='applied'
 return s,a

@pytest.mark.parametrize('pid',[650,1412])
def test_real(pid):
 s,a=prepare(pid);app=BoundApplicator();t=app.apply(s,a);assert t.status=='applied',t.diagnostic
 assert s.extract_answer()==sp.sqrt(2) and ('G','c_sq') not in s.properties
 r=ROWS[pid];old=solve_eccentricity_slice(r['fact_expressions'],r['query_expressions']);assert old.answer==s.extract_answer()
 before=deepcopy(s);assert app.apply(s,a).status=='no_op' and s==before

@pytest.mark.parametrize('equation,mid',[('y^2-x^2=4',6),('2*x^2-2*y^2=8',5),('x^2/4-y^2/4=1',5)])
def test_axis_and_scale(equation,mid):
 s,a=prepare(facts=f'G: Hyperbola;Expression(G)=({equation})',standard=mid)
 assert BoundApplicator().apply(s,a).status=='applied';assert s.extract_answer()==sp.sqrt(2)

def test_non_equal():
 s,a=prepare(2287);before=deepcopy(s)
 assert BoundApplicator().apply(s,a).status=='inapplicable' and s==before

@pytest.mark.parametrize('damage',['source','frame_source','equation','c','e','binding','multiple'])
def test_failure_atomic(damage):
 s,a=prepare()
 if damage=='source':s.provenance['property:G:a_sq']=()
 if damage=='frame_source':s.provenance['frame:G']=()
 if damage=='equation':s.equations[a.equation_id]=replace(s.equations[a.equation_id],expression=s.symbols['x']**2-2*s.symbols['y']**2-4)
 if damage=='c':s.properties['G','c_sq']=sp.Integer(99)
 if damage=='e':s.properties['G','eccentricity']=sp.Integer(99)
 if damage=='binding':a=replace(a,curve='other')
 if damage=='multiple':s.equations['other']=replace(s.equations[a.equation_id],fact_id='other')
 before=deepcopy(s);assert BoundApplicator().apply(s,a).status in ('inapplicable','conflict') and s==before

def test_consistent_c_and_e():
 r=ROWS[650];s=solve_eccentricity_slice(r['fact_expressions'],r['query_expressions']).state;before=deepcopy(s)
 assert BoundApplicator().apply(s,enumerate_actions(s,24)[0]).status=='no_op' and s==before

def test_isolation():
 s,a=prepare(facts=ROWS[650]['fact_expressions']+';H: Hyperbola;Expression(H)=(y^2-x^2=2)');app=BoundApplicator()
 assert app.apply(s,a).status=='applied';s.query=EccentricityQuery('H');assert s.extract_answer() is None
 other=next(a for a in enumerate_actions(s,24) if a.curve=='H')
 assert app.apply(s,BoundAction(6,'extract_parameters','H',other.equation_id)).status=='applied'
 assert app.apply(s,other).status=='applied' and s.extract_answer()==sp.sqrt(2)

@pytest.mark.parametrize('value',[sp.S.Zero,-sp.S.One,sp.oo,sp.Symbol('a',positive=True)])
def test_invalid_numeric_parameters(value):
 with pytest.raises(TransitionError):equal_axis_eccentricity(value,value)
