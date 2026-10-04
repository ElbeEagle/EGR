"""Transactional application of explicitly bound conic models."""
from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field, replace

import sympy as sp

from src.solver.transition_primitives import (
    TransitionError, truth, ensure_consistent, ellipse_parameters, hyperbola_parameters,
)
from src.state.transition_state import TransitionState, CurveFrame, EquationFact, PointCoordinates, IntersectionReduction, LineParameterization


@dataclass(frozen=True)
class BoundAction:
    model_id: int
    mode: str
    curve: str | None = None
    equation_id: str | None = None
    line_equation_id: str | None = None
    relation_id: str | None = None
    peer_curve: str | None = None
    peer_equation_id: str | None = None
    point: str | None = None
    coordinate_id: str | None = None
    line: str | None = None
    point_role: str | None = None
    incidence_id: str | None = None


@dataclass
class Proposal:
    properties: dict = field(default_factory=dict)
    values: dict = field(default_factory=dict)
    read_facts: tuple[str, ...] = ()
    operations: list[dict] = field(default_factory=list)
    candidates: tuple = ()
    constraints: dict = field(default_factory=dict)
    frames: dict[str, CurveFrame] = field(default_factory=dict)
    equations: dict[str, EquationFact] = field(default_factory=dict)
    coordinates: dict[str, PointCoordinates] = field(default_factory=dict)
    intersection_reductions: dict[str, IntersectionReduction] = field(default_factory=dict)
    parameterizations: dict[str, LineParameterization] = field(default_factory=dict)


@dataclass
class TransitionResult:
    status: str
    action: BoundAction
    before_revision: int
    after_revision: int
    delta: dict = field(default_factory=dict)
    read_facts: tuple[str, ...] = ()
    operations: list[dict] = field(default_factory=list)
    candidates: tuple = ()
    diagnostic: str = ''


