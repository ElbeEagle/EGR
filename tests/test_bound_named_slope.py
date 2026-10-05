from copy import deepcopy
from dataclasses import replace
import json
from pathlib import Path
import pytest
import sympy as sp
from src.state.transition_state import TransitionState
from src.theorems.bound_application import BoundApplicator,enumerate_actions
from src.reasoning.bound_slice import solve_named_slope_slice
from src.solver.intersection_operations import quadratic_root_relation
from src.solver.transition_primitives import TransitionError


def row():
    return next(r for r in json.loads(Path('data/train_with_models_v3.json').read_text()) if r['id']==56)


def prepared(order=(42,43), facts=None):
    r=row();s=TransitionState.from_facts(facts or r['fact_expressions'],r['query_expressions']);app=BoundApplicator()
    assert app.apply(s,enumerate_actions(s,78,'parameterize_named_line')[0]).status=='applied'
    for mid in order: assert app.apply(s,enumerate_actions(s,mid)[0]).status=='applied'
    return s


def test_original_result_reduction_and_repeat():
    r=row();result=solve_named_slope_slice(r['fact_expressions'],r['query_expressions'])
    assert result.status=='solved',result.diagnostic
    s=result.state;x,y=s.symbols['x'],s.symbols['y']
    assert sp.simplify(result.answer-(x+y/2-1))==0
    assert [t.action.model_id for t in result.transitions]==[78,42,43,55]
    u=next(iter(s.parameterizations.values())).parameter
    assert s.values[u]==-sp.Rational(1,2)
    f,=s.intersection_reductions.values()
    assert sp.expand(f.polynomial-(y*y+y-2))==0 and f.xy==(1-y/2,y)
    assert s.properties[(f.fact_id,'root_sum')]==-1
    assert s.properties[(f.fact_id,'root_product')]==-2
    assert any(o.get('intersection')==f.fact_id for o in result.transitions[-1].operations)
    assert 'f8' in s.provenance[f.fact_id] and 'f9' in s.provenance[f.fact_id]
    # Independent solution of final original curve and committed line.
    pts=sp.solve([s.equations['f5'].expression,result.answer],(x,y))
    assert sp.simplify(sum(py/px for px,py in pts))==1
    assert result.answer.subs({x:1,y:0})==0
    before=deepcopy(s)
    for t in result.transitions:
        q=BoundApplicator().apply(s,t.action)
        assert q.status=='no_op',q.diagnostic
    assert s==before and s.extract_answer()==result.answer


def test_symbolic_relations_and_reverse_order():
    s=prepared((43,42));f,=s.intersection_reductions.values();u=next(iter(s.parameterizations.values())).parameter
    assert s.properties[(f.fact_id,'root_sum')]==2*u and s.properties[(f.fact_id,'root_product')]==-2
    assert s.properties[(f.fact_id,'distinct_real_roots')]==2 and s.extract_answer() is None
    assert BoundApplicator().apply(s,enumerate_actions(s,55)[0]).status=='applied'


@pytest.mark.parametrize('order',[(),(42,),(43,)])
def test_no_hidden_vieta(order):
    s=prepared(order);before=deepcopy(s)
    assert BoundApplicator().apply(s,enumerate_actions(s,55)[0]).status=='inapplicable' and s==before


def test_zero_denominator_rejected():
    s=prepared(facts=row()['fact_expressions'].replace('Coordinate(M) = (1, 0)','Coordinate(M) = (0, 0)'))
    before=deepcopy(s)
    assert BoundApplicator().apply(s,enumerate_actions(s,55)[0]).status=='inapplicable' and s==before


@pytest.mark.parametrize('change',[{'slope_sum_id':'bad'},{'relation_id':'bad'},{'line':'bad'},
                                  {'coordinate_id':'bad'},{'mode':'bad'}])
def test_wrong_binding(change):
    s=prepared();before=deepcopy(s)
    assert BoundApplicator().apply(s,replace(enumerate_actions(s,55)[0],**change)).status=='inapplicable' and s==before


@pytest.mark.parametrize('kind',['root_sum','root_product','discriminant','constraint','base'])
def test_conflicts_or_unsupported_base(kind):
    s=prepared();f,=s.intersection_reductions.values();u=next(iter(s.parameterizations.values())).parameter
    if kind=='constraint': s.constraints['probe']=sp.Gt(u,0)
    elif kind=='base': s.coordinates['O']=replace(s.coordinates['O'],xy=(sp.S.One,sp.S.Zero))
    else:s.properties[(f.fact_id,kind)]=sp.Integer(999)
    before=deepcopy(s);result=BoundApplicator().apply(s,enumerate_actions(s,55)[0])
    assert result.status==('inapplicable' if kind=='base' else 'conflict') and s==before


def test_unscoped_symbol_and_symbolic_leading_coefficient_rejected():
    y,u,v=sp.symbols('y u v',real=True)
    for expr,params in [(y*y+v*y+1,(u,)),(u*y*y+y+1,(u,))]:
        with pytest.raises(TransitionError):quadratic_root_relation(expr,y,'sum',params)


def test_missing_or_multiple_slope_constraints_not_arbitrarily_selected():
    r=row();facts=r['fact_expressions'].rsplit(';',1)[0]
    assert solve_named_slope_slice(facts,r['query_expressions']).status=='undetermined'
    assert solve_named_slope_slice(r['fact_expressions']+';'+r['fact_expressions'].split(';')[-1],r['query_expressions']).status=='undetermined'
