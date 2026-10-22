"""ID1827 midpoint contract audit; no runtime RM54 or midpoint query execution."""
import hashlib
import json
from pathlib import Path
import sympy as sp
from src.state.transition_state import TransitionState
from src.theorems.bound_application import BoundApplicator, enumerate_actions

ROOT = Path(__file__).resolve().parents[2]
CASES = {1827: 'first_case', 5270: 'defer_vertex_and_inclination',
         1524: 'defer_focal_distance_sum', 4309: 'defer_focal_chord_length_inverse'}


def probe_midpoint(facts):
    """Facts-only subchain plus audit-only affine averaging and independent solve."""
    s = TransitionState.from_facts(facts, None)
    app = BoundApplicator()
    for mid in (78,41):
        actions = enumerate_actions(s,mid)
        assert len(actions)==1
        assert app.apply(s,actions[0]).status=='applied'
    key, = s.intersection_reductions
    f = s.intersection_reductions[key]
    assert s.properties[key,'distinct_real_roots']==2
    total = s.properties[key,'root_sum']
    midpoint = tuple(sp.simplify(v.subs(f.variable,total/2)) for v in f.xy)
    # Affine lift makes averaging valid; a quadratic lift would need the product too.
    assert all(sp.Poly(v,f.variable).degree()<=1 for v in f.xy)
    points=sp.solve([v.expression for v in s.equations.values()],(s.symbols['x'],s.symbols['y']))
    oracle=tuple(sp.simplify((a+b)/2) for a,b in zip(*points))
    assert len(points)==2 and midpoint==oracle==(sp.Integer(1),sp.Integer(2))
    assert len(s.named_intersections)==1 and not f.named_points and f.intersection_id is None
    return dict(variable=str(f.variable), polynomial=str(f.polynomial), lift=list(map(str,f.xy)),
                root_sum=str(total), midpoint=list(map(str,midpoint)), independent_midpoint=list(map(str,oracle)),
                existing_subchain=[78,41], missing_reduction_name_link=True)


def audit():
    raw=(ROOT/'data/train_with_models_v3.json').read_bytes()
    rows={r['id']:r for r in json.loads(raw)};cases=[]
    for pid,scope in CASES.items():
        r=rows[pid]
        try:
            TransitionState.from_facts(r['fact_expressions'],r['query_expressions'])
            diagnostic='parsed'
        except (ValueError,SyntaxError) as exc:
            diagnostic=str(exc)
        item=dict(id=pid,scope=scope,facts=r['fact_expressions'],query=r['query_expressions'],
                  text=r['text'],current_parser=diagnostic)
        if pid==1827:item['probe']=probe_midpoint(r['fact_expressions'])
        cases.append(item)
    # Same unordered pair and swapped intersection operands must retain audit result.
    facts=rows[1827]['fact_expressions'].replace('Intersection(H, G) = {A, B}','Intersection(G,H)={B,A}')
    assert probe_midpoint(';'.join(reversed(facts.split(';'))))['midpoint']==['1','2']
    return dict(stage='design_audit_only',dataset_sha256=hashlib.sha256(raw).hexdigest(),cases=cases)


if __name__=='__main__':
    result=audit()
    (ROOT/'docs/开发规格/artifacts/root_midpoint_contract.json').write_text(
        json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print('ID1827: existing RM78/41 subchain and independent midpoint (1, 2) verified; RM54 not executed')
