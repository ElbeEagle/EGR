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
    chord_sources = tuple(dict.fromkeys((*state.chords[key].sources, *sources))) if key in state.chords else sources
    state.chords[key] = ChordIdentity(key,line,curve,pair,chord_sources)
    state.chord_endpoint_pairs[pair] = AnonymousEndpointPair(pair,key,chord_sources)
    state.chord_midpoints[key] = ChordMidpoint(key,xy,sources)
    state.provenance[key] = chord_sources
    state.provenance[pair] = chord_sources
    return True


@dataclass(frozen=True)
class ChordEndpointNames:
    pair_id: str
    points: tuple[str, str]
    sources: tuple[str, ...]


def collect_named_chords(state, parts):
    """Resolve ellipse endpoint names before parsing facts; never assign coordinates."""
    consumed = set()
    name = r'([A-Za-z]\w*)'
    pattern = rf'Intersection\(\s*{name}\s*,\s*{name}\s*\)\s*=\s*\{{\s*{name}\s*,\s*{name}\s*\}}'
    for i,text in enumerate(parts):
        match = re.fullmatch(pattern,text)
        if not match:
            continue
        left,right,a,b = match.groups()
        if 'Ellipse' not in (state.entities.get(left),state.entities.get(right)):
            continue
        if sorted(state.entities.get(v,'') for v in (left,right)) != ['Ellipse','Line'] or a==b or any(state.entities.get(v)!='Point' for v in (a,b)):
            raise ValueError('Ellipse intersection requires Line and two declared distinct points')
        line,curve = (left,right) if state.entities[left]=='Line' else (right,left)
        key = f'@chord:{line}:{curve}'
        pair = f'{key}:endpoints'
        points = tuple(sorted((a,b)))
        old = state.chord_endpoint_names.get(pair)
        if old and old.points != points:
            raise ValueError('Conflicting endpoint names for one chord')
        if any(v.points==points and v.pair_id!=pair for v in state.chord_endpoint_names.values()):
            raise ValueError('Ambiguous endpoint pair across chords')
        sources = (*old.sources,f'f{i}') if old else (f'f{i}',)
        state.chord_endpoint_names[pair] = ChordEndpointNames(pair,points,sources)
        state.chords[key] = ChordIdentity(key,line,curve,pair,sources)
        state.chord_endpoint_pairs[pair] = AnonymousEndpointPair(pair,key,sources)
        state.provenance[key] = state.provenance[pair] = sources
        consumed.add(i)
    pattern = rf'Coordinate\(\s*MidPoint\(\s*LineSegmentOf\(\s*{name}\s*,\s*{name}\s*\)\s*\)\s*\)\s*=\s*\(([^,]+),([^,]+)\)'
    for i,text in enumerate(parts):
        match = re.fullmatch(pattern,text)
        if not match:
            continue
        a,b,xt,yt = match.groups()
        matches = [c for c in state.chords.values() if c.pair_id in state.chord_endpoint_names
                   and state.chord_endpoint_names[c.pair_id].points==tuple(sorted((a,b)))]
        if len(matches)!=1:
            raise ValueError('Named midpoint requires unique ellipse chord association')
        chord = matches[0]
        parse_chord_midpoint(state,
            f'Coordinate(MidPoint(InterceptChord({chord.line},{chord.curve})))=({xt},{yt})',f'f{i}')
        consumed.add(i)
    return consumed
