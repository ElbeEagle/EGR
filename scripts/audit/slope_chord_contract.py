"""RM51 design audit: existing root chain plus independent coordinate distance."""
import hashlib
import json
from pathlib import Path
import sympy as sp
from src.state.transition_state import TransitionState
from src.theorems.bound_application import BoundApplicator, enumerate_actions

ROOT = Path(__file__).resolve().parents[2]
CASES = (3057, 6347)


def probe(facts, query):
    state = TransitionState.from_facts(facts, query)
    app = BoundApplicator()
    for mid in (78, 41):
        result = app.apply(state, enumerate_actions(state, mid)[0])
        assert result.status == 'applied', result.diagnostic
    reduction, = state.intersection_reductions.values()
    key, t = reduction.fact_id, reduction.variable
    total, product = (state.properties[key, n] for n in ('root_sum','root_product'))
    assert state.properties[key,'distinct_real_roots'] == 2
    alpha, gamma = (sp.diff(v, t) for v in reduction.xy)
    eligible = alpha != 0
    roots = sp.solve(reduction.polynomial, t)
    assert len(roots) == 2
    points = [tuple(v.subs(t, root) for v in reduction.xy) for root in roots]
    oracle = sp.simplify(sp.sqrt(sum((u-v)**2 for u,v in zip(*points))))
    length = None
    slope = None
    if eligible:
        slope = sp.simplify(gamma/alpha)
        length = sp.simplify(abs(alpha)*sp.sqrt(total**2-4*product)*sp.sqrt(1+slope**2))
        assert sp.simplify(length-oracle) == 0
    assert state.extract_answer() is None  # Independent arithmetic never submits an answer.
    result = app.apply(state, enumerate_actions(state,50)[0])
    assert result.status == 'applied' and sp.simplify(state.extract_answer()-oracle) == 0
    return dict(executed_models=[78,41,50], variable=str(t), lift=list(map(str,reduction.xy)),
                root_sum=str(total), root_product=str(product), finite_slope_eligible=eligible,
                slope=str(slope), rm51_independent_length=str(length), coordinate_oracle=str(oracle))


def audit():
    raw = (ROOT/'data/train_with_models_v3.json').read_bytes()
    rows = {r['id']:r for r in json.loads(raw)}
    cases=[]
    for pid in CASES:
        r=rows[pid]
        cases.append(dict(id=pid, text=r['text'], facts=r['fact_expressions'], query=r['query_expressions'],
                          weak_models=r['models'], probe=probe(r['fact_expressions'],r['query_expressions'])))
    diagnostics={name:probe('G:Parabola;H:Line;Expression(G)=('+curve+');Expression(H)=('+line+')','Length(InterceptChord(H,G))')
                 for name,curve,line in [('swapped','x^2=4*y','x=y-1'),('vertical','y^2=4*x','x=1'),('horizontal','x^2=4*y','y=1')]}
    assert cases[0]['probe']['coordinate_oracle']=='sqrt(15)'
    assert cases[1]['probe']['coordinate_oracle']=='8'
    assert not diagnostics['vertical']['finite_slope_eligible']
    return dict(stage='design_audit_only_not_rm51_execution',dataset_sha256=hashlib.sha256(raw).hexdigest(),cases=cases,diagnostics=diagnostics)


if __name__=='__main__':
    report=audit()
    (ROOT/'docs/开发规格/artifacts/slope_chord_contract.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print('3057 sqrt(15), 6347 8; coordinate cross-checks pass; vertical RM51 excluded')
