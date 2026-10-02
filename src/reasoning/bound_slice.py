"""Explicit asymptote/shared-focus replay slices; not a learned or general solver."""
from __future__ import annotations

from dataclasses import dataclass, field, replace
from copy import deepcopy

from src.state.transition_state import TransitionState, AsymptoteQuery, FocalDistanceQuery, PointLineDistanceQuery, FocusLineDistanceQuery
from src.theorems.bound_application import BoundAction, BoundApplicator, enumerate_actions
from src.solver.transition_primitives import TransitionError


@dataclass
class SliceResult:
    status: str
    state: TransitionState | None = None
    transitions: list = field(default_factory=list)
    diagnostic: str = ''

    @property
    def answer(self):
        return self.state.extract_answer() if self.state else None


def select_standard_action(state, curve, equation_id):
    """Preflight the two axis-specific modes on copies; never commit a guessed axis."""
    model_ids = (3, 4) if state.entities[curve] == 'Ellipse' else (5, 6)
    app = BoundApplicator()
    probes = [app.apply(deepcopy(state), BoundAction(mid, 'extract_parameters', curve, equation_id))
              for mid in model_ids]
    accepted = [p.action for p in probes if p.status in ('applied', 'no_op')]
    if len(accepted) == 1:
        return accepted[0]
    if accepted:
        raise TransitionError('undetermined', 'More than one standard axis remains admissible')
    for status in ('conflict', 'undetermined', 'failed', 'inapplicable'):
        failure = next((p for p in probes if p.status == status), None)
        if failure:
            raise TransitionError(status, failure.diagnostic)
    raise TransitionError('inapplicable', 'No standard curve mode applies')


def solve_asymptote_slice(facts: str, query: str) -> SliceResult:
    try:
        state = TransitionState.from_facts(facts, query)
    except (ValueError, SyntaxError) as exc:
        return SliceResult('failed', diagnostic=str(exc))
    actions = enumerate_actions(state, 21, mode='constrain_parameters')
    if len(actions) != 1:
        return SliceResult('undetermined', state, diagnostic='Slice requires one bound curve/asymptote pair')
    inverse = actions[0]
    try:
        extract = select_standard_action(state, inverse.curve, inverse.equation_id)
    except TransitionError as exc:
        return SliceResult(exc.status, state, diagnostic=str(exc))
    return replay_actions(state, (extract, inverse))


def solve_shared_focus_slice(facts: str, query: str) -> SliceResult:
    try:
        state = TransitionState.from_facts(facts, query)
    except (ValueError, SyntaxError) as exc:
        return SliceResult('failed', diagnostic=str(exc))
    actions = enumerate_actions(state, 12, mode='constrain_shared_focus')
    if len(actions) != 1:
        return SliceResult('undetermined', state, diagnostic='Slice requires one hyperbola/ellipse focus binding')
    shared = actions[0]
    try:
        ellipse = select_standard_action(state, shared.peer_curve, shared.peer_equation_id)
        hyperbola = select_standard_action(state, shared.curve, shared.equation_id)
    except TransitionError as exc:
        return SliceResult(exc.status, state, diagnostic=str(exc))
    return replay_actions(state, (
        ellipse,
        BoundAction(11, 'derive_c_sq', shared.peer_curve, shared.peer_equation_id),
        hyperbola,
        shared,
    ))


def solve_forward_asymptote_slice(facts: str, query: str) -> SliceResult:
    try:
        state = TransitionState.from_facts(facts, query)
    except (ValueError, SyntaxError) as exc:
        return SliceResult('failed', diagnostic=str(exc))
    if not isinstance(state.query, AsymptoteQuery):
        return SliceResult('inapplicable', state, diagnostic='Forward slice requires an asymptote-set query')
    actions = [a for a in enumerate_actions(state, 21, 'derive_asymptotes')
               if a.curve == state.query.curve]
    if len(actions) != 1:
        return SliceResult('undetermined', state, diagnostic='Query requires one bound curve equation')
    forward = actions[0]
    try:
        extract = select_standard_action(state, forward.curve, forward.equation_id)
    except TransitionError as exc:
        return SliceResult(exc.status, state, diagnostic=str(exc))
    return replay_actions(state, (extract, forward))


