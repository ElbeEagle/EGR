from copy import deepcopy
from dataclasses import replace
import json
from pathlib import Path
import pytest
import sympy as sp
from src.state.transition_state import TransitionState
from src.theorems.bound_application import BoundApplicator,enumerate_actions
from src.reasoning.bound_slice import solve_parabola_tangent_slice

FACTS='G: Parabola;Expression(G)=(y=x^2);H: Point;Coordinate(H)=(-1,1)'
QUERY='Expression(TangentOnPoint(H, G))'


def test_original_and_read_only():
    row=next(r for r in json.loads(Path('data/train_with_models_v3.json').read_text()) if r['id']==2106)
    r=solve_parabola_tangent_slice(row['fact_expressions'],row['query_expressions'])
    assert r.status=='solved' and [t.action.model_id for t in r.transitions]==[9,39]
    x,y=r.state.symbols['x'],r.state.symbols['y']
    assert sp.simplify(r.answer/(-2*x-y-1))==sp.Rational(1,2)
    assert len(r.state.incidences)==0
    assert r.transitions[-1].operations[0]['residual']==0
    before=deepcopy(r.state)
    assert BoundApplicator().apply(r.state,r.transitions[-1].action).status=='no_op' and r.state==before
    s=TransitionState.from_facts(FACTS,QUERY);assert s.extract_answer() is None


@pytest.mark.parametrize('eq,xy',[('y^2=4*x',(1,2)),('y^2=-4*x',(-1,2)),
                                  ('x^2=4*y',(2,1)),('x^2=-4*y',(2,-1)),
                                  ('y^2=4*x',(0,0)),('y^2=-4*x',(0,0)),
                                  ('x^2=4*y',(0,0)),('x^2=-4*y',(0,0))])
def test_gradient_oracle_all_directions_and_vertices(eq,xy):
    facts=FACTS.replace('y=x^2',eq).replace('(-1,1)',str(xy))
    r=solve_parabola_tangent_slice(facts,QUERY);assert r.status=='solved'
    x,y=r.state.symbols['x'],r.state.symbols['y'];f=r.state.equations['f1'].expression
    at={x:xy[0],y:xy[1]}
    gradient=sp.diff(f,x).subs(at)*(x-xy[0])+sp.diff(f,y).subs(at)*(y-xy[1])
    ratio=sp.cancel(r.answer/gradient)
    assert not ratio.free_symbols and ratio!=0 and r.answer.subs(at)==0


def test_missing_frame_off_curve_and_rollback():
    s=TransitionState.from_facts(FACTS,QUERY);app=BoundApplicator();a=enumerate_actions(s,39)[0]
    before=deepcopy(s);assert app.apply(s,a).status=='inapplicable' and s==before
    app.apply(s,enumerate_actions(s,9,'extract_parameters')[0]);assert s.extract_answer() is None
    s.coordinates['H']=replace(s.coordinates['H'],xy=(sp.S.One,sp.Integer(2)))
    before=deepcopy(s);assert app.apply(s,a).status=='conflict' and s==before


@pytest.mark.parametrize('changes',[{'curve':'missing'},{'coordinate_id':'bad'},{'point':'bad'},
                                   {'equation_id':'f3'},{'line':'L'},{'mode':'inverse'}])
def test_wrong_binding(changes):
    s=TransitionState.from_facts(FACTS,QUERY);app=BoundApplicator();a=enumerate_actions(s,39)[0]
    before=deepcopy(s);assert app.apply(s,replace(a,**changes)).status=='inapplicable' and s==before


def test_conflicting_output_and_point_isolation():
    facts=FACTS+';P: Point;Coordinate(P)=(1,1)'
    r=solve_parabola_tangent_slice(facts,QUERY);s=r.state;app=BoundApplicator()
    p=next(a for a in enumerate_actions(s,39) if a.point=='P')
    assert app.apply(s,p).status=='applied' and len([f for f in s.equations.values() if f.role=='tangent'])==2
    key='derived:G:tangent:H';s.equations[key]=replace(s.equations[key],expression=sp.S.One)
    before=deepcopy(s);assert app.apply(s,r.transitions[-1].action).status=='conflict' and s==before