def check_binding(state, action):
    if action.model_id == 78 and action.mode == 'parameterize_named_line':
        curve = state.equations.get(action.equation_id)
        intersection = state.named_intersections.get(action.relation_id)
        point = state.coordinates.get(action.point)
        incidence = state.incidences.get(action.incidence_id)
        if (curve is None or curve.owner != action.curve or curve.role != 'curve'
                or state.entities.get(action.curve) != 'Parabola'
                or action.line not in state.named_lines or intersection is None
                or (intersection.line, intersection.curve) != (action.line, action.curve)
                or point is None or point.fact_id != action.coordinate_id
                or incidence is None or (incidence.point, incidence.curve) != (action.point, action.line)
                or any(v is not None for v in (action.line_equation_id, action.peer_curve,
                                               action.peer_equation_id, action.point_role))):
            raise TransitionError('inapplicable', 'Named line parameterization binding mismatch')
        return curve
    if action.incidence_id is not None:
        raise TransitionError('inapplicable', 'Incidence binding only valid for named parameterization')

    if action.model_id in (42, 43, 50):
        check_binding(state, replace(action, model_id=78, relation_id=None))
        fact = state.intersection_reductions.get(action.relation_id)
        if (fact is None or fact.fact_id != action.relation_id
                or fact.fact_id != f'derived:intersection:{action.equation_id}:{action.line_equation_id}'
                or (fact.curve, fact.line, fact.curve_equation_id, fact.line_equation_id)
                != (action.curve, action.line, action.equation_id, action.line_equation_id)):
            raise TransitionError('inapplicable', 'Intersection reduction binding mismatch')
        return fact
    if action.model_id == 78:
        curve = state.equations.get(action.equation_id)
        line = state.equations.get(action.line_equation_id)
        if (state.entities.get(action.curve) != 'Parabola' or state.entities.get(action.line) != 'Line'
                or curve is None or curve.owner != action.curve or curve.role != 'curve'
                or line is None or line.owner != action.line or line.role != 'line'
                or any(v is not None for v in (action.relation_id, action.peer_curve,
                    action.peer_equation_id, action.point, action.coordinate_id, action.point_role))):
            raise TransitionError('inapplicable', 'Line/parabola equation binding mismatch')
        return curve

    if action.model_id == 39:
        fact = state.equations.get(action.equation_id)
        point = state.coordinates.get(action.point)
        if (state.entities.get(action.curve) != 'Parabola' or state.entities.get(action.point) != 'Point'
                or fact is None or fact.owner != action.curve or fact.role != 'curve'
                or point is None or point.fact_id != action.coordinate_id
                or any(v is not None for v in (action.line, action.line_equation_id, action.relation_id,
                                               action.point_role, action.peer_curve, action.peer_equation_id))):
            raise TransitionError('inapplicable', 'Tangent point/curve binding mismatch')
        return fact
    if action.model_id == 13:
        fact = state.equations.get(action.equation_id)
        if (state.entities.get(action.curve) not in ('Ellipse', 'Hyperbola')
                or fact is None or fact.owner != action.curve or fact.role != 'curve'
                or any(v is not None for v in (action.line, action.line_equation_id, action.point,
                       action.coordinate_id, action.relation_id, action.point_role, action.peer_curve,
                       action.peer_equation_id))):
            raise TransitionError('inapplicable', 'Eccentricity curve binding mismatch')
        return fact
    if action.point_role is not None:
        curve = state.equations.get(action.equation_id)
        line = state.equations.get(action.line_equation_id)
        if (action.model_id != 52 or action.point_role != 'focus'
                or action.mode != 'focus_line_distance'
                or action.point is not None or action.coordinate_id is not None or action.relation_id is not None
                or state.entities.get(action.curve) != 'Parabola' or state.entities.get(action.line) != 'Line'
                or curve is None or curve.owner != action.curve or curve.role != 'curve'
                or line is None or line.owner != action.line or line.role != 'line'):
            raise TransitionError('inapplicable', 'Focus/line binding mismatch')
        return curve
    if action.model_id == 72:
        fact = state.equations.get(action.line_equation_id)
        coordinate = state.coordinates.get(action.point)
        incidence = state.incidences.get(action.relation_id)
        if (action.curve is not None or action.equation_id is not None
                or state.entities.get(action.line) != 'Line'
                or fact is None or fact.owner != action.line or fact.role != 'line'
                or coordinate is None or coordinate.fact_id != action.coordinate_id
                or incidence is None or incidence.point != action.point or incidence.curve != action.line):
            raise TransitionError('inapplicable', 'Line recovery binding mismatch')
        return fact
    if action.model_id == 52 and action.line is not None:
        line = state.equations.get(action.line_equation_id)
        coordinate = state.coordinates.get(action.point)
        if (action.curve is not None or action.equation_id is not None
                or state.entities.get(action.line) != 'Line'
                or line is None
                or (line, action.relation_id) not in state.line_bindings(action.line)
                or state.entities.get(action.point) != 'Point'
                or coordinate is None or coordinate.fact_id != action.coordinate_id):
            raise TransitionError('inapplicable', 'Point/independent line binding mismatch')
        return line
    if action.line is not None:
        raise TransitionError('inapplicable', 'Independent line binding only supported by RM52')
    expected = {3: 'Ellipse', 4: 'Ellipse', 11: 'Ellipse', 5: 'Hyperbola', 6: 'Hyperbola', 12: 'Hyperbola', 21: 'Hyperbola'}
    expected.update({mid: 'Parabola' for mid in (2, 7, 8, 9, 10, 17, 29, 52)})
    if action.model_id not in expected or state.entities.get(action.curve) != expected[action.model_id]:
        raise TransitionError('inapplicable', 'Unsupported model or curve type binding')
    fact = state.equations.get(action.equation_id)
    parameter_mode = action.model_id in (11, 12) and action.mode in (
        'derive_a_sq', 'derive_b_sq', 'derive_c_sq', 'constrain_parameters')
    if parameter_mode and action.equation_id is None:
        if any(f.owner == action.curve and f.role == 'curve' for f in state.equations.values()):
            raise TransitionError('inapplicable', 'Bind an existing curve equation explicitly')
        return None  # Intrinsic parameter relations do not require an axis or equation.
    if fact is None or fact.owner != action.curve or fact.role != 'curve':
        raise TransitionError('inapplicable', 'Curve equation binding mismatch')
    if action.model_id in (2, 17) or (action.model_id in (7, 8, 9, 10) and action.mode == 'recover_from_point'):
        incidence = state.incidences.get(action.relation_id)
        coordinate = state.coordinates.get(action.point)
        if (incidence is None or incidence.point != action.point or incidence.curve != action.curve
                or coordinate is None or coordinate.fact_id != action.coordinate_id):
            raise TransitionError('inapplicable', 'Point coordinate/incidence binding mismatch')
    if action.model_id in (2, 52):
        line = state.equations.get(action.line_equation_id)
        coordinate = state.coordinates.get(action.point)
        if (line is None or line.owner != action.curve or line.role != 'directrix'
                or coordinate is None or coordinate.fact_id != action.coordinate_id):
            raise TransitionError('inapplicable', 'Point/directrix binding mismatch')
    if action.model_id == 21 and action.mode == 'constrain_parameters':
        line = state.equations.get(action.line_equation_id)
        if line is None or line.owner != action.curve or line.role != 'asymptote':
            raise TransitionError('inapplicable', 'Asymptote does not belong to bound curve')
    if action.model_id == 12 and action.mode == 'constrain_shared_focus':
        relation = state.relations.get(action.relation_id)
        peer = state.equations.get(action.peer_equation_id)
        if (relation is None or action.peer_curve == action.curve
                or set(relation.curves) != {action.curve, action.peer_curve}
                or state.entities.get(action.peer_curve) != 'Ellipse'
                or peer is None or peer.owner != action.peer_curve or peer.role != 'curve'):
            raise TransitionError('inapplicable', 'Shared-focus relation or peer binding mismatch')
    return fact


