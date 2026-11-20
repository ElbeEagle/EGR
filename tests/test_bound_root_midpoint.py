from copy import deepcopy
from dataclasses import replace
import json
from pathlib import Path
import pytest
import sympy as sp
from src.state.transition_state import TransitionState
from src.theorems.bound_application import BoundApplicator,enumerate_actions

ROW=next(r for r in json.loads(Path('data/train_with_models_v3.json').read_text()) if r['id']==1827)

def prepare(facts=None):
 s=TransitionState.from_facts(facts or ROW['fact_expressions'],ROW['query_expressions']);app=BoundApplicator()
 for mid in (78,41):assert app.apply(s,enumerate_actions(s,mid)[0]).status=='applied'
 return s,enumerate_actions(s,54,'derive_midpoint_from_roots')[0]

@pytest.mark.parametrize('variant',['original','reverse','duplicate','axis'])
def test_success(variant):
 facts=ROW['fact_expressions']
 if variant=='reverse':facts=';'.join(reversed(facts.replace('Intersection(H, G) = {A, B}','Intersection(G,H)={B,A}').split(';')))
 if variant=='duplicate':facts+=';Intersection(G,H)={B,A}'
 if variant=='axis':facts=facts.replace('x^2 = 2*y','y^2 = 2*x').replace('y = x + 1','x = y + 1')
 s,a=prepare(facts);assert s.extract_answer() is None
 assert BoundApplicator().apply(s,a).status=='applied'
 assert s.extract_answer()==((2,1) if variant=='axis' else (1,2))
 before=deepcopy(s);assert BoundApplicator().apply(s,a).status=='no_op' and s==before
 del s.properties[a.relation_id,'midpoint_y'];assert s.extract_answer() is None
 assert BoundApplicator().apply(s,a).status=='applied'

@pytest.mark.parametrize('damage',['sum','source','curve','lift','conflict'])
def test_atomic_rejection(damage):
 s,a=prepare();f=s.intersection_reductions[a.relation_id]
 if damage=='sum':del s.properties[f.fact_id,'root_sum']
 if damage=='source':s.provenance[f'property:{f.fact_id}:root_sum']=()
 if damage=='curve':s.equations[f.curve_equation_id]=replace(s.equations[f.curve_equation_id],expression=s.symbols['x']**2-3*s.symbols['y'])
 if damage=='lift':s.intersection_reductions[f.fact_id]=replace(f,xy=(f.variable**2,f.variable))
 if damage=='conflict':s.properties[f.fact_id,'midpoint_y']=sp.Integer(99)
 before=deepcopy(s);assert BoundApplicator().apply(s,a).status in ('inapplicable','conflict') and s==before

@pytest.mark.parametrize('line',['y=0','y=-1','x=1'])
def test_degenerate(line):
 facts=ROW['fact_expressions'].replace('y = x + 1',line)
 s=TransitionState.from_facts(facts,ROW['query_expressions']);app=BoundApplicator()
 assert app.apply(s,enumerate_actions(s,78)[0]).status=='applied'
 app.apply(s,enumerate_actions(s,41)[0]);a=enumerate_actions(s,54,'derive_midpoint_from_roots')[0]
 before=deepcopy(s);assert app.apply(s,a).status=='inapplicable' and s==before

def test_ambiguous_pair():
 s=TransitionState.from_facts(ROW['fact_expressions']+';C: Point;D: Point;Intersection(H,G)={C,D}',ROW['query_expressions'])
 before=deepcopy(s);assert BoundApplicator().apply(s,enumerate_actions(s,78)[0]).status=='conflict' and s==before
