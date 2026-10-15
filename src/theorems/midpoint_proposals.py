"""RM40 proposal from a given anonymous chord midpoint; no endpoint solving."""
import sympy as sp
from src.solver.transition_primitives import TransitionError
from src.solver.midpoint_operations import ellipse_midpoint_chord, canonical_numeric_line
from src.state.transition_state import EquationFact
from .bound_application import Proposal, bound_parameters, bound_axis


def check_midpoint_binding(state, action):
    chord = state.chords.get(action.relation_id)
    equation = state.equations.get(action.equation_id)
    if (chord is None or (chord.line,chord.curve)!=(action.line,action.curve)
            or state.entities.get(action.curve)!='Ellipse' or state.entities.get(action.line)!='Line'
            or equation is None or equation.owner!=action.curve or equation.role!='curve'
            or any(v is not None for v in (action.line_equation_id,action.point,action.coordinate_id,
                action.peer_curve,action.peer_equation_id,action.point_role,action.incidence_id,action.slope_sum_id))):
        raise TransitionError('inapplicable','Chord midpoint binding mismatch')
    midpoint = state.chord_midpoints.get(chord.chord_id)
    pair = state.chord_endpoint_pairs.get(chord.pair_id)
    if (midpoint is None or midpoint.chord_id!=chord.chord_id or pair is None
            or (pair.pair_id,pair.chord_id)!=(chord.pair_id,chord.chord_id)
            or midpoint.sources!=chord.sources or pair.sources!=chord.sources):
        raise TransitionError('inapplicable','Missing or mismatched anonymous endpoint identity')
    return chord


def derive_midpoint_chord(state, action):
    chord = check_midpoint_binding(state,action)
    if action.mode!='derive_midpoint_chord':
        raise TransitionError('inapplicable','Unsupported RM40 mode')
    a,b = bound_parameters(state,action.curve,action.equation_id)
    axis = bound_axis(state,action.curve,action.equation_id)
    dx,dy = (a,b) if axis=='x' else (b,a)
    midpoint = state.chord_midpoints[chord.chord_id]
    x,y = state.symbols['x'],state.symbols['y']
    rho,normal,line = ellipse_midpoint_chord(x,y,dx.subs(state.values),dy.subs(state.values),midpoint.xy)
    if any((f.line,f.curve)==(chord.line,chord.curve) for f in state.named_intersections.values()):
        raise TransitionError('undetermined','Named endpoint cross-check not implemented for this mode')
    existing = [f for f in state.equations.values() if f.owner==chord.line and f.role=='line']
    for fact in existing:
        if sp.simplify(canonical_numeric_line(fact.expression.subs(state.values),x,y)-line)!=0:
            raise TransitionError('conflict','Existing line contradicts given chord midpoint')
    key = f'derived:{chord.chord_id}:line'
    equations = {} if existing else {key:EquationFact(key,chord.line,'line',line,'RM40')}
    return Proposal(equations=equations,
        properties={(chord.chord_id,'midpoint_rho'):rho,(chord.chord_id,'normal_x'):normal[0],
                    (chord.chord_id,'normal_y'):normal[1],(chord.chord_id,'distinct_real_intersections'):sp.Integer(2)},
        read_facts=(action.equation_id,chord.chord_id,chord.pair_id,*midpoint.sources,
                    f'frame:{chord.curve}',*(f'property:{chord.curve}:{k}' for k in ('a_sq','b_sq')),
                    *(f.fact_id for f in existing),*state.constraints,*(f'value:{v}' for v in state.values)),
        operations=[{'operation':'verify_midpoint_chord','rho':rho,'normal':normal,'pair':chord.pair_id},
                    {'operation':'line_through_midpoint','midpoint':midpoint.xy,'equation':line}])