def solve_parabola_focal_slice(facts: str, query: str, *, definition=False) -> SliceResult:
    try:
        state = TransitionState.from_facts(facts, query)
    except (ValueError, SyntaxError) as exc:
        return SliceResult('failed', diagnostic=str(exc))
    if not isinstance(state.query, FocalDistanceQuery):
        return SliceResult('inapplicable', state, diagnostic='Requires a point-to-parabola-focus query')
    radius_actions = [a for a in enumerate_actions(state, 17)
                      if a.point == state.query.point and a.curve == state.query.curve]
    if len(radius_actions) != 1:
        return SliceResult('undetermined', state, diagnostic='Requires one point/curve/equation binding')
    radius = radius_actions[0]
    app = BoundApplicator()
    probes = [app.apply(deepcopy(state), replace(radius, model_id=mid, mode='recover_from_point'))
              for mid in (7, 8, 9, 10)]
    accepted = [p.action for p in probes if p.status in ('applied', 'no_op')]
    if len(accepted) == 1:
        if definition:
            line_id = f'derived:{radius.curve}:directrix'
            return replay_actions(state, (
                accepted[0],
                BoundAction(29, 'derive_directrix', radius.curve, radius.equation_id),
                replace(radius, model_id=52, mode='point_line_distance', line_equation_id=line_id,
                        relation_id=None),
                replace(radius, model_id=2, mode='focal_from_directrix', line_equation_id=line_id),
            ))
        return replay_actions(state, (accepted[0], radius))
    if accepted:
        return SliceResult('undetermined', state, diagnostic='Multiple opening modes remain admissible')
    for status in ('conflict', 'undetermined', 'failed', 'inapplicable'):
        failed = next((p for p in probes if p.status == status), None)
        if failed:
            return SliceResult(status, state, transitions=[failed], diagnostic=failed.diagnostic)
    return SliceResult('inapplicable', state)


def solve_parabola_definition_slice(facts: str, query: str) -> SliceResult:
    return solve_parabola_focal_slice(facts, query, definition=True)


def solve_point_line_distance_slice(facts: str, query: str) -> SliceResult:
    """One explicit RM52 step selected by the point/line query, not gold labels."""
    try:
        state = TransitionState.from_facts(facts, query)
    except (ValueError, SyntaxError) as exc:
        return SliceResult('failed', diagnostic=str(exc))
    if not isinstance(state.query, PointLineDistanceQuery):
        return SliceResult('inapplicable', state, diagnostic='Requires a point-to-line query')
    actions = [a for a in enumerate_actions(state, 52, 'point_line_distance')
               if a.line == state.query.line and a.point == state.query.point]
    if len(actions) != 1:
        return SliceResult('undetermined', state, diagnostic='Requires one coordinate/line equation binding')
    return replay_actions(state, actions)


def solve_directrix_alias_distance_slice(facts: str, query: str) -> SliceResult:
    """Fixed standard-parabola -> RM29 -> RM52 replay for a named directrix."""
    try:
        state = TransitionState.from_facts(facts, query)
    except (ValueError, SyntaxError) as exc:
        return SliceResult('failed', diagnostic=str(exc))
    if not isinstance(state.query, PointLineDistanceQuery):
        return SliceResult('inapplicable', state, diagnostic='Requires a named point/line distance query')
    aliases = [a for a in state.directrix_aliases.values() if a.line == state.query.line]
    if len(aliases) != 1 or any(f.owner == state.query.line and f.role == 'line' for f in state.equations.values()):
        return SliceResult('undetermined', state, diagnostic='Requires one alias without additional line equations')
    alias = aliases[0]
    equations = [f for f in state.equations.values() if f.owner == alias.curve and f.role == 'curve']
    coordinate = state.coordinates.get(state.query.point)
    focus_aliases = [a for a in state.focus_aliases.values()
                     if a.point == state.query.point and a.curve == alias.curve]
    if len(equations) != 1 or (coordinate is None and len(focus_aliases) != 1):
        return SliceResult('undetermined', state, diagnostic='Requires one curve equation and point coordinates')
    app = BoundApplicator()
    probes = [app.apply(deepcopy(state), BoundAction(mid, 'extract_parameters', alias.curve, equations[0].fact_id))
              for mid in (7, 8, 9, 10)]
    accepted = [p.action for p in probes if p.status in ('applied', 'no_op')]
    if len(accepted) != 1:
        if accepted:
            return SliceResult('undetermined', state, diagnostic='Ambiguous standard direction')
        failure = next(p for status in ('conflict', 'undetermined', 'failed', 'inapplicable')
                       for p in probes if p.status == status)
        return SliceResult(failure.status, state, transitions=[failure], diagnostic=failure.diagnostic)
    prefix = replay_actions(state, (
        accepted[0], BoundAction(29, 'derive_directrix', alias.curve, equations[0].fact_id),
    ))
    if prefix.status not in ('solved', 'unresolved'):
        return prefix
    coordinate = state.coordinates.get(state.query.point)
    if coordinate is None:
        return SliceResult('undetermined', state, prefix.transitions, 'Missing committed point coordinates')
    tail = replay_actions(state, (BoundAction(
        52, 'point_line_distance', line=alias.line,
        line_equation_id=f'derived:{alias.curve}:directrix', relation_id=alias.fact_id,
        point=state.query.point, coordinate_id=coordinate.fact_id),))
    tail.transitions = prefix.transitions + tail.transitions
    return tail



