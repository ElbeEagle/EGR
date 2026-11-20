"""Finite RM32 selection audit, not runtime RM32 execution."""
import hashlib
import json
from pathlib import Path
import sympy as sp
from src.state.transition_state import TransitionState
from src.theorems.bound_application import BoundApplicator,enumerate_actions,BoundAction
ROOT=Path(__file__).resolve().parents[2]
CASES={998:(25,16),1552:(25,9)}

def probe(aa,bb):
    """Facts-only standard/parameter subchain; independent distance checks at sample points."""
    s=TransitionState.from_facts(f'G: Ellipse;Expression(G)=(x^2/{aa}+y^2/{bb}=1)',None)
    eq=next(iter(s.equations));app=BoundApplicator()
    assert app.apply(s,BoundAction(3,'extract_parameters','G',eq)).status=='applied'
    assert app.apply(s,enumerate_actions(s,11,'derive_c_sq')[0]).status=='applied'
    a,b,c=sp.sqrt(aa),sp.sqrt(bb),sp.sqrt(s.properties['G','c_sq'])
    expected=2*a+2*c
    checks=[]
    for u,v in [(0,1),(sp.Rational(3,5),sp.Rational(4,5)),(1,0)]:
        x,y=a*u,b*v
        total=sp.sqrt((x-c)**2+y*y)+sp.sqrt((x+c)**2+y*y)+2*c
        assert sp.simplify(total-expected)==0
        checks.append(dict(point=[str(x),str(y)],perimeter=str(sp.simplify(total))))
    return dict(stage='fact_projection_3_11_only',c_sq=str(c*c),expected=str(expected),distance_checks=checks)

def audit():
    raw=(ROOT/'data/train_with_models_v3.json').read_bytes();rows={r['id']:r for r in json.loads(raw)};out=[]
    for pid in (998,1552,3272,3703):
        r=rows[pid]
        try:TransitionState.from_facts(r['fact_expressions'],r['query_expressions']);diagnostic='parsed'
        except (ValueError,SyntaxError) as exc:diagnostic=str(exc)
        item=dict(id=pid,text=r['text'],facts=r['fact_expressions'],query=r['query_expressions'],weak_models=r['models'],reference_answer=r['answer_expressions'],current_parser=diagnostic)
        if pid in CASES:item['probe']=probe(*CASES[pid])
        out.append(item)
    return dict(stage='design_audit_only',dataset_sha256=hashlib.sha256(raw).hexdigest(),cases=out)

if __name__=='__main__':
    report=audit();(ROOT/'docs/开发规格/artifacts/focal_perimeter_contract.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print('998: 16; 1552: 18; standard/parameter projections and distance checks passed')
