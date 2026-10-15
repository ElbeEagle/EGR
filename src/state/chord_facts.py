"""Given chord midpoints and anonymous endpoint identity; no endpoint construction."""
from dataclasses import dataclass
import re
import sympy as sp
from src.solver.transition_primitives import parse_expression


@dataclass(frozen=True)
class ChordIdentity:
    chord_id: str
    line: str
    curve: str
    pair_id: str
    sources: tuple[str, ...]


@dataclass(frozen=True)
class AnonymousEndpointPair:
    pair_id: str
    chord_id: str
    sources: tuple[str, ...]  # Given nondegenerate chord semantics, not computed roots.


@dataclass(frozen=True)
class ChordMidpoint:
    chord_id: str
    xy: tuple[sp.Expr, sp.Expr]
    sources: tuple[str, ...]


def parse_chord_midpoint(state, text: str, fact_id: str) -> bool:
    pattern = r'Coordinate\(\s*MidPoint\(\s*InterceptChord\(\s*([A-Za-z]\w*)\s*,\s*([A-Za-z]\w*)\s*\)\s*\)\s*\)\s*=\s*\(([^,]+),([^,]+)\)'
    match = re.fullmatch(pattern, text)
    if not match:
        return False
    line, curve, xt, yt = match.groups()
    if state.entities.get(line) != 'Line' or state.entities.get(curve) != 'Ellipse':
        raise ValueError('Chord midpoint requires declared Line and Ellipse')
    values = [parse_expression(t, state.symbols) for t in (xt, yt)]
    if any(any(g is not sp.true for g in guards) or v.free_symbols or v.is_real is not True or v.is_finite is not True for v,guards in values):
        raise ValueError('Chord midpoint currently requires finite numeric coordinates')
    xy = tuple(v for v,_ in values)
    key = f'@chord:{line}:{curve}'
    old = state.chord_midpoints.get(key)
    if old and any(sp.simplify(a-b)!=0 for a,b in zip(old.xy,xy)):
        raise ValueError('Conflicting midpoint coordinates for the same chord')
    sources = (*old.sources, fact_id) if old else (fact_id,)
    pair = f'{key}:endpoints'
    state.chords[key] = ChordIdentity(key,line,curve,pair,sources)
    state.chord_endpoint_pairs[pair] = AnonymousEndpointPair(pair,key,sources)
    state.chord_midpoints[key] = ChordMidpoint(key,xy,sources)
    state.provenance[key] = sources
    state.provenance[pair] = sources
    return True
