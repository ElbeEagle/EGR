"""RM58 design audit on explicit three-coordinate projections."""
import hashlib
import itertools
import json
from pathlib import Path
import sympy as sp
from src.state.transition_state import TransitionState

ROOT=Path(__file__).resolve().parents[2]
CASES={870:('H','F1','F2'),3239:('Z','F1','F2')}


def probe(facts,names):
    query='Area(TriangleOf('+','.join(names)+'))'
    state=TransitionState.from_facts(facts,query)
    points=[state.coordinates[n].xy for n in names]
    assert all(state.provenance.get(state.coordinates[n].fact_id) for n in names)
    a,b,c=points
    determinant=sp.simplify((b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0]))
    area=sp.Abs(determinant)/2
    for perm in itertools.permutations(points):
        assert sp.Abs(sp.Matrix([[p[0],p[1],1] for p in perm]).det())/2==area
    if area>0:
        assert sp.Abs(sp.Polygon(*(sp.Point(*p) for p in points)).area)==area
    for perm in itertools.permutations(names):
        other=TransitionState.from_facts(facts,'Area(TriangleOf('+','.join(perm)+'))')
        assert other.query==state.query and other.extract_answer() is None
    return dict(query=query,query_class=type(state.query).__name__,area=str(area),
                determinant=str(determinant),eligible=bool(area>0),runtime_answer=None)


def audit():
    raw=(ROOT/'data/train_with_models_v3.json').read_bytes();rows={r['id']:r for r in json.loads(raw)};cases=[]
    for pid,names in CASES.items():
        r=rows[pid];parts=[p.strip() for p in r['fact_expressions'].split(';')]
        facts=';'.join(p for p in parts if any(p==f'{n}: Point' or p.startswith(f'Coordinate({n})') for n in names))
        cases.append(dict(id=pid,original_facts=r['fact_expressions'],original_query=r['query_expressions'],
                          projected_facts=facts,probe=probe(facts,names)))
    diagnostics={name:probe(f'A: Point;B: Point;C: Point;Coordinate(A)=({a});Coordinate(B)=({b});Coordinate(C)=({c})',('A','B','C'))
                 for name,a,b,c in [('non_origin','1,2','4,2','1,6'),('collinear','0,0','1,1','2,2'),('coincident','1,1','1,1','2,3')]}
    assert [c['probe']['area'] for c in cases]==['6','3']
    assert diagnostics['non_origin']['area']=='6'
    assert not diagnostics['collinear']['eligible'] and not diagnostics['coincident']['eligible']
    return dict(stage='design_audit_only_fact_projections',dataset_sha256=hashlib.sha256(raw).hexdigest(),cases=cases,diagnostics=diagnostics)


if __name__=='__main__':
    report=audit()
    (ROOT/'docs/开发规格/artifacts/coordinate_area_contract.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print('870: 6; 3239: 3; permutations/non-origin verified; degenerate cases excluded; RM58 not executed')
