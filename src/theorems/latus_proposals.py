"""Bound latus eligibility and proposals; application commits the result."""
from src.solver.transition_primitives import TransitionError
from src.solver.latus_operations import latus_length

def check_latus_binding(state,a):
    chord=state.chords.get(a.relation_id)
    segments=[s for s in state.segment_chords.values() if chord and (s.line,s.curve)==(chord.line,chord.curve)]
    f=state.equations.get(a.equation_id)
    if (a.mode!='derive_latus_length' or chord is None or len(segments)!=1 or
        (a.curve,a.line)!=(chord.curve,chord.line) or state.entities.get(a.curve)!={19:'Hyperbola',20:'Parabola'}[a.model_id] or
        f is None or f.owner!=a.curve or f.role!='curve' or not chord.sources or
        any(v is not None for v in (a.point,a.coordinate_id,a.line_equation_id,a.peer_curve,a.peer_equation_id,a.point_role,a.incidence_id,a.slope_sum_id))):
        raise TransitionError('inapplicable','Latus chord binding mismatch')
    return chord,segments[0],f

def derive_latus(state,a):
    from .bound_application import Proposal,bound_parameters,bound_axis
    from .parabola_proposals import bound_parabola,parabola_reads
    chord,segment,f=check_latus_binding(state,a)
    if a.model_id==19:
        aa,bb=bound_parameters(state,a.curve,a.equation_id);axis=bound_axis(state,a.curve,a.equation_id)
        value=latus_length(19,aa.subs(state.values),bb.subs(state.values))
        reads=(a.equation_id,f'frame:{a.curve}',*(f'property:{a.curve}:{k}' for k in ('a_sq','b_sq')))
    else:
        _,axis,_,p,_=bound_parabola(state,a,f);value=latus_length(20,p);reads=parabola_reads(state,a)
    if any(not state.provenance.get(k) for k in reads if k.startswith(('property:','frame:'))):
        raise TransitionError('inapplicable','Standard parameter sources required')
    evidence=[e for e in state.latus_evidence.values() if e.segment==segment.segment]
    focus=[e for e in evidence if e.kind=='focus' and e.target==a.curve]
    perpendicular=[e for e in evidence if e.kind=='perpendicular']
    if not focus or not perpendicular:raise TransitionError('inapplicable','Focus and perpendicular evidence required')
    if any(e.target not in (axis+'Axis',f'SymmetryAxis({a.curve})') for e in perpendicular):
        raise TransitionError('conflict','Perpendicular direction is not the conic axis')
    return Proposal(properties={(chord.chord_id,'chord_length'):value},
        read_facts=(*reads,chord.chord_id,*chord.sources,*(e.source for e in evidence)),
        operations=[{'operation':'latus_length','model':a.model_id,'axis':axis,'length':value}])
