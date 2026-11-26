"""Read-only two-directrix identity and input/output freshness stamps."""
from dataclasses import dataclass
import hashlib
from src.solver.midpoint_operations import canonical_numeric_line
from src.solver.transition_primitives import TransitionError


@dataclass(frozen=True)
class DirectrixPairQuery:
    curve: str


def pair_keys(curve):
    return tuple(f'derived:{curve}:directrix:{side}' for side in ('negative', 'positive'))


def pair_snapshot(state, curve, expression):
    """Fingerprint inputs and a normalized output; does not derive a directrix."""
    originals = tuple((k, repr(f)) for k, f in sorted(state.equations.items()) if f.owner == curve and f.role == 'curve')
    reads = (f'frame:{curve}', *(f'property:{curve}:{p}' for p in ('a_sq', 'b_sq', 'c_sq')))
    payload = (originals, repr(state.frames.get(curve)),
               tuple(str(state.properties.get((curve, p))) for p in ('a_sq', 'b_sq', 'c_sq')),
               tuple((k, state.provenance.get(k)) for k in reads),
               tuple(sorted((str(k), str(v)) for k, v in state.values.items())),
               str(canonical_numeric_line(expression, state.symbols['x'], state.symbols['y'])))
    return 'RM28:' + hashlib.sha256(repr(payload).encode()).hexdigest()


def read_directrix_pair(state, query):
    keys = pair_keys(query.curve)
    originals = [f for f in state.equations.values() if f.owner == query.curve and f.role == 'curve']
    actual = {k for k, f in state.equations.items() if f.owner == query.curve and f.role == 'directrix'}
    if state.entities.get(query.curve) != 'Hyperbola' or len(originals) != 1 or actual != set(keys):
        return None
    lines = []
    for key in keys:
        f = state.equations[key]
        try:
            if (f.fact_id != key or originals[0].fact_id not in state.provenance.get(key, ())
                    or f.source != pair_snapshot(state, query.curve, f.expression)):
                return None
            lines.append(canonical_numeric_line(f.expression, state.symbols['x'], state.symbols['y']))
        except TransitionError:
            return None
    return frozenset(lines) if len(set(lines)) == 2 else None
