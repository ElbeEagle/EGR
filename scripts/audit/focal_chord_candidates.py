"""RM34/35 weak-label inventory and independent algebra checks, not a solver."""
import hashlib
import json
from pathlib import Path
import sys
import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from src.state.transition_state import TransitionState


def verify_product_identities():
    """Check coordinate products without invoking theorem implementations."""
    p = sp.Symbol('p', positive=True)
    m, v = sp.symbols('m v', real=True)
    checks = []
    for axis in ('x', 'y'):
        for sign in (-1, 1):
            # v²=2*s*p*u, u=m*v+s*p/2; Vieta used only as audit algebra.
            polynomial = sp.expand(v*v-2*sign*p*(m*v+sign*p/2))
            a,b,c = sp.Poly(polynomial,v).all_coeffs()
            total, product = -b/a, c/a
            axial_product = sp.expand(m*m*product+m*sign*p*total/2+p*p/4)
            assert sp.simplify(axial_product-p*p/4)==0
            assert sp.simplify(product+p*p)==0
            assert sp.discriminant(polynomial,v).is_positive
            checks.append({'axis':axis,'sign':sign,'axial_product':str(axial_product),
                           'transverse_product':str(product),'two_real_roots':True})
    assert sp.Rational(2)**2/4-2**2 == -3  # ID4373: independent mathematical result.
    assert sp.Rational(4)**2/4 == 4 and -4**2 == -16  # ID1191 axes.
    return checks


def build_audit():
    """Inventory source records and probe only their original input parsing."""
    raw=(ROOT/'data/train_with_models_v3.json').read_bytes()
    rows=json.loads(raw)
    selected=[r for r in rows if {34,35}.intersection(r.get('models',[]))]
    candidates=[]
    for r in selected:
        try:
            TransitionState.from_facts(r['fact_expressions'],r['query_expressions'])
            parsed,error=True,None
        except (ValueError,TypeError,KeyError,SyntaxError) as exc:
            parsed,error=False,str(exc)
        try:
            TransitionState.from_facts(r['fact_expressions'],None)
            facts_parsed,facts_error=True,None
        except (ValueError,TypeError,KeyError,SyntaxError) as exc:
            facts_parsed,facts_error=False,str(exc)
        candidates.append({'id':r['id'],'weak_models':r['models'],
            'facts':r['fact_expressions'],'query':r['query_expressions'],
            'input_parses':parsed,'first_parse_error':error,
            'facts_only_parses':facts_parsed,'first_facts_error':facts_error})
    return {'schema_version':'focal-chord-selection-v1','dataset_sha256':hashlib.sha256(raw).hexdigest(),
            'scope':'All records weak-labeled RM34/35; parsing probes and independent algebra only, no solver coverage claim',
            'weak_label_counts':{str(mid):sum(mid in r.get('models',[]) for r in rows) for mid in (34,35)},
            'unique_candidates':len(selected),'candidates':candidates,
            'independent_algebra':verify_product_identities(),
            'selected_primary':4373,'selected_axis_validation':1191,'deferred_symbolic':1833}


if __name__=='__main__':
    print(json.dumps(build_audit(),ensure_ascii=False,indent=2))
