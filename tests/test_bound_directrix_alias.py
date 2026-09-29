"""Named directrix identity, without hidden equation generation in queries."""
from copy import deepcopy
from dataclasses import replace
import json
from pathlib import Path

import pytest
import sympy as sp
from src.state.transition_state import TransitionState
from src.theorems.bound_application import BoundApplicator, enumerate_actions
from src.reasoning.bound_slice import solve_directrix_alias_distance_slice

FACTS = 'l: Line;G: Parabola;Expression(G)=(y=4*x^2);Directrix(G)=l;A: Point;Coordinate(A)=(1,4)'
QUERY = 'Distance(A, l)'


def test_original_id3723_and_only_recorded_computation():
    row=next(r for r in json.loads(Path('data/train_with_models_v3.json').read_text()) if r['id']==3723)
    r=solve_directrix_alias_distance_slice(row['fact_expressions'],row['query_expressions'])
    assert r.status=='solved' and r.answer==sp.Rational(65,16)
    assert [t.action.model_id for t in r.transitions]==[9,29,52]
    assert r.state.properties['G','p']==sp.Rational(1,8)
    assert r.state.equations['derived:G:directrix'].expression==r.state.symbols['y']+sp.Rational(1,16)
    assert len(r.state.equations)==2  # No duplicate equation owned by alias l.
    last=r.transitions[-1]
    assert last.action.line=='l' and last.action.relation_id=='f3'
    assert {'f3','derived:G:directrix'} <= set(last.read_facts)
    assert last.operations[0]['operation']=='resolve_directrix_alias'
    before=deepcopy(r.state)
    for t in r.transitions:
        assert BoundApplicator().apply(r.state,t.action).status=='no_op'
    assert r.state==before


def test_initial_state_and_rm29_dependency():
    s=TransitionState.from_facts(FACTS,QUERY)
    assert len(s.directrix_aliases)==1 and not s.properties and not s.frames
    assert s.line_bindings('l')==[] and s.extract_answer() is None
    assert not [a for a in enumerate_actions(s,52) if a.line=='l']
    app=BoundApplicator()
    assert app.apply(s,enumerate_actions(s,9,'extract_parameters')[0]).status=='applied'
    assert s.line_bindings('l')==[]
    assert app.apply(s,enumerate_actions(s,29)[0]).status=='applied'
    assert s.extract_answer() is None
    action=next(a for a in enumerate_actions(s,52) if a.line=='l')
    for bad in (replace(action,relation_id=None),replace(action,relation_id='wrong'),
                replace(action,line_equation_id='f2'),replace(action,line='missing')):
        before=deepcopy(s)
        assert app.apply(s,bad).status=='inapplicable' and s==before
    assert app.apply(s,action).status=='applied' and s.extract_answer()==sp.Rational(65,16)


@pytest.mark.parametrize('eq,mid', [('y^2=4*x',7),('y^2=-4*x',8),('x^2=4*y',9),('x^2=-4*y',10)])
def test_four_directions_and_point_need_not_lie_on_curve(eq,mid):
    r=solve_directrix_alias_distance_slice(FACTS.replace('y=4*x^2',eq).replace('(1,4)','(0,0)'),QUERY)
    assert r.status=='solved' and r.answer==1 and r.transitions[0].action.model_id==mid
    assert not r.state.incidences


def test_two_curves_do_not_cross_bind():
    facts=FACTS+';H: Parabola;Expression(H)=(x^2=4*y);h: Line;Directrix(H)=h'
    r=solve_directrix_alias_distance_slice(facts,'Distance(A, h)')
    assert r.status=='solved' and r.answer==5
    assert 'derived:G:directrix' not in r.state.equations
    assert r.state.line_bindings('l')==[]


@pytest.mark.parametrize('extra', [';Directrix(G)=l', ';Expression(l)=(y=-1/16)',
                                   ';Expression(l)=(y=5)',
                                   ';H: Parabola;Expression(H)=(x^2=4*y);Directrix(H)=l'])
def test_ambiguous_alias_or_additional_equation_not_silently_selected(extra):
    r=solve_directrix_alias_distance_slice(FACTS+extra,QUERY)
    assert r.status=='undetermined' and r.answer is None and not r.state.history
    assert r.state.line_bindings('l')==[]


@pytest.mark.parametrize('facts',[FACTS.replace('G: Parabola','G: Ellipse'),
                                  FACTS.replace('l: Line','l: Point'),
                                  FACTS.replace('Directrix(G)=l','Directrix(missing)=l')])
def test_alias_types(facts):
    assert solve_directrix_alias_distance_slice(facts,QUERY).status=='failed'


def test_conflicting_directrix_rolls_back():
    s=TransitionState.from_facts(FACTS,QUERY);app=BoundApplicator()
    app.apply(s,enumerate_actions(s,9,'extract_parameters')[0])
    action=enumerate_actions(s,29)[0]
    app.apply(s,action)
    f=s.equations['derived:G:directrix']
    s.equations[f.fact_id]=replace(f,expression=s.symbols['y']+3)
    before=deepcopy(s)
    assert app.apply(s,action).status=='conflict' and s==before


def test_missing_coordinate_or_alias():
    for facts in (FACTS.replace(';Coordinate(A)=(1,4)',''),FACTS.replace(';Directrix(G)=l','')):
        r=solve_directrix_alias_distance_slice(facts,QUERY)
        assert r.status=='undetermined' and r.answer is None
