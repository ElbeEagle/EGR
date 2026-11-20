"""Finite latus-rectum selection audit; not runtime model execution."""
import hashlib
import json
from pathlib import Path
import sympy as sp
from src.state.transition_state import TransitionState

ROOT=Path(__file__).resolve().parents[2]
CASES={6057:'first_rm19',6770:'first_rm20',598:'defer_inclination',1378:'defer_circle_chord'}


def independent_probe(pid):
    """Exact equation transcriptions from raw facts; answers are not inputs."""
    x,y=sp.symbols('x y',real=True)
    if pid==6057:
        equation=x*x/3-y*y/4-1
        focus=sp.sqrt(7)
        expected=8/sp.sqrt(3)
    else:
        equation=y*y-4*x
        focus=sp.Integer(1)
        expected=sp.Integer(4)
    ordinates=sp.solve(equation.subs(x,focus),y)
    assert len(ordinates)==2 and all(v.is_real for v in ordinates)
    length=sp.simplify(abs(ordinates[1]-ordinates[0]))
    assert sp.simplify(length-expected)==0
    return dict(equation=str(equation),focus_x=str(focus),endpoints_y=list(map(str,ordinates)),length=str(length))


def audit():
    raw=(ROOT/'data/train_with_models_v3.json').read_bytes()
    rows={r['id']:r for r in json.loads(raw)};cases=[]
    for pid,scope in CASES.items():
        r=rows[pid]
        try:
            TransitionState.from_facts(r['fact_expressions'],r['query_expressions'])
            diagnostic='parsed'
        except (ValueError,SyntaxError) as exc:diagnostic=str(exc)
        item=dict(id=pid,scope=scope,text=r['text'],facts=r['fact_expressions'],query=r['query_expressions'],weak_models=r['models'],current_parser=diagnostic)
        if pid in (6057,6770):item['independent_probe']=independent_probe(pid)
        cases.append(item)
    return dict(stage='design_audit_only',dataset_sha256=hashlib.sha256(raw).hexdigest(),cases=cases)


if __name__=='__main__':
    report=audit()
    (ROOT/'docs/开发规格/artifacts/latus_rectum_contract.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print('Independent checks passed: 6057 = 8*sqrt(3)/3; 6770 = 4; no RM19/20 runtime execution')
