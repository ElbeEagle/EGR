"""RM28 finite design audit; fact projections are not original-query solves."""
import hashlib
import json
from pathlib import Path
import sympy as sp
from src.state.transition_state import TransitionState
from src.theorems.bound_application import BoundApplicator, enumerate_actions

ROOT = Path(__file__).resolve().parents[2]
CASES = {2779: 'first_pair_query', 1834: 'defer_right_directrix'}


def probe(facts, standard):
    """Run existing parameter models, then independently check a directrix pair."""
    state = TransitionState.from_facts(facts, None)
    app = BoundApplicator()
    executed = []
    for mid, mode in ((standard, 'extract_parameters'), (12, 'derive_c_sq')):
        actions = enumerate_actions(state, mid, mode)
        assert len(actions) == 1
        result = app.apply(state, actions[0])
        assert result.status == 'applied', result.diagnostic
        executed.append(mid)
    aa, bb, cc = (state.properties['G', k] for k in ('a_sq', 'b_sq', 'c_sq'))
    assert cc == aa + bb and all(v.is_positive for v in (aa, bb, cc))
    axis = state.frames['G'].axis
    offset = sp.simplify(aa / sp.sqrt(cc))
    # At the positive-axis vertex, distance-to-focus / distance-to-directrix = e.
    ratio = sp.simplify((sp.sqrt(cc)-sp.sqrt(aa))/(sp.sqrt(aa)-offset))
    assert sp.simplify(ratio-sp.sqrt(cc/aa)) == 0
    return dict(executed_models=executed, axis=axis, a_sq=str(aa), b_sq=str(bb),
                c_sq=str(cc), offsets=[str(-offset), str(offset)],
                vertex_ratio=str(ratio), kind='parameter_projection_and_independent_math')


def audit():
    raw = (ROOT/'data/train_with_models_v3.json').read_bytes()
    rows = {r['id']: r for r in json.loads(raw)}
    cases = []
    for pid, scope in CASES.items():
        r = rows[pid]
        try:
            TransitionState.from_facts(r['fact_expressions'], r['query_expressions'])
        except ValueError as exc:
            gap = str(exc)
        else:
            gap = None  # Query identity may be implemented after the design audit.
        cases.append(dict(id=pid, scope=scope, text=r['text'], facts=r['fact_expressions'],
                          query=r['query_expressions'], weak_models=r['models'], query_gap=gap,
                          probe=probe(r['fact_expressions'], 5)))
    y = probe('G: Hyperbola;Expression(G)=(y^2-x^2/3=1)', 6)
    scaled = probe('G: Hyperbola;Expression(G)=(3*x^2-y^2=3)', 5)
    assert cases[0]['probe']['offsets'] == y['offsets'] == scaled['offsets'] == ['-1/2', '1/2']
    return dict(stage='design_audit_only', dataset_sha256=hashlib.sha256(raw).hexdigest(),
                cases=cases, diagnostics=dict(y_axis=y, scaled=scaled))


if __name__ == '__main__':
    report = audit()
    (ROOT/'docs/开发规格/artifacts/directrix_pair_contract.json').write_text(
        json.dumps(report, ensure_ascii=False, indent=2)+'\n')
    print('2779: x=±1/2; y-axis/scaling verified; query capability recorded live; RM28 not executed')
