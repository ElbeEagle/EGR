from copy import deepcopy
from dataclasses import replace
import json
from pathlib import Path
import pytest
import sympy as sp
from src.state.transition_state import TransitionState
from src.theorems.bound_application import BoundApplicator, enumerate_actions
from src.solver.intersection_operations import slope_chord_length
from src.solver.transition_primitives import TransitionError

ROWS={r['id']:r for r in json.loads(Path('data/train_with_models_v3.json').read_text())}


def prepare(pid=6347, facts=None, joint=True):
    r=ROWS[pid];s=TransitionState.from_facts(facts or r['fact_expressions'],r['query_expressions']);app=BoundApplicator()
    for mid in ([78,41] if joint else [78,42,43]):
        a=next(a for a in enumerate_actions(s,mid) if a.curve=='G' and a.line=='H')
        t=app.apply(s,a);assert t.status=='applied',t.diagnostic
    return s,next(a for a in enumerate_actions(s,51) if a.curve=='G' and a.line=='H')


@pytest.mark.parametrize('pid,expected',[(3057,sp.sqrt(15)),(6347,sp.Integer(8))])
@pytest.mark.parametrize('joint',[True,False])
def test_original(pid,expected,joint):
    s,a=prepare(pid,joint=joint);app=BoundApplicator();assert s.extract_answer() is None
    t=app.apply(s,a);assert t.status=='applied',t.diagnostic
    assert s.extract_answer()==expected and not s.coordinates
    before=deepcopy(s);assert app.apply(s,a).status=='no_op' and s==before
    assert app.apply(s,replace(a,model_id=50)).status=='no_op' and s==before


@pytest.mark.parametrize('curve,line,expected',[('x^2=4*y','x=y-1',8),('x^2=4*y','y=1',4),('2*y^2=8*x','2*y=2*x-2',8)])
def test_axis_horizontal_scale(curve,line,expected):
    s,a=prepare(facts=f'G:Parabola;H:Line;Expression(G)=({curve});Expression(H)=({line})')
    assert BoundApplicator().apply(s,a).status=='applied' and s.extract_answer()==expected


def test_vertical_keeps_rm50():
    s,a=prepare(facts='G:Parabola;H:Line;Expression(G)=(y^2=4*x);Expression(H)=(x=1)');app=BoundApplicator();before=deepcopy(s)
    assert app.apply(s,a).status=='inapplicable' and s==before
    assert app.apply(s,replace(a,model_id=50)).status=='applied' and s.extract_answer()==4


@pytest.mark.parametrize('damage',['sum','product','source','reduction_source','curve','line','lift','nonaffine','polynomial','value','answer','binding'])
def test_failure_atomic(damage):
    s,a=prepare();key=a.relation_id;f=s.intersection_reductions[key];x,y=s.symbols['x'],s.symbols['y']
    if damage in ('sum','product'):del s.properties[key,'root_'+damage]
    if damage=='source':s.provenance[f'property:{key}:root_sum']=('unrelated',)
    if damage=='reduction_source':s.provenance[key]=()
    if damage=='curve':s.equations[a.equation_id]=replace(s.equations[a.equation_id],expression=y*y-8*x)
    if damage=='line':s.equations[a.line_equation_id]=replace(s.equations[a.line_equation_id],expression=y-x-2)
    if damage=='lift':s.intersection_reductions[key]=replace(f,xy=(y+2,y))
    if damage=='nonaffine':s.intersection_reductions[key]=replace(f,xy=(y*y,y))
    if damage=='polynomial':s.intersection_reductions[key]=replace(f,polynomial=y-1)
    if damage=='value':s.properties[key,'root_sum']=sp.Integer(99)
    if damage=='answer':s.properties[key,'chord_length']=sp.Integer(99)
    if damage=='binding':a=replace(a,line='other')
    before=deepcopy(s);t=BoundApplicator().apply(s,a)
    assert t.status in ('inapplicable','conflict') and s==before,t.diagnostic


@pytest.mark.parametrize('line',['y=0','y=x+1','y=x+2'])
def test_degenerate_tangent_nonreal(line):
    s=TransitionState.from_facts(f'G:Parabola;H:Line;Expression(G)=(y^2=4*x);Expression(H)=({line})',ROWS[6347]['query_expressions']);app=BoundApplicator()
    assert app.apply(s,enumerate_actions(s,78)[0]).status=='applied'
    app.apply(s,enumerate_actions(s,41)[0]);before=deepcopy(s)
    assert app.apply(s,enumerate_actions(s,51)[0]).status=='inapplicable' and s==before


def test_alternate_root_variable():
    s,a=prepare();key=a.relation_id;x,y=s.symbols['x'],s.symbols['y'];f=s.intersection_reductions[key]
    s.intersection_reductions[key]=replace(f,variable=x,xy=(x,x-1),polynomial=x*x-6*x+1)
    for k in ('root_sum','root_product','discriminant','distinct_real_roots'):del s.properties[key,k]
    app=BoundApplicator();assert app.apply(s,replace(a,model_id=41,mode='derive_root_relations')).status=='applied'
    assert app.apply(s,a).status=='applied' and s.extract_answer()==8


def test_isolation():
    s,a=prepare(facts=ROWS[6347]['fact_expressions']+';J:Parabola;Expression(J)=(y^2=8*x)')
    assert BoundApplicator().apply(s,a).status=='applied'
    assert all(k[0]==a.relation_id for k in s.properties if k[1]=='chord_length')


def test_symbolic_operation_rejected():
    t,k=sp.symbols('t k',real=True)
    with pytest.raises(TransitionError):slope_chord_length(sp.Integer(4),sp.Integer(-4),(k*t,t),t)
