"""Finite RM41 batch selection; existing-chain probes are not RM41 execution."""
import hashlib
import json
from pathlib import Path
import sympy as sp
from src.reasoning.bound_slice import solve_chord_length_slice
from src.state.transition_state import TransitionState

ROOT = Path(__file__).resolve().parents[2]
CASES = {3057: 'first_new_case', 6347: 'regression', 1827: 'defer_midpoint_output',
         1010: 'defer_ellipse_elimination', 1249: 'defer_hyperbola_elimination',
         813: 'defer_generic_curve_type'}


def independent_length(state):
    """Solve the two input equations independently; only an audit oracle."""
    x, y = state.symbols['x'], state.symbols['y']
    equations = [f.expression for f in state.equations.values()]
    points = sp.solve(equations, (x, y))
    assert len(points) == 2 and points[0] != points[1]
    assert all(v.is_real is True for point in points for v in point)
    return sp.sqrt(sp.simplify(sum((a-b)**2 for a,b in zip(*points))))


def audit():
    raw = (ROOT/'data/train_with_models_v3.json').read_bytes()
    rows = {r['id']: r for r in json.loads(raw)}
    output = []
    for pid, scope in CASES.items():
        row = rows[pid]
        facts, query = row['fact_expressions'], row['query_expressions']
        result = solve_chord_length_slice(facts, query)
        item = dict(id=pid, scope=scope, text=row['text'], facts=facts, query=query,
                    weak_models=row['models'], existing_chain_status=result.status,
                    diagnostic=result.diagnostic, answer=str(result.answer) if result.answer is not None else None,
                    executed_models=[t.action.model_id for t in result.transitions])
        if scope in ('first_new_case', 'regression'):
            expected = independent_length(TransitionState.from_facts(facts, query))
            assert result.status == 'solved' and sp.simplify(result.answer-expected) == 0
            assert item['executed_models'] == [78,42,43,50]
            item['independent_length'] = str(expected)
        output.append(item)
    return dict(stage='selection_audit_only', dataset_sha256=hashlib.sha256(raw).hexdigest(),
                proposed_chain=[78,41,50], cases=output)


if __name__ == '__main__':
    report = audit()
    target = ROOT/'docs/开发规格/artifacts/vieta_batch_selection.json'
    target.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
    for case in report['cases']:
        print(case['id'], case['existing_chain_status'], case['answer'])
