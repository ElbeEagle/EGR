"""Design audit for RM73-to-RM52 consumption; all queries are explicit projections."""
from copy import deepcopy
from dataclasses import replace
import hashlib
import json
from pathlib import Path
import sympy as sp
from src.state.transition_state import TransitionState, PointLineDistanceQuery
from src.state.two_point_line_facts import fresh_two_point_line
from src.theorems.bound_application import BoundApplicator, enumerate_actions

ROOT=Path(__file__).resolve().parents[2]
CASES={870:('H','F1','F2'),3239:('F1','F2','Z')}


def probe(facts, point, first, second):
    query=f'Distance({point},LineOf({first},{second}))'
    try:
        TransitionState.from_facts(facts,query)
        query_gap=None
    except ValueError as exc:
        query_gap=str(exc)
    s=TransitionState.from_facts(facts,f'Expression(LineOf({first},{second}))')
    app=BoundApplicator();a=enumerate_actions(s,73)[0]
    assert app.apply(s,a).status=='applied'
    line=s.equations[f'derived:{a.line}:two_points']
    # Internal typed query is a diagnostic bypass, not raw query support.
    s.query=PointLineDistanceQuery(point,a.line)
    action=next(v for v in enumerate_actions(s,52) if v.line==a.line and v.point==point)
    before=deepcopy(s)
    result=app.apply(s,action);assert result.status=='applied',result.diagnostic
    points=[s.coordinates[n].xy for n in (point,first,second)]
    p,u,v=points;dx,dy=v[0]-u[0],v[1]-u[1]
    oracle=sp.simplify(abs(dx*(p[1]-u[1])-dy*(p[0]-u[0]))/sp.sqrt(dx*dx+dy*dy))
    assert sp.simplify(s.extract_answer()-oracle)==0
    stale_point=deepcopy(s)
    old=stale_point.coordinates[point]
    stale_point.coordinates[point]=replace(old,xy=(old.xy[0],old.xy[1]+1))
    stale_line=deepcopy(before)
    old=stale_line.coordinates[first]
    stale_line.coordinates[first]=replace(old,xy=(old.xy[0],old.xy[1]+1))
    assert not fresh_two_point_line(stale_line,line)
    stale_result=app.apply(stale_line,action)
    return dict(diagnostic_query=query,raw_query_gap=query_gap,internal_typed_query_bypass=True,
                baseline_distance=str(oracle),executed_models=[73,52],
                after_target_coordinate_change_read=str(stale_point.extract_answer()),
                stale_line_application_status=stale_result.status,
                stale_line_read=str(stale_line.extract_answer()))


def audit():
    raw=(ROOT/'data/train_with_models_v3.json').read_bytes();rows={r['id']:r for r in json.loads(raw)};cases=[]
    for pid,names in CASES.items():
        r=rows[pid];parts=[p.strip() for p in r['fact_expressions'].split(';')]
        selected=[p for p in parts if any(p==f'{n}: Point' or p.startswith(f'Coordinate({n})') for n in names)]
        facts=';'.join(selected)
        cases.append(dict(id=pid,original_facts=r['fact_expressions'],original_query=r['query_expressions'],
                          projected_facts=facts,probe=probe(facts,*names)))
    assert cases[0]['probe']['baseline_distance']=='3'
    assert sp.simplify(sp.sympify(cases[1]['probe']['baseline_distance'])-6*sp.sqrt(10)/5)==0
    deferred = dict(id=6261, reason='Numeric sqrt(11) coordinate syntax unsupported; no parser expansion this batch')
    return dict(deferred=deferred, stage='design_audit_fact_projections_not_original_solves',dataset_sha256=hashlib.sha256(raw).hexdigest(),cases=cases)


if __name__=='__main__':
    report=audit()
    (ROOT/'docs/开发规格/artifacts/named_line_distance_contract.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print('870: 3; 3239: 6*sqrt(10)/5; raw query and stale-state behavior recorded')
