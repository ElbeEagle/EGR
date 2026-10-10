"""Validate given or computed numeric focal chords without committing state."""
from dataclasses import dataclass
import sympy as sp
from src.solver.transition_primitives import TransitionError
from src.solver.parabola_operations import substitute_point
from src.solver.intersection_operations import substitute_line_in_parabola, classify_quadratic_roots
from .parabola_proposals import bound_parabola, parabola_reads


@dataclass(frozen=True)
class FocalChordEvidence:
    owner: str
    axis: str
    p: sp.Expr
    reads: tuple[str, ...]
    operations: tuple[dict, ...]


def check_product_binding(state, action):
    fact = state.named_intersections.get(action.relation_id) or state.intersection_reductions.get(action.relation_id)
    curve = state.equations.get(action.equation_id)
    if (fact is None or (fact.curve,fact.line) != (action.curve,action.line)
            or curve is None or curve.owner != action.curve or curve.role != 'curve'
            or state.entities.get(action.curve) != 'Parabola'
            or any(v is not None for v in (action.peer_curve,action.peer_equation_id,
                action.point_role,action.incidence_id,action.slope_sum_id))):
        raise TransitionError('inapplicable','Focal chord binding mismatch')
    if action.model_id != 59 and (action.point is not None or action.coordinate_id is not None):
        raise TransitionError('inapplicable','Unexpected point binding')
    if hasattr(fact,'curve_equation_id'):
        if (fact.curve_equation_id,fact.line_equation_id) != (action.equation_id,action.line_equation_id):
            raise TransitionError('inapplicable','Reduction equation binding mismatch')
    elif action.line_equation_id is not None:
        raise TransitionError('inapplicable','Given intersection does not bind an equation')
    return fact


def verify_focus_line(line, x, y, focus):
    residual = substitute_point(line,x,y,focus)
    if residual != 0:
        raise TransitionError('inapplicable','Bound line does not pass through focus')
    return residual


def verify_focal_chord(state, action):
    fact = check_product_binding(state,action)
    _,axis,_,p,focus = bound_parabola(state,action,state.equations[action.equation_id])
    if p.free_symbols or p.is_positive is not True:
        raise TransitionError('undetermined','Numeric positive p required')
    reads = list(parabola_reads(state,action)) + [fact.fact_id]
    operations=[]
    given = fact.fact_id in state.named_intersections
    if given:
        sources = [f.fact_id for f in state.focus_incidences.values()
                   if (f.curve,f.line)==(fact.curve,fact.line)]
        for alias in state.focus_aliases.values():
            if alias.curve == fact.curve:
                for incidence in state.incidences.values():
                    if (incidence.point,incidence.curve)==(alias.point,fact.line):
                        sources.extend((alias.fact_id,incidence.fact_id))
        if not sources:
            raise TransitionError('inapplicable','Given focus incidence required')
        reads.extend(sources)
        operations.append({"operation":"verify_given_focal_chord", "intersection":fact.fact_id,
                           "points":fact.points, "focus_sources":sources})
    lines = [f for f in state.equations.values() if f.owner==fact.line and f.role=='line']
    if not given and (len(lines)!=1 or lines[0].fact_id!=action.line_equation_id):
        raise TransitionError('inapplicable','Unique source line required')
    x,y=state.symbols['x'],state.symbols['y']
    curve=state.equations[action.equation_id].expression.subs(state.values)
    for line in lines:
        expression=line.expression.subs(state.values)
        try:
            verify_focus_line(expression,x,y,focus)
            computed=substitute_line_in_parabola(curve,expression,x,y)
            roots=classify_quadratic_roots(computed.polynomial,computed.variable)
            if roots.distinct_real_roots!=2:
                raise TransitionError('inapplicable','Two finite distinct intersections required')
        except TransitionError as exc:
            if given and exc.status == 'inapplicable':
                raise TransitionError('conflict','Given focal chord contradicts explicit line') from exc
            raise
        reads.append(line.fact_id)
        operations.append({"operation":"verify_computed_focal_chord", "line":line.fact_id,
                           "focus_residual":sp.S.Zero,"discriminant":roots.discriminant,
                           "distinct_real_roots":roots.distinct_real_roots})
        if not given and (fact.variable!=computed.variable or
                sp.simplify(fact.polynomial.subs(state.values)-computed.polynomial)!=0 or
                any(sp.simplify(a.subs(state.values)-b)!=0 for a,b in zip(fact.xy,computed.xy))):
            raise TransitionError('conflict','Reduction disagrees with source equations')
    if given:
        known=[]
        for point in fact.points:
            coord=state.coordinates.get(point)
            if coord is not None:
                xy=tuple(v.subs(state.values) for v in coord.xy)
                if substitute_point(curve,x,y,xy)!=0 or any(substitute_point(l.expression.subs(state.values),x,y,xy)!=0 for l in lines):
                    raise TransitionError('conflict','Intersection coordinates contradict equations')
                # A known endpoint also determines its focus-line; the axial
                # singleton branch contradicts a declared pair even without H's equation.
                endpoint_line=(x-focus[0])*(xy[1]-focus[1])-(y-focus[1])*(xy[0]-focus[0])
                candidate=substitute_line_in_parabola(curve,endpoint_line,x,y)
                try:
                    qualification=classify_quadratic_roots(candidate.polynomial,candidate.variable)
                    if qualification.distinct_real_roots != 2:
                        raise TransitionError('inapplicable','Not a finite pair')
                except TransitionError as exc:
                    raise TransitionError('conflict','Endpoint implies a singleton focal intersection') from exc
                known.append(xy);reads.append(coord.fact_id)
        if len(known)==2:
            if known[0]==known[1]:
                raise TransitionError('conflict','Intersection points coincide')
            # The chord defined by two known endpoints must contain the focus.
            a,b=known
            if sp.simplify((a[0]-focus[0])*(b[1]-focus[1])-(a[1]-focus[1])*(b[0]-focus[0]))!=0:
                raise TransitionError('conflict','Known endpoints do not form a focal chord')
    return FocalChordEvidence(fact.fact_id,axis,p,tuple(dict.fromkeys(reads)),tuple(operations))
