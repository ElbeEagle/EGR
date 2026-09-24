"""Explicit asymptote/shared-focus replay slices; not a learned or general solver."""
from __future__ import annotations

from dataclasses import dataclass, field

from src.state.transition_state import TransitionState, AsymptoteQuery
from src.theorems.bound_application import BoundAction, BoundApplicator, enumerate_actions


@dataclass
class SliceResult:
    status: str
    state: TransitionState | None = None
    transitions: list = field(default_factory=list)
    diagnostic: str = ''

    @property
    def answer(self):
        return self.state.extract_answer() if self.state else None


def solve_asymptote_slice(facts: str, query: str) -> SliceResult:
    try:
        state = TransitionState.from_facts(facts, query)
    except (ValueError, SyntaxError) as exc:
        return SliceResult('failed', diagnostic=str(exc))
    actions = enumerate_actions(state, 21, mode='constrain_parameters')
    if len(actions) != 1:
        return SliceResult('undetermined', state, diagnostic='Slice requires one bound curve/asymptote pair')
    inverse = actions[0]
    extract = BoundAction(5, 'extract_parameters', inverse.curve, inverse.equation_id)
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
    return replay_actions(state, (
        BoundAction(3, 'extract_parameters', shared.peer_curve, shared.peer_equation_id),
        BoundAction(11, 'derive_c_sq', shared.peer_curve, shared.peer_equation_id),
        BoundAction(5, 'extract_parameters', shared.curve, shared.equation_id),
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
    return replay_actions(state, (BoundAction(5, 'extract_parameters', forward.curve,
                                             forward.equation_id), forward))


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
    parser.add_argument('--mode', choices=('asymptote', 'shared-focus', 'asymptote-forward'), default='asymptote')
    args = parser.parse_args()
    records = json.loads(Path(args.data).read_text())
    problem = next(item for item in records if item['id'] == args.problem_id)
    solve = {'asymptote': solve_asymptote_slice, 'shared-focus': solve_shared_focus_slice,
             'asymptote-forward': solve_forward_asymptote_slice}[args.mode]
    result = solve(problem['fact_expressions'], problem['query_expressions'])

    def serializable(value):
        if isinstance(value, dict):
            return {str(k): serializable(v) for k, v in value.items()}
        if isinstance(value, (tuple, list)):
            return [serializable(v) for v in value]
        if value is None or isinstance(value, (str, int, float, bool)):
            return value
        return str(value)

    print(json.dumps(serializable({'schema_version': 'bound-slice-v3', 'mode': args.mode,
                                  'problem_id': args.problem_id, 'status': result.status,
                                  'facts': problem['fact_expressions'], 'query': problem['query_expressions'],
                                  'answer': result.answer, 'diagnostic': result.diagnostic,
                                  'transitions': [asdict(t) for t in result.transitions]}),
                     ensure_ascii=False, indent=2))
