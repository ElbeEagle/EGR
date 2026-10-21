"""Read-only midpoint-alias and hyperbola qualification audit; not model execution."""
import hashlib
import json
from pathlib import Path
import sympy as sp
from src.state.transition_state import TransitionState
from src.solver.transition_primitives import parse_expression

# Numeric coefficients and midpoints transcribed from raw facts; never from answers.
CASES = [(2227,'1/2','1/4',('1','1'),'segment_alias_first'),
         (2324,'1/9','1/5',('1','1'),'segment_alias_first'),
         (3337,'1/4','1',('1','1/2'),'segment_alias_first'),
         (2290,'1/4','1/9',('1','1'),'endpoint_alias_second'),
         (4761,'1/4','1',('1','1/2'),'endpoint_alias_second'),
         (7300,'1/4','1/3',('1','1'),'reference_conflict'),
         (1801,'1/4','-1',('4','1'),'rm46_deferred'),
         (3119,'1/4','-1',('6','3'),'rm46_deferred')]


def numeric_probe(alpha, beta, midpoint):
    """Independent line-parameter substitution, including degenerate directions."""
    x,y,t=sp.symbols('x y t',real=True)
    a,b=sp.Rational(alpha),sp.Rational(beta)
    mx,my=map(sp.Rational,midpoint)
    q=sp.simplify(a*mx**2+b*my**2)
    if mx==0 and my==0:
        return {'q':q,'status':'undetermined_center','line':None}
    nx,ny=a*mx,b*my
    line=sp.expand((nx*(x-mx)+ny*(y-my))/(nx if nx else ny))
    poly=sp.Poly(a*(mx-ny*t)**2+b*(my+nx*t)**2-1,t)
    valid=poly.degree()==2 and sp.discriminant(poly.as_expr(),t).is_positive is True
    assert sp.simplify(poly.as_expr()-(a*b*q*t**2+q-1))==0
    return {'q':q,'line':line,'intersection_polynomial':poly.as_expr(),
            'degree':poly.degree(),'two_distinct_real_points':valid,
            'midpoint_verified':valid and poly.coeff_monomial(t)==0}


def audit(data_path):
    raw=Path(data_path).read_bytes();rows={r['id']:r for r in json.loads(raw)}
    x,y=sp.symbols('x y',real=True);cases=[]
    for pid,a,b,m,scope in CASES:
        r=rows[pid];probe=numeric_probe(a,b,m)
        try:
            TransitionState.from_facts(r['fact_expressions'],r['query_expressions'])
            parser='parsed'
        except (ValueError,SyntaxError) as exc:
            parser=str(exc)
        agreement=None
        if '=' in r['answer_expressions']:
            lhs,rhs=r['answer_expressions'].split('=')
            expr=parse_expression(lhs,{'x':x,'y':y})[0]-parse_expression(rhs,{'x':x,'y':y})[0]
            poly=sp.Poly(expr,x,y);scale=poly.coeff_monomial(x) or poly.coeff_monomial(y)
            agreement=sp.simplify(expr/scale-probe['line'])==0
        cases.append({'id':pid,'scope':scope,'text':r['text'],'facts':r['fact_expressions'],
                      'query':r['query_expressions'],'weak_models':r['models'],
                      'reference_answer':r['answer_expressions'],'reference_agrees':agreement,
                      'current_parser':parser,'manual_numeric_input':[a,b,m],'probe':probe})
    boundary=[{'midpoint':m,'probe':numeric_probe('1/4','-1',m)}
              for m in [('4','1'),('0','1'),('1','0'),('2','0'),('2','1'),('0','0')]]
    assert [p['probe'].get('two_distinct_real_points') for p in boundary]==[True,True,False,False,False,None]
    assert all(c['reference_agrees'] for c in cases if c['scope'] in ('segment_alias_first','endpoint_alias_second'))
    assert next(c for c in cases if c['id']==7300)['reference_agrees'] is False
    return {'stage':'design_audit_only','data_sha256':hashlib.sha256(raw).hexdigest(),
            'cases':cases,'hyperbola_boundary_probes':boundary}


if __name__=='__main__':
    print(json.dumps(audit('data/train_with_models_v3.json'),default=str,ensure_ascii=False,indent=2))
