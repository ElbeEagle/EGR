from copy import deepcopy
from dataclasses import replace
import json
from pathlib import Path
import pytest
import sympy as sp
from src.state.transition_state import TransitionState
from src.state.point_pair_distance import PointPairDistanceQuery
from src.theorems.bound_application import BoundApplicator,enumerate_actions
from src.solver.point_pair_operations import point_pair_distance
from src.solver.transition_primitives import TransitionError

FACTS='A:Point;B:Point;Coordinate(A)=(-1,0);Coordinate(B)=(2,4)'


def prepare(facts=FACTS,query='Distance(A,B)'):
    s=TransitionState.from_facts(facts,query);assert s.extract_answer() is None
    return s,enumerate_actions(s,53)[0]


@pytest.mark.parametrize('pid,names,expected',[(1199,('A','B'),sp.Integer(5)),(5211,('E','F'),2*sp.sqrt(13))])
@pytest.mark.parametrize('reverse',[False,True])
def test_real(pid,names,expected,reverse):
    row=next(r for r in json.loads(Path('data/train_with_models_v3.json').read_text()) if r['id']==pid)
    parts=[p.strip() for p in row['fact_expressions'].split(';')]
    parts=[p for p in parts if any(p==f'{n}: Point' or p.startswith(f'Coordinate({n})') for n in names)]
    if reverse:parts.reverse();names=names[::-1]
    s,a=prepare(';'.join(parts),f'Distance({names[0]},{names[1]})');app=BoundApplicator()
    t=app.apply(s,a);assert t.status=='applied',t.diagnostic
    assert s.extract_answer()==expected and not s.named_lines and not s.equations
    s.query=PointPairDistanceQuery(s.query.points[::-1]);before=deepcopy(s)
    assert app.apply(s,enumerate_actions(s,53)[0]).status=='no_op' and s==before


@pytest.mark.parametrize('facts,query,value',[(FACTS,'Distance(A,A)',0),('A:Point;B:Point;Coordinate(A)=(1,1);Coordinate(B)=(1,1)','Distance(A,B)',0),('A:Point;B:Point;Coordinate(A)=(0,2);Coordinate(B)=(3,2)','Distance(A,B)',3),('A:Point;B:Point;Coordinate(A)=(2,0);Coordinate(B)=(2,4)','Distance(A,B)',4)])
def test_zero_axes(facts,query,value):
    s,a=prepare(facts,query);assert BoundApplicator().apply(s,a).status=='applied';assert s.extract_answer()==value


@pytest.mark.parametrize('damage',['id','value','source','missing','binding','extra','other_model'])
def test_old_action(damage):
    s,a=prepare()
    if damage=='id':s.coordinates['A']=replace(s.coordinates['A'],fact_id='other')
    if damage=='value':s.coordinates['A']=replace(s.coordinates['A'],xy=(sp.S.Zero,sp.S.Zero))
    if damage=='source':s.provenance[s.coordinates['A'].fact_id]=()
    if damage=='missing':del s.coordinates['A']
    if damage=='binding':a=replace(a,coordinate_ids=a.coordinate_ids[::-1])
    if damage=='extra':a=replace(a,line='L')
    if damage=='other_model':a=replace(a,model_id=73)
    before=deepcopy(s);assert BoundApplicator().apply(s,a).status=='inapplicable' and s==before


@pytest.mark.parametrize('damage',['same_distance','source','evidence','property','property_source'])
def test_stale_read(damage):
    s,a=prepare();app=BoundApplicator();assert app.apply(s,a).status=='applied';key=(s.query.owner,'distance')
    if damage=='same_distance':
        for p in ('A','B'):
            c=s.coordinates[p];s.coordinates[p]=replace(c,xy=(c.xy[0]+1,c.xy[1]))
    if damage=='source':s.provenance[s.coordinates['A'].fact_id]=()
    if damage=='evidence':s.point_pair_snapshots.clear()
    if damage=='property':s.properties[key]=sp.Integer(99)
    if damage=='property_source':s.provenance[f'property:{key[0]}:{key[1]}']=()
    before=deepcopy(s);assert s.extract_answer() is None and s==before
    actions=enumerate_actions(s,53)
    if actions:assert app.apply(s,actions[0]).status in ('inapplicable','conflict') and s==before


def test_conflict_and_pair_isolation():
    s,a=prepare(FACTS+';C:Point;Coordinate(C)=(8,0)');app=BoundApplicator();key=(s.query.owner,'distance')
    s.properties[key]=sp.Integer(99);before=deepcopy(s)
    assert app.apply(s,a).status=='conflict' and s==before and not s.point_pair_snapshots
    del s.properties[key];assert app.apply(s,a).status=='applied'
    s.query=PointPairDistanceQuery(('A','C'));assert s.extract_answer() is None
    assert app.apply(s,enumerate_actions(s,53)[0]).status=='applied' and s.extract_answer()==9


@pytest.mark.parametrize('v',[sp.oo,sp.I,sp.Symbol('a',real=True)])
def test_invalid_numeric(v):
    with pytest.raises(TransitionError):point_pair_distance((v,sp.S.Zero),(sp.S.One,sp.S.One))


def test_missing_query_coordinates():
    s=TransitionState.from_facts('A:Point;B:Point','Distance(A,B)')
    assert s.extract_answer() is None and enumerate_actions(s,53)==[]
