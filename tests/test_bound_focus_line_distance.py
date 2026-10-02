"""Focus properties are inputs to RM52; query reading never solves parameters."""
from copy import deepcopy
from dataclasses import replace
import json
from pathlib import Path
import pytest
import sympy as sp
from src.state.transition_state import TransitionState,FocusLineDistanceQuery
from src.theorems.bound_application import BoundApplicator,enumerate_actions
from src.reasoning.bound_slice import solve_intersection_focus_distance_slice


def row():
    return next(r for r in json.loads(Path('data/train_with_models_v3.json').read_text()) if r['id']==7260)


def make_state():
    r=row();s=TransitionState.from_facts(r['fact_expressions'],r['query_expressions'])
    return s,BoundApplicator(),enumerate_actions(s,52,'focus_line_distance')[0]


def test_real_original_query():
    p=row();r=solve_intersection_focus_distance_slice(p['fact_expressions'],p['query_expressions'])
    assert r.status=='solved' and r.answer==2*sp.sqrt(5)/5
    assert [t.action.model_id for t in r.transitions]==[7,72,52]
    assert r.state.values=={r.state.symbols['p']:2,r.state.symbols['a']:2}
    assert len(r.state.coordinates)==1 and not r.state.focus_aliases
    t=r.transitions[-1]
    assert t.action.point is None and t.action.point_role=='focus'
    assert {'property:G:focus_x','property:G:focus_y','frame:G','value:a','f1'}<=set(t.read_facts)
    before=deepcopy(r.state)
    assert BoundApplicator().apply(r.state,t.action).status=='no_op' and r.state==before


def test_missing_prerequisites_and_read_only_query():
    s,app,d=make_state();before=deepcopy(s)
    assert isinstance(s.query,FocusLineDistanceQuery)
    assert s.extract_answer() is None and s==before
    assert app.apply(s,d).status=='inapplicable' and s==before
    app.apply(s,enumerate_actions(s,7,'recover_from_point')[0]);before=deepcopy(s)
    assert app.apply(s,d).status=='undetermined' and s==before
    app.apply(s,enumerate_actions(s,72)[0]);before=deepcopy(s)
    assert s.extract_answer() is None and s==before
    assert app.apply(s,d).status=='applied'


def test_reverse_recovery_order():
    s,app,d=make_state()
    for mid in (72,7):assert app.apply(s,enumerate_actions(s,mid,'recover_from_point')[0]).status=='applied'
    assert app.apply(s,d).status=='applied' and s.extract_answer()==2*sp.sqrt(5)/5


@pytest.mark.parametrize('changes',[{'point':'F'},{'coordinate_id':'f7'},{'point_role':'center'},
                                   {'curve':'H'},{'line':'G'},{'equation_id':'f1'},
                                   {'line_equation_id':'f4'},{'relation_id':'f7'}])
def test_wrong_bindings(changes):
    s,app,d=make_state();before=deepcopy(s)
    assert app.apply(s,replace(d,**changes)).status=='inapplicable' and s==before


@pytest.mark.parametrize('key,value',[('focus_x',99),('p',3)])
def test_corrupt_properties_rejected(key,value):
    s,app,d=make_state()
    for mid in (7,72):app.apply(s,enumerate_actions(s,mid,'recover_from_point')[0])
    s.properties['G',key]=sp.Integer(value);before=deepcopy(s)
    assert app.apply(s,d).status=='conflict' and s==before


def test_query_curve_isolation_and_zero_distance():
    facts='G: Parabola;Expression(G)=(y^2=4*x);J: Parabola;Expression(J)=(y^2=8*x);H: Line;Expression(H)=(x=1)'
    s=TransitionState.from_facts(facts,'Distance(Focus(G), H)');app=BoundApplicator()
    for a in enumerate_actions(s,7,'extract_parameters'):assert app.apply(s,a).status=='applied'
    d=next(a for a in enumerate_actions(s,52,'focus_line_distance') if a.curve=='G')
    assert app.apply(s,d).status=='applied' and s.extract_answer()==0
    s.query=FocusLineDistanceQuery('J','H');assert s.extract_answer() is None


def test_ambiguous_witness_does_not_pick_first():
    p=row()
    r=solve_intersection_focus_distance_slice(p['fact_expressions']+';Coordinate(OneOf(Intersection(H,G)))=(2,3)',p['query_expressions'])
    assert r.status=='undetermined' and not r.state.history
