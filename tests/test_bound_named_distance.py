from copy import deepcopy
from dataclasses import replace
import json
from pathlib import Path
import pytest
import sympy as sp
from src.state.transition_state import TransitionState
from src.theorems.bound_application import BoundApplicator, enumerate_actions

ROWS={r['id']:r for r in json.loads(Path('data/train_with_models_v3.json').read_text())}
CASES={870:('H','F1','F2'),3239:('F1','F2','Z')}
FACTS='P:Point;A:Point;B:Point;Coordinate(P)=(0,3);Coordinate(A)=(-2,0);Coordinate(B)=(2,0)'


def prepare(facts=FACTS,query='Distance(P,LineOf(A,B))'):
    s=TransitionState.from_facts(facts,query);app=BoundApplicator()
    assert s.extract_answer() is None
    assert app.apply(s,next(a for a in enumerate_actions(s,73) if a.line==s.query.line)).status=='applied'
    a=next(a for a in enumerate_actions(s,52) if a.line==s.query.line and a.point==s.query.point)
    return s,a


@pytest.mark.parametrize('pid,value',[(870,sp.Integer(3)),(3239,6*sp.sqrt(10)/5)])
@pytest.mark.parametrize('reverse',[False,True])
def test_real_projections(pid,value,reverse):
    point,first,second=CASES[pid];names=(point,first,second)
    parts=[p.strip() for p in ROWS[pid]['fact_expressions'].split(';')]
    parts=[p for p in parts if any(p==f'{n}: Point' or p.startswith(f'Coordinate({n})') for n in names)]
    if reverse:parts.reverse();first,second=second,first
    s,a=prepare(';'.join(parts),f'Distance({point},LineOf({first},{second}))');app=BoundApplicator()
    t=app.apply(s,a);assert t.status=='applied',t.diagnostic
    assert sp.simplify(s.extract_answer()-value)==0 and len(s.distance_snapshots)==1
    before=deepcopy(s);assert app.apply(s,a).status=='no_op' and s==before


@pytest.mark.parametrize('damage',['endpoint','point','line','line_source','coord_source','distance_source','evidence','value','multiple'])
def test_stale_read(damage):
    s,a=prepare();app=BoundApplicator();assert app.apply(s,a).status=='applied'
    key=next(iter(s.distance_snapshots))
    if damage in ('endpoint','point'):
        name='A' if damage=='endpoint' else 'P';old=s.coordinates[name];s.coordinates[name]=replace(old,xy=(old.xy[0],old.xy[1]+1))
    if damage=='line':s.equations[a.line_equation_id]=replace(s.equations[a.line_equation_id],expression=s.symbols['y']-1)
    if damage=='line_source':s.equations[a.line_equation_id]=replace(s.equations[a.line_equation_id],source='removed')
    if damage=='coord_source':s.provenance[a.coordinate_id]=()
    if damage=='distance_source':s.provenance[f'property:{key[0]}:{key[1]}']=()
    if damage=='evidence':s.distance_snapshots.clear()
    if damage=='value':s.properties[key]=sp.Integer(99)
    if damage=='multiple':s.equations['other']=replace(s.equations[a.line_equation_id],fact_id='other')
    before=deepcopy(s);assert s.extract_answer() is None and s==before
    assert app.apply(s,a).status in ('inapplicable','conflict') and s==before


@pytest.mark.parametrize('damage',['endpoint','point_source','line_source'])
def test_reject_before_distance(damage):
    s,a=prepare()
    if damage=='endpoint':s.coordinates['A']=replace(s.coordinates['A'],xy=(sp.S.Zero,sp.S.One))
    if damage=='point_source':s.provenance[a.coordinate_id]=()
    if damage=='line_source':s.provenance[a.line_equation_id]=()
    before=deepcopy(s);assert BoundApplicator().apply(s,a).status=='inapplicable' and s==before
    assert not s.distance_snapshots


@pytest.mark.parametrize('query,value',[('Distance(A,LineOf(A,B))',0),('Distance(P,LineOf(B,A))',3)])
def test_zero_and_reversed(query,value):
    s,a=prepare(query=query);assert BoundApplicator().apply(s,a).status=='applied';assert s.extract_answer()==value


def test_vertical_scale_isolation():
    facts=FACTS.replace('(-2,0)','(2,0)').replace('(2,0)','(2,4)',1)
    s,a=prepare(facts);app=BoundApplicator();assert app.apply(s,a).status=='applied';assert s.extract_answer()==2
    f=s.equations[a.line_equation_id];s.equations[a.line_equation_id]=replace(f,expression=3*f.expression)
    assert s.extract_answer()==2
    assert app.apply(s,a).status=='no_op'
    before=deepcopy(s);assert app.apply(s,replace(a,point='A')).status=='inapplicable' and s==before


def test_conflict_rolls_back_evidence():
    s,a=prepare();key=(a.line,f'point_line_distance:{a.point}:{a.line_equation_id}');s.properties[key]=sp.Integer(99)
    before=deepcopy(s);assert BoundApplicator().apply(s,a).status=='conflict' and s==before
    assert not s.distance_snapshots


def test_new_line_cannot_revive_old_distance():
    s,a=prepare();app=BoundApplicator();assert app.apply(s,a).status=='applied'
    s.coordinates['A']=replace(s.coordinates['A'],xy=(-sp.S.One,sp.S.Zero))
    del s.equations[a.line_equation_id]
    assert app.apply(s,enumerate_actions(s,73)[0]).status=='applied'
    assert s.extract_answer() is None
    before=deepcopy(s);assert app.apply(s,a).status=='inapplicable' and s==before