def solve_intersection_focus_distance_slice(facts: str, query: str) -> SliceResult:
    """Fixed known-intersection recovery followed by focus-to-line distance."""
    try:
        state = TransitionState.from_facts(facts, query)
    except (ValueError, SyntaxError) as exc:
        return SliceResult('failed', diagnostic=str(exc))
    if not isinstance(state.query, FocusLineDistanceQuery):
        return SliceResult('inapplicable', state, diagnostic='Requires Focus(curve)-to-line query')
    distances = [a for a in enumerate_actions(state, 52, 'focus_line_distance')
                 if a.curve == state.query.curve and a.line == state.query.line]
    if len(distances) != 1:
        return SliceResult('undetermined', state, diagnostic='Requires unique curve and line equations')
    distance = distances[0]
    pairs = []
    for line in enumerate_actions(state, 72, 'recover_from_point'):
        if line.line != distance.line or line.line_equation_id != distance.line_equation_id:
            continue
        for incidence in state.incidences.values():
            if incidence.point == line.point and incidence.curve == distance.curve:
                pairs.append((line, incidence))
    if len(pairs) != 1:
        return SliceResult('undetermined', state, diagnostic='Requires a unique shared known point')
    line, incidence = pairs[0]
    app = BoundApplicator()
    probes = [app.apply(deepcopy(state), BoundAction(mid, 'recover_from_point',
              distance.curve, distance.equation_id, point=line.point,
              coordinate_id=line.coordinate_id, relation_id=incidence.fact_id)) for mid in (7, 8, 9, 10)]
    accepted = [p.action for p in probes if p.status in ('applied', 'no_op')]
    if len(accepted) != 1:
        if accepted:
            return SliceResult('undetermined', state, diagnostic='Ambiguous standard direction')
        failure = next(p for status in ('conflict', 'undetermined', 'failed', 'inapplicable')
                       for p in probes if p.status == status)
        return SliceResult(failure.status, state, [failure], failure.diagnostic)
    return replay_actions(state, (accepted[0], line, distance))


def replay_actions(state: TransitionState, actions) -> SliceResult:
    """Run an explicit diagnostic action sequence; retain unsuccessful attempts too."""
    applicator = BoundApplicator()
    result = SliceResult('unresolved', state)
    for action in actions:
        transition = applicator.apply(state, action)
        result.transitions.append(transition)
        if transition.status not in ('applied', 'no_op'):
            result.status, result.diagnostic = transition.status, transition.diagnostic
            return result
    result.status = 'solved' if result.answer is not None else 'unresolved'
    return result


if __name__ == '__main__':
    import argparse
    import json
    from dataclasses import asdict
    from pathlib import Path

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data', default='data/train_with_models_v3.json')
    parser.add_argument('--problem-id', type=int, default=2)
    parser.add_argument('--mode', choices=('asymptote', 'shared-focus', 'asymptote-forward', 'parabola-focal', 'parabola-definition', 'point-line-distance', 'directrix-alias-distance', 'intersection-focus-distance'), default='asymptote')
    args = parser.parse_args()
    records = json.loads(Path(args.data).read_text())
    problem = next(item for item in records if item['id'] == args.problem_id)
    solve = {'asymptote': solve_asymptote_slice, 'shared-focus': solve_shared_focus_slice,
             'asymptote-forward': solve_forward_asymptote_slice,
             'parabola-focal': solve_parabola_focal_slice,
             'parabola-definition': solve_parabola_definition_slice,
             'point-line-distance': solve_point_line_distance_slice,
             'directrix-alias-distance': solve_directrix_alias_distance_slice,
             'intersection-focus-distance': solve_intersection_focus_distance_slice}[args.mode]
    result = solve(problem['fact_expressions'], problem['query_expressions'])

    def serializable(value):
        if isinstance(value, dict):
            return {str(k): serializable(v) for k, v in value.items()}
        if isinstance(value, (tuple, list)):
            return [serializable(v) for v in value]
        if value is None or isinstance(value, (str, int, float, bool)):
            return value
        return str(value)

    print(json.dumps(serializable({'schema_version': 'bound-slice-v7', 'mode': args.mode,
                                  'problem_id': args.problem_id, 'status': result.status,
                                  'facts': problem['fact_expressions'], 'query': problem['query_expressions'],
                                  'answer': result.answer, 'diagnostic': result.diagnostic,
                                  'transitions': [asdict(t) for t in result.transitions]}),
                     ensure_ascii=False, indent=2))
