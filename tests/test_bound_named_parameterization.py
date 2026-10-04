from copy import deepcopy
from dataclasses import replace
import json
from pathlib import Path
import pytest
import sympy as sp
from src.state.transition_state import TransitionState, EquationFact
from src.theorems.bound_application import BoundApplicator, enumerate_actions


def initial():
    r=next(r for r in json.loads(Path('data/train_with_models_v3.json').read_text()) if r['id']==56)
    return TransitionState.from_facts(r['fact_expressions'],r['query_expressions'])


def action(s):
    return enumerate_actions(s,78,'parameterize_named_line')[0]


def test_original_atomic_outputs_and_repeat():
    s=initial();a=action(s);r=BoundApplicator().apply(s,a)
    assert r.status=='applied',r.diagnostic
    p=s.parameterizations[a.line];u=p.parameter;y=s.symbols['y'];x=s.symbols['x']
    f,=s.intersection_reductions.values()
    assert sp.expand(f.polynomial-(y*y-2*u*y-2))==0
    assert f.named_points==('A','B') and f.intersection_id=='f8' and f.xy==(u*y+1,y)
    assert sp.expand(s.equations[p.line_equation_id].expression-(x-u*y-1))==0
    assert set(r.delta)>={'equations','intersection_reductions','parameterizations'}
    assert {'f5','f6','f7','f8'}.issubset(s.provenance[f.fact_id])
    assert r.operations[0]['distinct_intersections']==1
    assert not s.values and not s.properties and s.extract_answer() is None
    before=deepcopy(s);assert BoundApplicator().apply(s,a).status=='no_op' and s==before
    for value in (-2,0,3):
        for root in sp.solve(f.polynomial.subs(u,value),y):
            xy=[v.subs({u:value,y:root}, simultaneous=True) for v in f.xy]
            assert sp.simplify(xy[1]**2-2*xy[0])==0


@pytest.mark.parametrize('change',[{'relation_id':'bad'},{'incidence_id':'bad'},{'coordinate_id':'bad'},
                                  {'line':'bad'},{'point':'O'},{'line_equation_id':'f5'}])
def test_invalid_bindings(change):
    s=initial();before=deepcopy(s)
    assert BoundApplicator().apply(s,replace(action(s),**change)).status=='inapplicable' and s==before


def test_unsupported_axis_rolls_back():
    s=initial();f=s.equations['f5'];x,y=s.symbols['x'],s.symbols['y']
    s.equations['f5']=replace(f,expression=x*x-2*y)
    before=deepcopy(s)
    assert BoundApplicator().apply(s,action(s)).status=='inapplicable' and s==before


def test_parameter_scope_and_no_global_collision():
    s=initial();s.symbols['u']=sp.Symbol('u',real=True)
    app=BoundApplicator();assert app.apply(s,action(s)).status=='applied'
    assert next(iter(s.parameterizations.values())).parameter != s.symbols['u']
    from src.state.named_line_facts import register_named_line, NamedIntersection
    s.entities.update(C='Point',D='Point')
    line=register_named_line(s,'C','D','test')
    s.named_intersections['other']=NamedIntersection('other',line,'G',('C','D'),'test')
    s.incidences['other_on']=replace(s.incidences['f7'],fact_id='other_on',curve=line)
    b=next(a for a in enumerate_actions(s,78,'parameterize_named_line') if a.line==line)
    assert app.apply(s,b).status=='applied'
    assert len({v.parameter for v in s.parameterizations.values()})==2


@pytest.mark.parametrize('target',['line','reduction','parameter'])
def test_conflicts_commit_nothing(target):
    s=initial();a=action(s);app=BoundApplicator();assert app.apply(s,a).status=='applied'
    if target=='line':
        key=s.parameterizations[a.line].line_equation_id
        s.equations[key]=replace(s.equations[key],expression=sp.S.One)
    elif target=='reduction':
        key=next(iter(s.intersection_reductions))
        s.intersection_reductions[key]=replace(s.intersection_reductions[key],named_points=('B','A'))
    else:
        s.parameterizations[a.line]=replace(s.parameterizations[a.line],parameter=sp.Symbol('wrong',real=True))
    before=deepcopy(s)
    assert app.apply(s,a).status=='conflict' and s==before


def test_vertex_requires_nonzero_parameter_for_two_intersections():
    s=initial();s.coordinates['M']=replace(s.coordinates['M'],xy=(sp.S.Zero,sp.S.Zero))
    r=BoundApplicator().apply(s,action(s));assert r.status=='applied'
    u=next(iter(s.parameterizations.values())).parameter
    guard=next(v for k,v in s.constraints.items() if k.endswith(':distinct_roots'))
    assert guard.subs(u,0)==sp.false and guard.subs(u,1)==sp.true


def test_missing_intersection_or_through_point_has_no_candidate():
    s=initial();s.named_intersections.clear()
    assert not enumerate_actions(s,78,'parameterize_named_line')
    s=initial();s.coordinates.clear()
    assert not enumerate_actions(s,78,'parameterize_named_line')
