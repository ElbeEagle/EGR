"""RM30 finite selection and geometric attainability audit; no runtime model."""
import hashlib
import json
from pathlib import Path
import sympy as sp
from src.state.transition_state import TransitionState
ROOT=Path(__file__).resolve().parents[2]
# Exact numeric transcriptions of equations and angles in raw facts.
CASES={3174:(4,1,sp.pi/3),3900:(4,1,sp.pi/2),6748:(10,1,2*sp.pi/3)}

def probe(aa,bb,theta):
    cc=sp.Integer(aa-bb);area=bb*sp.tan(theta/2)
    v=sp.simplify(area/sp.sqrt(cc));u_sq=sp.simplify(aa*(1-v*v/bb))
    assert u_sq.is_nonnegative is True
    u=sp.sqrt(u_sq);c=sp.sqrt(cc)
    r1=sp.sqrt((u-c)**2+v*v);r2=sp.sqrt((u+c)**2+v*v)
    cosine=sp.simplify((u*u+v*v-cc)/(r1*r2))
    assert sp.simplify(cosine-sp.cos(theta))==0
    assert sp.simplify(u*u/aa+v*v/bb-1)==0
    determinant_area=sp.simplify(c*v)
    assert sp.simplify(determinant_area-area)==0
    return dict(area=str(area),point=[str(u),str(v)],cosine=str(cosine),attainability_margin=str(sp.simplify(cc-aa*sp.sin(theta/2)**2)))

def audit():
    raw=(ROOT/'data/train_with_models_v3.json').read_bytes();rows={r['id']:r for r in json.loads(raw)};out=[]
    for pid in (*CASES,2571,1156):
        r=rows[pid]
        try:TransitionState.from_facts(r['fact_expressions'],r['query_expressions']);diagnostic='parsed'
        except (ValueError,SyntaxError) as exc:diagnostic=str(exc)
        item=dict(id=pid,text=r['text'],facts=r['fact_expressions'],query=r['query_expressions'],weak_models=r['models'],current_parser=diagnostic)
        if pid in CASES:item['independent_probe']=probe(*CASES[pid])
        else:item['scope']='defer_degree_unit_conversion'
        out.append(item)
    assert sp.simplify(3-4*sp.sin(sp.pi/3)**2)==0  # attainable maximum angle
    assert sp.simplify(3-4*sp.sin(5*sp.pi/12)**2)<0  # impossible 150 degrees
    return dict(stage='design_audit_only',dataset_sha256=hashlib.sha256(raw).hexdigest(),cases=out)

if __name__=='__main__':
    report=audit();(ROOT/'docs/开发规格/artifacts/focal_area_contract.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print('Three geometric witnesses and attainable/impossible boundary checks passed')
