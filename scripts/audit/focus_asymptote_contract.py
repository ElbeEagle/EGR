"""Finite RM22 selection audit, not runtime distance-model execution."""
import hashlib
import json
from pathlib import Path
import sympy as sp
from src.state.transition_state import TransitionState
from src.theorems.bound_application import BoundApplicator,BoundAction
from src.solver.distance_operations import point_to_line_distance
ROOT=Path(__file__).resolve().parents[2]
CASES={3200:(1,3),891:(4,3)}

def probe(aa,bb,axis='x'):
    equation=f'x^2/{aa}-y^2/{bb}=1' if axis=='x' else f'y^2/{aa}-x^2/{bb}=1'
    s=TransitionState.from_facts(f'G: Hyperbola;Expression(G)=({equation})',None)
    eq=next(iter(s.equations));t=BoundApplicator().apply(s,BoundAction(5 if axis=='x' else 6,'extract_parameters','G',eq))
    assert t.status=='applied'
    x,y=s.symbols['x'],s.symbols['y'];c=sp.sqrt(aa+bb);a,b=sp.sqrt(aa),sp.sqrt(bb);checks=[]
    for sign in (-1,1):
        focus=(sign*c,sp.S.Zero) if axis=='x' else (sp.S.Zero,sign*c)
        for branch in (-1,1):
            line=b*x+branch*a*y if axis=='x' else a*x+branch*b*y
            distance=point_to_line_distance(line,x,y,focus)
            assert sp.simplify(distance-b)==0
            checks.append(dict(focus=list(map(str,focus)),line=str(line),distance=str(distance)))
    return dict(scope='standard_model_fact_projection_plus_independent_geometry',axis=axis,equation=equation,checks=checks)

def audit():
    raw=(ROOT/'data/train_with_models_v3.json').read_bytes();rows={r['id']:r for r in json.loads(raw)};out=[]
    for pid in (3200,891,2417,1013):
        r=rows[pid]
        try:TransitionState.from_facts(r['fact_expressions'],r['query_expressions']);diagnostic='parsed'
        except (ValueError,SyntaxError) as exc:diagnostic=str(exc)
        item=dict(id=pid,text=r['text'],facts=r['fact_expressions'],query=r['query_expressions'],weak_models=r['models'],current_parser=diagnostic)
        if pid in CASES:item['probe']=probe(*CASES[pid])
        else:item['scope']='deferred_specific_focus_or_symbolic'
        out.append(item)
    return dict(stage='design_audit_only',dataset_sha256=hashlib.sha256(raw).hexdigest(),cases=out,y_axis_diagnostic=probe(4,3,'y'))

if __name__=='__main__':
    result=audit();(ROOT/'docs/开发规格/artifacts/focus_asymptote_contract.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print('Two numeric cases and y-axis diagnostic: all four distances equal sqrt(3)')