def bound_axis(state, curve, equation_id):
    frame = state.frames.get(curve)
    if (frame is None or frame.equation_id != equation_id or frame.axis not in ('x', 'y')
            or frame.center != (sp.S.Zero, sp.S.Zero)):
        raise TransitionError('inapplicable', 'Missing matching centered x/y frame')
    return frame.axis


def bound_parameters(state, curve, equation_id):
    """Require prior standard-model facts and verify their equation/frame binding."""
    fact = state.equations[equation_id]
    if fact.owner != curve or fact.role != 'curve':
        raise TransitionError('inapplicable', 'Parameter equation binding mismatch')
    if curve not in state.frames or any((curve, k) not in state.properties for k in ('a_sq', 'b_sq')):
        raise TransitionError('inapplicable', 'Missing standard-model parameters or frame')
    axis = bound_axis(state, curve, equation_id)
    operation = ellipse_parameters if state.entities[curve] == 'Ellipse' else hyperbola_parameters
    expected = operation(fact.expression, state.symbols['x'], state.symbols['y'],
                         list(state.constraints.values()), axis)
    for key, value in zip(('a_sq', 'b_sq'), expected):
        if sp.simplify((state.properties[curve, key] - value).subs(state.values)) != 0:
            raise TransitionError('conflict', 'Parameters do not match bound equation')
    return tuple(state.properties[curve, key] for key in ('a_sq', 'b_sq'))


