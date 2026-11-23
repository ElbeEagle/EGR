from copy import deepcopy
from dataclasses import replace
import json
from pathlib import Path
import pytest
import sympy as sp
from src.state.transition_state import TransitionState,EquationFact
from src.state.focus_asymptote_query import FocusAsymptoteDistanceQuery
from src.theorems.bound_application import BoundApplicator,BoundAction,enumerate_actions
ROWS={r['id']:r for r in json.loads(Path('data/train_with_models_v3.json').read_text())}

def prepare(pid=891,transform=lambda f:f,standard=5):
 r=ROWS[pid];s=TransitionState.from_facts(transform(r['fact_expressions']),r['query_expressions']);a=enumerate_actions(s,22)[0];app=BoundApplicator()
 assert s.extract_answer() is None
 assert app.apply(s,a).status=='inapplicable'
 assert app.apply(s,BoundAction(standard,'extract_parameters',a.curve,a.equation_id)).status=='applied'
 return s,a

@pytest.mark.parametrize('pid',[3200,891])
def test_real(pid):
 s,a=prepare(pid);app=BoundApplicator();t=app.apply(s,a);assert t.status=='applied',t.diagnostic
 assert s.extract_answer()==sp.sqrt(3)
 before=deepcopy(s);assert app.apply(s,a).status=='no_op' and s==before

def test_y_axis():
 s,a=prepare(transform=lambda f:f.replace('x^2/4 - y^2/3','y^2/4 - x^2/3'),standard=6)
 assert BoundApplicator().apply(s,a).status=='applied';assert s.extract_answer()==sp.sqrt(3)

@pytest.mark.parametrize('damage',['source','equation','frame','asymptote','c','distance','binding','multiple'])
def test_atomic_failure(damage):
 s,a=prepare();x=s.symbols['x']
 if damage=='source':s.provenance['property:G:b_sq']=()
 if damage=='equation':s.equations[a.equation_id]=replace(s.equations[a.equation_id],expression=x*x-s.symbols['y']**2-1)
 if damage=='frame':s.frames['G']=replace(s.frames['G'],axis='y')
 if damage=='asymptote':s.equations['bad']=EquationFact('bad','G','asymptote',x,'test')
 if damage=='c':s.properties['G','c_sq']=sp.Integer(99)
 if damage=='distance':s.properties['G','focus_asymptote_distance']=sp.Integer(99)
 if damage=='binding':a=replace(a,curve='other')
 if damage=='multiple':s.equations['other']=replace(s.equations[a.equation_id],fact_id='other')
 before=deepcopy(s);assert BoundApplicator().apply(s,a).status in ('conflict','inapplicable') and s==before

def test_existing_asymptotes():
 s,a=prepare();app=BoundApplicator();t=app.apply(s,enumerate_actions(s,21,'derive_asymptotes')[0]);assert t.status=='applied'
 assert app.apply(s,a).status=='applied'

def test_multiple_curves():
 s,a=prepare(transform=lambda f:f+';H: Hyperbola;Expression(H)=(x^2-y^2/9=1)');app=BoundApplicator()
 assert app.apply(s,a).status=='applied'
 other=next(x for x in enumerate_actions(s,22) if x.curve=='H');s.query=FocusAsymptoteDistanceQuery('H');assert s.extract_answer() is None
 assert app.apply(s,BoundAction(5,'extract_parameters','H',other.equation_id)).status=='applied'
 assert app.apply(s,other).status=='applied';assert s.extract_answer()==3
 assert s.properties['G','focus_asymptote_distance']==sp.sqrt(3)

def test_cross_curve_query_rejected():
 r=ROWS[891]
 with pytest.raises(ValueError):TransitionState.from_facts(r['fact_expressions']+';H: Hyperbola','Distance(Focus(G),Asymptote(H))')
