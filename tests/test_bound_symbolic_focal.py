from copy import deepcopy
from dataclasses import replace
import json
from pathlib import Path
import pytest
import sympy as sp
from src.state.transition_state import TransitionState
from src.theorems.bound_application import BoundApplicator, enumerate_actions
from src.reasoning.bound_slice import solve_symbolic_focal_product_slice

ROW=next(r for r in json.loads(Path('data/train_with_models_v3.json').read_text()) if r['id']==1833)
FACTS=ROW['fact_expressions']


def action(s, mid=35):
    mode={34:'derive_symbolic_axial_product',35:'derive_symbolic_transverse_product'}[mid]
    a,=enumerate_actions(s,mid,mode)
    return a


def test_original_direction_free_and_provenance():
    r=solve_symbolic_focal_product_slice(FACTS,ROW['query_expressions'])
    assert r.status=='solved',r.diagnostic
    p=r.state.symbols['p']
    assert r.answer==-p**2
    assert not r.state.frames and not r.state.values
    assert ('G','p') not in r.state.properties
    condition=next(iter(r.state.constraints))
    assert r.state.constraints[condition]==sp.Ne(p,0)
    assert 'entity:G' in r.state.provenance[condition]
    assert r.transitions[0].operations[0]['positive_geometric_parameter']==sp.Abs(p)
    before=deepcopy(r.state)
    assert BoundApplicator().apply(r.state,r.transitions[0].action).status=='no_op' and r.state==before


@pytest.mark.parametrize('extra',[';p>0',';p<0',';p!=0',';p=-2'])
def test_sign_conditions(extra):
    r=solve_symbolic_focal_product_slice(FACTS+extra,'y1*y2')
    assert r.status=='solved',r.diagnostic
    assert r.answer==-r.state.symbols['p']**2


def test_zero_conflict_rolls_back():
    s=TransitionState.from_facts(FACTS+';p=0','y1*y2');before=deepcopy(s)
    assert BoundApplicator().apply(s,action(s)).status=='conflict' and s==before


def test_output_conflict_rolls_back_condition():
    s=TransitionState.from_facts(FACTS,'y1*y2');a=action(s)
    s.properties[(a.relation_id,'y_product')]=sp.S.One;before=deepcopy(s)
    assert BoundApplicator().apply(s,a).status=='conflict' and s==before


@pytest.mark.parametrize('curve,axis',[('y^2 = 2*(p*x)','x'),('y^2 = -2*(p*x)','x'),
                                    ('x^2 = 2*(p*y)','y'),('x^2 = -2*(p*y)','y')])
def test_axes_and_signed_coefficients(curve,axis):
    s=TransitionState.from_facts(FACTS.replace('y^2 = 2*(p*x)',curve),None)
    for mid,key in [(34,axis),(35,'y' if axis=='x' else 'x')]:
        a=action(s,mid);assert BoundApplicator().apply(s,a).status=='applied'
        assert s.properties[(a.relation_id,key+'_product')]==(s.symbols['p']**2/4 if mid==34 else -s.symbols['p']**2)


@pytest.mark.parametrize('extra',[';Expression(H)=(y=x)', ';Coordinate(A)=(0,0)'])
def test_additional_geometry_is_not_silently_ignored(extra):
    s=TransitionState.from_facts(FACTS+extra,'y1*y2');before=deepcopy(s)
    assert BoundApplicator().apply(s,action(s)).status=='undetermined' and s==before


@pytest.mark.parametrize('change',[{'line':'G'},{'relation_id':'wrong'},{'mode':'derive_symbolic_axial_product'}])
def test_bad_bindings(change):
    s=TransitionState.from_facts(FACTS,'y1*y2');before=deepcopy(s)
    assert BoundApplicator().apply(s,replace(action(s),**change)).status=='inapplicable' and s==before


def test_missing_focus_and_wrong_curve_type():
    for facts in [FACTS.replace('PointOnCurve(Focus(G), H);',''),FACTS.replace('G: Parabola','G: Ellipse')]:
        try:s=TransitionState.from_facts(facts,'y1*y2')
        except ValueError:continue
        before=deepcopy(s)
        assert BoundApplicator().apply(s,action(s)).status=='inapplicable' and s==before


def test_focus_alias_sources():
    s=TransitionState.from_facts(FACTS.replace('PointOnCurve(Focus(G), H)',
        'F: Point;Focus(G)=F;PointOnCurve(F,H)'), 'y1*y2')
    r=BoundApplicator().apply(s,action(s));assert r.status=='applied'
    assert next(iter(s.focus_aliases)) in r.read_facts


@pytest.mark.parametrize('coefficient',[2,-3])
def test_independent_intersections(coefficient):
    r=solve_symbolic_focal_product_slice(FACTS,'y1*y2')
    y=sp.Symbol('t',real=True)
    roots=sp.solve(y**2-2*coefficient*(2*y+sp.Rational(coefficient,2)),y)
    assert len(roots)==2
    assert sp.simplify(roots[0]*roots[1]-r.answer.subs(r.state.symbols['p'],coefficient))==0


@pytest.mark.parametrize('coefficient',['p^2','p+1','0'])
def test_unsupported_coefficient(coefficient):
    s=TransitionState.from_facts(FACTS.replace('2*(p*x)',f'2*({coefficient})*x'),'y1*y2')
    before=deepcopy(s)
    assert BoundApplicator().apply(s,action(s)).status in ('undetermined','inapplicable') and s==before