def enumerate_actions(state: TransitionState, model_id: int, mode: str | None = None):
    if model_id in (42, 43, 50):
        name = {42: 'derive_root_sum', 43: 'derive_root_product', 50: 'derive_chord_length'}[model_id]
        actions = [BoundAction(model_id, name, f.curve, f.curve_equation_id,
                               line=f.line, line_equation_id=f.line_equation_id, relation_id=f.fact_id)
                   for f in state.intersection_reductions.values()]
        return [a for a in actions if mode is None or a.mode == mode]
    if model_id == 78:
        actions = [BoundAction(78, 'substitute_line', c.owner, c.fact_id,
                               line=l.owner, line_equation_id=l.fact_id)
                   for c in state.equations.values() if c.role == 'curve'
                   and state.entities.get(c.owner) == 'Parabola'
                   for l in state.equations.values() if l.role == 'line'
                   and state.entities.get(l.owner) == 'Line']
        actions += [BoundAction(78, 'parameterize_named_line', n.curve, c.fact_id,
                                relation_id=n.fact_id, line=n.line, point=i.point,
                                coordinate_id=state.coordinates[i.point].fact_id, incidence_id=i.fact_id)
                    for n in state.named_intersections.values()
                    for c in state.equations.values() if c.owner == n.curve and c.role == 'curve'
                    for i in state.incidences.values() if i.curve == n.line and i.point in state.coordinates]
        return [a for a in actions if mode is None or a.mode == mode]
    if model_id == 39:
        actions = [BoundAction(39, 'derive_tangent', f.owner, f.fact_id,
                               point=p, coordinate_id=c.fact_id)
                   for f in state.equations.values() if f.role == 'curve'
                   and state.entities.get(f.owner) == 'Parabola' for p, c in state.coordinates.items()]
        return [a for a in actions if mode is None or a.mode == mode]
    if model_id == 13:
        actions = [BoundAction(13, 'derive_eccentricity', f.owner, f.fact_id)
                   for f in state.equations.values() if f.role == 'curve'
                   and state.entities.get(f.owner) in ('Ellipse', 'Hyperbola')]
        return [a for a in actions if mode is None or a.mode == mode]
    if model_id == 72:
        actions = []
        for fact in state.equations.values():
            if fact.role != 'line' or state.entities.get(fact.owner) != 'Line':
                continue
            for inc in state.incidences.values():
                coordinate = state.coordinates.get(inc.point)
                if inc.curve == fact.owner and coordinate:
                    actions.append(BoundAction(72, 'recover_from_point', line=fact.owner,
                                               line_equation_id=fact.fact_id, point=inc.point,
                                               coordinate_id=coordinate.fact_id, relation_id=inc.fact_id))
        return [a for a in actions if mode is None or a.mode == mode]
    if model_id in (2, 29, 52):
        actions = []
        if model_id == 52:
            for name, kind in state.entities.items():
                if kind != 'Line':
                    continue
                for line, alias_id in state.line_bindings(name):
                    actions.extend(BoundAction(52, 'point_line_distance', line=name,
                                               line_equation_id=line.fact_id, point=point,
                                               coordinate_id=coordinate.fact_id, relation_id=alias_id)
                                   for point, coordinate in state.coordinates.items())
        for fact in state.equations.values():
            if fact.role != 'curve' or state.entities.get(fact.owner) != 'Parabola':
                continue
            if model_id == 29:
                actions.append(BoundAction(29, 'derive_directrix', fact.owner, fact.fact_id))
                continue
            for line in state.equations.values():
                if line.owner != fact.owner or line.role != 'directrix':
                    continue
                for point, coordinate in state.coordinates.items():
                    base = BoundAction(model_id, 'point_line_distance' if model_id == 52 else 'focal_from_directrix',
                                       fact.owner, fact.fact_id, line.fact_id,
                                       point=point, coordinate_id=coordinate.fact_id)
                    if model_id == 52:
                        actions.append(base)
                    else:
                        actions.extend(replace(base, relation_id=inc.fact_id) for inc in state.incidences.values()
                                       if inc.point == point and inc.curve == fact.owner)
        if model_id == 52:
            for curve in state.equations.values():
                if curve.role != 'curve' or state.entities.get(curve.owner) != 'Parabola':
                    continue
                for line in state.equations.values():
                    if line.role == 'line' and state.entities.get(line.owner) == 'Line':
                        actions.append(BoundAction(52, 'focus_line_distance', curve.owner, curve.fact_id,
                                                   line.fact_id, line=line.owner, point_role='focus'))
        return [a for a in actions if mode is None or a.mode == mode]
    if model_id in (7, 8, 9, 10, 17):
        actions = []
        for fact in state.equations.values():
            if fact.role != 'curve' or state.entities.get(fact.owner) != 'Parabola':
                continue
            if model_id != 17:
                actions.append(BoundAction(model_id, 'extract_parameters', fact.owner, fact.fact_id))
            for incidence in state.incidences.values():
                coordinate = state.coordinates.get(incidence.point)
                if incidence.curve == fact.owner and coordinate:
                    actions.append(BoundAction(model_id, 'focal_radius' if model_id == 17 else 'recover_from_point',
                                               fact.owner, fact.fact_id, relation_id=incidence.fact_id,
                                               point=incidence.point, coordinate_id=coordinate.fact_id))
        return [a for a in actions if mode is None or a.mode == mode]
    if model_id not in (3, 4, 5, 6, 11, 12, 21):
        return []
    actions = []
    for fact in state.equations.values():
        kind = 'Ellipse' if model_id in (3, 4, 11) else 'Hyperbola'
        if fact.role != 'curve' or state.entities.get(fact.owner) != kind:
            continue
        if model_id in (3, 4, 5, 6, 11):
            action_mode = 'derive_c_sq' if model_id == 11 else 'extract_parameters'
            actions.append(BoundAction(model_id, action_mode, fact.owner, fact.fact_id))
        elif model_id == 12:
            for relation in state.relations.values():
                if fact.owner not in relation.curves:
                    continue
                peer = next(c for c in relation.curves if c != fact.owner)
                for eq in state.equations.values():
                    if eq.owner == peer and eq.role == 'curve' and state.entities[peer] == 'Ellipse':
                        actions.append(BoundAction(12, 'constrain_shared_focus', fact.owner,
                                                   fact.fact_id, relation_id=relation.fact_id,
                                                   peer_curve=peer, peer_equation_id=eq.fact_id))
        else:
            for line in state.equations.values():
                if line.owner == fact.owner and line.role == 'asymptote':
                    actions.append(BoundAction(21, 'constrain_parameters', fact.owner,
                                               fact.fact_id, line.fact_id))
    if model_id in (11, 12):
        kind = 'Ellipse' if model_id == 11 else 'Hyperbola'
        for curve, entity_type in state.entities.items():
            if entity_type != kind:
                continue
            equations = [f.fact_id for f in state.equations.values()
                         if f.owner == curve and f.role == 'curve'] or [None]
            for equation_id in equations:
                for parameter_mode in ('derive_a_sq', 'derive_b_sq', 'derive_c_sq', 'constrain_parameters'):
                    action = BoundAction(model_id, parameter_mode, curve, equation_id)
                    if action not in actions:
                        actions.append(action)
    if model_id == 21:
        for fact in state.equations.values():
            if fact.role == 'curve' and state.entities.get(fact.owner) == 'Hyperbola':
                actions.append(BoundAction(21, 'derive_asymptotes', fact.owner, fact.fact_id))
    return [action for action in actions if mode is None or action.mode == mode]


