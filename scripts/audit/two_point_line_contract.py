"""RM73 design audit on explicit fact projections, not original-query solves."""
import hashlib
import json
from pathlib import Path
import sympy as sp
from src.state.transition_state import TransitionState
from src.solver.midpoint_operations import canonical_numeric_line

ROOT = Path(__file__).resolve().parents[2]
CASES = (1168, 1199)


def probe(facts):
    state = TransitionState.from_facts(facts, 'Expression(LineOf(A,B))')
    assert state.extract_answer() is None
    identity = state.named_lines[state.query.line]
    a, b = (state.coordinates[p].xy for p in identity.endpoints)
    x, y = state.symbols['x'], state.symbols['y']
    assert a != b
    expression = (b[1]-a[1])*(x-a[0])-(b[0]-a[0])*(y-a[1])
    line = canonical_numeric_line(expression, x, y)
    for xy in (a,b):
        assert sp.simplify(line.subs({x:xy[0], y:xy[1]}, simultaneous=True)) == 0
    reversed_state = TransitionState.from_facts(facts, 'Expression(LineOf(B,A))')
    assert reversed_state.query == state.query
    assert state.extract_answer() is None  # Independent calculation does not submit a result.
    return dict(line_identity=state.query.line, endpoints=identity.endpoints,
                coordinate_ids=[state.coordinates[p].fact_id for p in identity.endpoints],
                equation=str(line), runtime_answer=None)


def audit():
    raw=(ROOT/'data/train_with_models_v3.json').read_bytes()
    rows={r['id']:r for r in json.loads(raw)};cases=[]
    for pid in CASES:
        r=rows[pid]
        parts=[p.strip() for p in r['fact_expressions'].split(';')]
        selected=[p for p in parts if p in ('A: Point','B: Point') or p.startswith(('Coordinate(A)', 'Coordinate(B)'))]
        facts=';'.join(selected)
        cases.append(dict(id=pid,text=r['text'],original_facts=r['fact_expressions'],original_query=r['query_expressions'],
                          projected_facts=facts,diagnostic_query='Expression(LineOf(A,B))',probe=probe(facts)))
    diagnostics={name:probe(f'A: Point;B: Point;Coordinate(A)=({a});Coordinate(B)=({b})')
                 for name,a,b in [('vertical','2,0','2,3'),('horizontal','0,2','3,2')]}
    return dict(stage='design_audit_only_fact_projections',dataset_sha256=hashlib.sha256(raw).hexdigest(),cases=cases,diagnostics=diagnostics)


if __name__=='__main__':
    report=audit()
    (ROOT/'docs/开发规格/artifacts/two_point_line_contract.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print('1168/1199 point projections verified; reversed identity and axis-aligned lines verified; RM73 not executed')
