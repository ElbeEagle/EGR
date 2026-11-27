"""Finite RM53 design audit on explicit coordinate projections."""
import hashlib
import json
from pathlib import Path
import sympy as sp
from src.state.transition_state import TransitionState

ROOT=Path(__file__).resolve().parents[2]
CASES={1199:('A','B'),5211:('E','F')}


def probe(facts, names):
    query=f'Distance({names[0]},{names[1]})'
    try:
        TransitionState.from_facts(facts,query)
        gap=None
    except ValueError as exc:
        gap=str(exc)
    state=TransitionState.from_facts(facts,None)
    coordinates=[state.coordinates[p] for p in names]
    assert all(state.provenance.get(c.fact_id) for c in coordinates)
    first,second=(c.xy for c in coordinates)
    squared=sp.simplify(sum((a-b)**2 for a,b in zip(first,second)))
    length=sp.sqrt(squared)
    # Independent geometry library cross-check; not a runtime model call.
    oracle=sp.Point(*first).distance(sp.Point(*second))
    assert sp.simplify(length-oracle)==0
    reverse=sp.sqrt(sum((b-a)**2 for a,b in zip(first,second)))
    assert sp.simplify(length-reverse)==0 and state.extract_answer() is None
    return dict(query=query,raw_query_gap=gap,points=sorted(names),coordinate_ids=[c.fact_id for c in coordinates],
                squared_distance=str(squared),distance=str(length),runtime_answer=None)


def audit():
    raw=(ROOT/'data/train_with_models_v3.json').read_bytes();rows={r['id']:r for r in json.loads(raw)};cases=[]
    for pid,names in CASES.items():
        r=rows[pid];parts=[p.strip() for p in r['fact_expressions'].split(';')]
        selected=[p for p in parts if any(p==f'{n}: Point' or p.startswith(f'Coordinate({n})') for n in names)]
        facts=';'.join(selected)
        cases.append(dict(id=pid,original_facts=r['fact_expressions'],original_query=r['query_expressions'],
                          projected_facts=facts,probe=probe(facts,names)))
    assert [c['probe']['distance'] for c in cases]==['5','2*sqrt(13)']
    diagnostics={name:probe(f'A: Point;B: Point;Coordinate(A)=({a});Coordinate(B)=({b})',('A','B'))
                 for name,a,b in [('horizontal','0,2','3,2'),('vertical','2,0','2,4'),('coincident','1,1','1,1')]}
    same=probe('A: Point;Coordinate(A)=(1,1)',('A','A'))
    assert diagnostics['coincident']['distance']==same['distance']=='0'
    return dict(stage='design_audit_only_fact_projections',dataset_sha256=hashlib.sha256(raw).hexdigest(),
                cases=cases,diagnostics=diagnostics,same_point=same)


if __name__=='__main__':
    report=audit()
    (ROOT/'docs/开发规格/artifacts/point_pair_distance_contract.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print('1199: 5; 5211: 2*sqrt(13); zero/horizontal/vertical cases verified; RM53 not executed')