class BoundApplicator:
    def __init__(self, library=None):
        if library is None:
            from .theorem_library import TheoremLibrary
            library = TheoremLibrary()
        self.library = library

    def apply(self, state: TransitionState, action: BoundAction) -> TransitionResult:
        result = TransitionResult('failed', action, state.revision, state.revision)
        try:
            check_binding(state, action)
            ensure_consistent([c.subs(state.values) for c in state.constraints.values()])
            model = self.library.get_model(action.model_id)
            if model is None:
                raise TransitionError('inapplicable', 'Model is not registered')
            # Isolate even a misbehaving proposal method from the caller's state.
            proposal = model.propose_bound(deepcopy(state), action)
            result.read_facts = proposal.read_facts
            result.operations = proposal.operations
            result.candidates = proposal.candidates
            if len(proposal.candidates) > 1:
                result.status = 'undetermined'
                result.diagnostic = 'Multiple admissible roots; branch selection is not implemented'
                return result
            values = dict(state.values)
            for symbol, value in proposal.values.items():
                value = sp.simplify(value)
                if value.free_symbols or value.is_real is not True or value.is_finite is not True:
                    raise TransitionError('undetermined', 'Only finite real scalar assignments supported')
                if symbol in values and sp.simplify(values[symbol]-value) != 0:
                    raise TransitionError('conflict', 'Conflicting scalar assignment')
                values[symbol] = value
            constraints = dict(state.constraints)
            for key, condition in proposal.constraints.items():
                if key in constraints and constraints[key] != condition:
                    raise TransitionError('conflict', 'Constraint ID collision')
                constraints[key] = condition
            ensure_consistent([c.subs(values) for c in constraints.values()])
            for condition in constraints.values():
                valid = truth(condition.subs(values))
                if valid is False:
                    raise TransitionError('conflict', 'Assignment violates a given/domain constraint')
                if proposal.values and valid is None and condition.free_symbols.intersection(proposal.values):
                    raise TransitionError('undetermined', 'Assignment has unresolved constraints')
            frames = dict(state.frames)
            for curve, frame in proposal.frames.items():
                if curve in frames and frames[curve] != frame:
                    raise TransitionError('conflict', 'Conflicting curve frame or equation binding')
                frames[curve] = frame
            properties = dict(state.properties)
            for key, value in proposal.properties.items():
                value = sp.simplify(value.subs(values))
                if key in properties:
                    equal = truth(sp.Eq(properties[key].subs(values), value))
                    if equal is not True:
                        raise TransitionError('conflict' if equal is False else 'undetermined',
                                              'Object property is inconsistent or unresolved')
                properties[key] = value
            # Only substitute known scalar assignments into existing properties.
            # No new theorem, variable solving, or model choice occurs here.
            for key, value in list(properties.items()):
                reduced = sp.simplify(value.subs(values))
                if reduced != value:
                    result.operations.append({'operation': 'restricted_substitution',
                                              'property': key, 'before': value, 'after': reduced,
                                              'substitution': dict(values)})
                properties[key] = reduced
            changed_properties = {k: v for k, v in properties.items() if state.properties.get(k) != v}
            changed_values = {k: v for k, v in values.items() if state.values.get(k) != v}
            changed_constraints = {k: v for k, v in constraints.items() if k not in state.constraints}
            changed_frames = {k: v for k, v in frames.items() if k not in state.frames}
            equations = dict(state.equations)
            for key, fact in proposal.equations.items():
                tangent = (action.model_id == 39 and fact.role == 'tangent'
                           and key == f'derived:{action.curve}:tangent:{action.point}')
                named_line = (action.model_id == 78 and action.mode == 'parameterize_named_line'
                              and fact.role == 'line' and fact.owner == action.line
                              and key == f'derived:{action.line}:parameterized'
                              and action.line in proposal.parameterizations)
                if not named_line and (key != fact.fact_id or fact.owner != action.curve or (fact.role not in ('asymptote', 'directrix') and not tangent)):
                    raise TransitionError('inapplicable', 'Invalid derived equation binding')
                if key != fact.fact_id:
                    raise TransitionError('inapplicable', 'Invalid derived equation binding')
                normalized = replace(fact, expression=sp.simplify(fact.expression.subs(values)))
                if key in equations:
                    old = equations[key]
                    if (old.owner != fact.owner or old.role != fact.role
                            or sp.simplify(old.expression.subs(values)-normalized.expression) != 0):
                        raise TransitionError('conflict', 'Conflicting derived equation')
                else:
                    equations[key] = normalized
            # Preserve given equations; only reduce model-produced equations.
            for key, fact in list(equations.items()):
                if key.startswith('derived:'):
                    reduced = sp.simplify(fact.expression.subs(values))
                    if reduced != fact.expression:
                        result.operations.append({'operation': 'restricted_substitution',
                                                  'equation': key, 'before': fact.expression,
                                                  'after': reduced, 'substitution': dict(values)})
                        equations[key] = replace(fact, expression=reduced)
            coordinates = dict(state.coordinates)
            for point, coordinate in proposal.coordinates.items():
                aliases = [a for a in state.focus_aliases.values() if a.point == point]
                if (action.model_id not in (7, 8, 9, 10) or len(aliases) != 1
                        or aliases[0].curve != action.curve or aliases[0].fact_id not in proposal.read_facts
                        or state.entities.get(point) != 'Point' or coordinate.point != point
                        or coordinate.fact_id != f'derived:{action.curve}:focus:{point}'
                        or len(coordinate.xy) != 2):
                    raise TransitionError('inapplicable', 'Invalid focus coordinate proposal binding')
                xy = tuple(sp.simplify(v.subs(values)) for v in coordinate.xy)
                if any(v.free_symbols or v.is_real is not True or v.is_finite is not True for v in xy):
                    raise TransitionError('undetermined', 'Focus coordinates require finite real numbers')
                if any(properties.get((action.curve, k)) != v for k, v in zip(('focus_x', 'focus_y'), xy)):
                    raise TransitionError('conflict', 'Coordinates do not match focus properties')
                if point in coordinates:
                    equal = [truth(sp.Eq(old.subs(values), new)) for old, new in zip(coordinates[point].xy, xy)]
                    if not all(v is True for v in equal):
                        raise TransitionError('conflict' if False in equal else 'undetermined',
                                              'Existing point coordinates disagree with focus')
                else:
                    coordinates[point] = replace(coordinate, xy=xy)
            parameterizations = dict(state.parameterizations)
            for line, fact in proposal.parameterizations.items():
                if (action.model_id != 78 or action.mode != 'parameterize_named_line'
                        or line != action.line or fact.line != line
                        or (fact.point, fact.coordinate_id, fact.incidence_id, fact.intersection_id)
                        != (action.point, action.coordinate_id, action.incidence_id, action.relation_id)
                        or fact.parameter != sp.Symbol(f'@parameter:{line}:u', real=True)
                        or fact.line_equation_id != f'derived:{line}:parameterized'
                        or fact.line_equation_id not in proposal.equations):
                    raise TransitionError('inapplicable', 'Invalid local parameter binding')
                if line in parameterizations and parameterizations[line] != fact:
                    raise TransitionError('conflict', 'Conflicting line parameterization')
                parameterizations[line] = fact
            changed_parameterizations = {k:v for k,v in parameterizations.items() if k not in state.parameterizations}
            reductions = dict(state.intersection_reductions)
            for key, fact in proposal.intersection_reductions.items():
                parameterized = action.mode == 'parameterize_named_line'
                line_id = f'derived:{action.line}:parameterized' if parameterized else action.line_equation_id
                if parameterized:
                    n = state.named_intersections[action.relation_id]
                    if (action.line not in proposal.parameterizations or fact.named_points != n.points
                            or fact.intersection_id != n.fact_id):
                        raise TransitionError('inapplicable', 'Invalid unordered named-root association')
                if (action.model_id != 78 or action.mode not in ('substitute_line', 'parameterize_named_line')
                        or key != fact.fact_id
                        or key != f'derived:intersection:{action.equation_id}:{line_id}'
                        or (fact.curve, fact.line, fact.curve_equation_id, fact.line_equation_id)
                        != (action.curve, action.line, action.equation_id, line_id)
                        or not {action.equation_id, action.relation_id if parameterized else line_id}.issubset(proposal.read_facts)):
                    raise TransitionError('inapplicable', 'Invalid intersection reduction binding')
                if key in reductions and reductions[key] != fact:
                    raise TransitionError('conflict', 'Conflicting intersection reduction')
                reductions[key] = fact
            changed_reductions = {k: v for k, v in reductions.items() if k not in state.intersection_reductions}
            changed_coordinates = {p: c for p, c in coordinates.items() if p not in state.coordinates}
            changed_equations = {k: v for k, v in equations.items() if state.equations.get(k) != v}
            if not any((changed_properties, changed_values, changed_constraints, changed_frames, changed_equations, changed_coordinates, changed_reductions, changed_parameterizations)):
                result.status = 'no_op'
                return result
            result.delta = {'properties': changed_properties, 'values': changed_values}
            if changed_constraints:
                result.delta['constraints'] = changed_constraints
            if changed_frames:
                result.delta['frames'] = changed_frames
            if changed_equations:
                result.delta['equations'] = changed_equations
            if changed_coordinates:
                result.delta['coordinates'] = changed_coordinates
            if changed_reductions:
                result.delta['intersection_reductions'] = changed_reductions
            if changed_parameterizations:
                result.delta['parameterizations'] = changed_parameterizations
            result.status = 'applied'
            result.after_revision += 1
            provenance = dict(state.provenance)
            for key in changed_properties:
                source_key = f'property:{key[0]}:{key[1]}'
                provenance[source_key] = tuple(dict.fromkeys(
                    (*provenance.get(source_key, ()), *proposal.read_facts,
                     f'action:{result.after_revision}')))
            for key in changed_values:
                provenance[f'value:{key}'] = (*proposal.read_facts, f'action:{result.after_revision}')
            for key in (*changed_constraints, *(f'frame:{c}' for c in changed_frames)):
                provenance[key] = (*proposal.read_facts, f'action:{result.after_revision}')
            for key in changed_equations:
                provenance[key] = tuple(dict.fromkeys(
                    (*provenance.get(key, ()), *proposal.read_facts, f'action:{result.after_revision}')))
            for key in changed_reductions:
                provenance[key] = (*proposal.read_facts, f'action:{result.after_revision}')
            for coordinate in changed_coordinates.values():
                provenance[coordinate.fact_id] = (*proposal.read_facts, f'action:{result.after_revision}')
            for line in changed_parameterizations:
                provenance[f'parameterization:{line}'] = (*proposal.read_facts, f'action:{result.after_revision}')
            state.parameterizations = parameterizations
            state.intersection_reductions = reductions
            state.coordinates = coordinates
            state.properties, state.values, state.provenance = properties, values, provenance
            state.constraints, state.frames = constraints, frames
            state.equations = equations
            state.revision = result.after_revision
            state.history.append(deepcopy(result))
        except TransitionError as exc:
            result.status, result.diagnostic = exc.status, str(exc)
        except (ValueError, TypeError, KeyError, NotImplementedError, sp.PolynomialError) as exc:
            result.status, result.diagnostic = 'failed', str(exc)
        return result
