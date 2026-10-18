"""Candidate contract audit, never a solver or a training trajectory generator."""
import hashlib
import json
from pathlib import Path
import sympy as sp
from src.state.transition_state import TransitionState

# Manually transcribed numeric forms from the saved raw facts, not gold answers.
# (id, x^2 coefficient, y^2 coefficient, midpoint, proposed scope)
CASES = [
    (5644, '1/2', '1', ('1','1/2'), 'first_batch'),
    (3682, '1/4', '1', ('-4/5','1/5'), 'first_batch'),
    (6164, '1/4', '1/2', ('1/2','-1'), 'first_batch'),
    (7439, '1/4', '1/2', ('1','1'), 'defer_segment_identity'),
    (7300, '1/4', '1/3', ('1','1'), 'defer_named_midpoint'),
    (4359, '1/4', '-1', ('4','1'), 'defer_hyperbola'),
    (3119, '1/4', '-1', ('6','3'), 'defer_hyperbola_no_chord'),
]


def audit_candidates(data_path):
    """Keep raw records separate from manually specified independent probes."""
    raw = Path(data_path).read_bytes()
    rows = {r['id']:r for r in json.loads(raw)}
    x,y,t = sp.symbols('x y t', real=True)
    cases = []
    for pid,at,bt,mt,scope in CASES:
        row = rows[pid]
        try:
            TransitionState.from_facts(row['fact_expressions'],row['query_expressions'])
            parser = 'parsed'
        except (ValueError,SyntaxError) as exc:
            parser = str(exc)
        a,b = sp.Rational(at),sp.Rational(bt)
        mx,my = map(sp.Rational,mt)
        nx,ny = a*mx,b*my
        line = sp.expand((nx*(x-mx)+ny*(y-my))/(nx if nx else ny))
        # Independent intersection probe along the proposed direction.
        poly = sp.Poly(a*(mx-ny*t)**2+b*(my+nx*t)**2-1,t)
        delta = sp.discriminant(poly.as_expr(),t)
        qualifies = poly.degree()==2 and delta.is_positive is True
        cases.append({'id':pid,'scope':scope,
            'facts':row['fact_expressions'],'query':row['query_expressions'],
            'weak_models':row['models'],'reference_answer':row['answer_expressions'],
            'current_parser':parser,
            'manual_numeric_probe':{'quadratic_coefficients':[a,b], 'midpoint':[mx,my],
                'candidate_line_lhs':line,'intersection_polynomial':poly.as_expr(),
                'discriminant':delta,'two_distinct_real_intersections':qualifies,
                'midpoint_verified':qualifies and poly.coeff_monomial(t)==0}})
    return {'stage':'design_audit_only','data_sha256':hashlib.sha256(raw).hexdigest(),
            'method':'Manual numeric transcription; independent SymPy probe; no solver success claim',
            'cases':cases}


if __name__ == '__main__':
    print(json.dumps(audit_candidates('data/train_with_models_v3.json'),
                     default=str,ensure_ascii=False,indent=2))
