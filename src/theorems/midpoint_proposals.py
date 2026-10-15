"""Anonymous midpoint chord proposals for RM40/54/45; no endpoint solving."""
import sympy as sp
from src.solver.transition_primitives import TransitionError
from src.solver.midpoint_operations import ellipse_midpoint_chord, canonical_numeric_line, midpoint_coordinate_sums, ellipse_point_difference
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
    return chord_line_proposal(state,action,chord,rho,normal,line,
        [{'operation':'verify_midpoint_chord','rho':rho,'normal':normal,'pair':chord.pair_id},
         {'operation':'line_through_midpoint','midpoint':midpoint.xy,'equation':line}])


def derive_endpoint_sums(state, action):
    chord = check_midpoint_binding(state,action)
    if action.mode != 'derive_endpoint_sums':
        raise TransitionError('inapplicable','Unsupported RM54 mode')
    midpoint = state.chord_midpoints[chord.chord_id]
    sums = midpoint_coordinate_sums(midpoint.xy)
    return Proposal(properties={(chord.pair_id,k):v for k,v in zip(('x_sum','y_sum'),sums)},
        read_facts=(chord.chord_id,chord.pair_id,*midpoint.sources),
        operations=[{'operation':'midpoint_coordinate_sums','pair':chord.pair_id,
                     'midpoint':midpoint.xy,'sums':sums}])


def derive_point_difference_chord(state, action):
    chord = check_midpoint_binding(state,action)
    if action.mode != 'derive_point_difference_chord':
        raise TransitionError('inapplicable','Unsupported RM45 mode')
    keys = [(chord.pair_id,k) for k in ('x_sum','y_sum')]
    sources = tuple(f'property:{owner}:{name}' for owner,name in keys)
    if any(k not in state.properties for k in keys):
        raise TransitionError('inapplicable','Missing same-pair endpoint sums')
    if any(chord.pair_id not in state.provenance.get(k,()) for k in sources):
        raise TransitionError('inapplicable','Missing endpoint sum provenance')
    sums = tuple(state.properties[k].subs(state.values) for k in keys)
    midpoint = state.chord_midpoints[chord.chord_id]
    if any(sp.simplify(v-2*m)!=0 for v,m in zip(sums,midpoint.xy)):
        raise TransitionError('conflict','Endpoint sums contradict bound midpoint')
    a,b = bound_parameters(state,action.curve,action.equation_id)
    axis = bound_axis(state,action.curve,action.equation_id)
    dx,dy = (a,b) if axis=='x' else (b,a)
    rho,normal,line,coefficients = ellipse_point_difference(
        state.symbols['x'],state.symbols['y'],dx.subs(state.values),dy.subs(state.values),sums)
    return chord_line_proposal(state,action,chord,rho,normal,line,
        [{'operation':'ellipse_point_difference','pair':chord.pair_id,'sums':sums,
          'difference_coefficients':coefficients,'rho':rho,'equation':line}],sources)


def chord_line_proposal(state, action, chord, rho, normal, line, operations, extra_reads=()):
    """Check existing lines and organize a proposal; applicator owns the commit."""
    midpoint = state.chord_midpoints[chord.chord_id]
    x,y = state.symbols['x'],state.symbols['y']
    if any((f.line,f.curve)==(chord.line,chord.curve) for f in state.named_intersections.values()):
        raise TransitionError('undetermined','Named endpoint cross-check not implemented for this mode')
    existing = [f for f in state.equations.values() if f.owner==chord.line and f.role=='line']
    for fact in existing:
        if sp.simplify(canonical_numeric_line(fact.expression.subs(state.values),x,y)-line)!=0:
            raise TransitionError('conflict','Existing line contradicts given chord midpoint')
    key = f'derived:{chord.chord_id}:line'
    equations = {} if existing else {key:EquationFact(key,chord.line,'line',line,f'RM{action.model_id}')}
    return Proposal(equations=equations,
        properties={(chord.chord_id,'midpoint_rho'):rho,(chord.chord_id,'normal_x'):normal[0],
                    (chord.chord_id,'normal_y'):normal[1],(chord.chord_id,'distinct_real_intersections'):sp.Integer(2)},
        read_facts=(action.equation_id,chord.chord_id,chord.pair_id,*midpoint.sources,
                    f'frame:{chord.curve}',*(f'property:{chord.curve}:{k}' for k in ('a_sq','b_sq')),
                    *(f.fact_id for f in existing),*extra_reads,*state.constraints,*(f'value:{v}' for v in state.values)),
        operations=operations)
