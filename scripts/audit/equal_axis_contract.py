"""Finite RM24 contract audit; baseline chains are not RM24 execution."""
import hashlib
import json
from pathlib import Path
import sympy as sp
from src.reasoning.bound_slice import solve_eccentricity_slice
ROOT=Path(__file__).resolve().parents[2]
CASES={650:'first_numeric',1412:'first_numeric',2287:'reject_not_equal',3316:'defer_scalar_alias',799:'defer_symbolic'}

def audit():
 raw=(ROOT/'data/train_with_models_v3.json').read_bytes();rows={r['id']:r for r in json.loads(raw)};out=[]
 for pid,scope in CASES.items():
  r=rows[pid];item=dict(id=pid,scope=scope,text=r['text'],facts=r['fact_expressions'],query=r['query_expressions'],weak_models=r['models'])
  if scope!='defer_symbolic':
   result=solve_eccentricity_slice(r['fact_expressions'],r['query_expressions'])
   item.update(status=result.status,answer=str(result.answer),diagnostic=result.diagnostic,executed_models=[t.action.model_id for t in result.transitions])
   if scope in ('first_numeric','reject_not_equal'):
    assert result.status=='solved'
    aa=result.state.properties['G','a_sq'];bb=result.state.properties['G','b_sq']
    equal=sp.simplify(aa-bb)==0
    assert equal==(scope=='first_numeric')
    assert sp.simplify(result.answer-sp.sqrt((aa+bb)/aa))==0
    item.update(a_sq=str(aa),b_sq=str(bb),equal_axis_eligible=equal)
  out.append(item)
 return dict(stage='design_audit_only',dataset_sha256=hashlib.sha256(raw).hexdigest(),cases=out)

if __name__=='__main__':
 report=audit();(ROOT/'docs/开发规格/artifacts/equal_axis_contract.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
 print('650/1412 eligible, baseline sqrt(2); 2287 ineligible; 3316 scalar alias deferred')
