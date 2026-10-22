"""Declared segment midpoint aliases and immutable input-coordinate snapshots."""
from dataclasses import dataclass, replace
import re
import sympy as sp
from .chord_facts import store_chord_midpoint
from src.solver.transition_primitives import TransitionError


@dataclass(frozen=True)
class ChordMidpointAlias:
    chord_id: str
    segment: str
    point: str
    sources: tuple[str, ...]
    coordinate_id: str | None = None
    xy: tuple[sp.Expr, sp.Expr] | None = None


def collect_midpoint_aliases(state, parts):
    consumed = set()
    for i,text in enumerate(parts):
        match = re.fullmatch(r'MidPoint\(\s*([A-Za-z]\w*)\s*\)\s*=\s*([A-Za-z]\w*)',text)
        if not match:
            continue
        segment,point = match.groups()
        relation = state.segment_chords.get(segment)
        if relation is None or state.entities.get(point)!='Point':
            raise ValueError('Midpoint alias requires a segment chord and declared Point')
        key = f'@chord:{relation.line}:{relation.curve}'
        old = state.midpoint_aliases.get(key)
        if old and old.point!=point:
            raise ValueError('Conflicting midpoint aliases for one chord')
        sources = (*old.sources,f'f{i}') if old else (f'f{i}',)
        state.midpoint_aliases[key] = ChordMidpointAlias(key,segment,point,sources)
        consumed.add(i)
    return consumed


def resolve_midpoint_aliases(state):
    """Resolve only given numeric coordinates after normal input parsing."""
    for key,alias in list(state.midpoint_aliases.items()):
        coordinate = state.coordinates.get(alias.point)
        if coordinate is None:
            continue
        alias = replace(alias,coordinate_id=coordinate.fact_id,xy=coordinate.xy)
        state.midpoint_aliases[key] = alias
        if any(v.free_symbols for v in coordinate.xy):
            continue
        chord = state.chords[key]
        for source in (*alias.sources,coordinate.fact_id):
            store_chord_midpoint(state,chord.line,chord.curve,
                                 str(coordinate.xy[0]),str(coordinate.xy[1]),source)
        state.chord_midpoints[key] = replace(state.chord_midpoints[key],alias_point=alias.point)


def check_midpoint_alias(state, chord):
    """Reject stale input snapshots; never refresh or derive coordinates here."""
    alias = state.midpoint_aliases.get(chord.chord_id)
    midpoint = state.chord_midpoints.get(chord.chord_id)
    if alias is None:
        if midpoint and midpoint.alias_point is not None:
            raise TransitionError('inapplicable','Missing midpoint alias record')
        return
    relation = state.segment_chords.get(alias.segment)
    if (alias.chord_id!=chord.chord_id or relation is None
            or (relation.line,relation.curve)!=(chord.line,chord.curve)
            or state.entities.get(alias.point)!='Point' or not alias.sources):
        raise TransitionError('inapplicable','Mismatched midpoint alias binding')
    coordinate = state.coordinates.get(alias.point)
    if coordinate is None:
        raise TransitionError('inapplicable','Missing midpoint coordinate')
    if (coordinate.point!=alias.point or coordinate.fact_id!=alias.coordinate_id
            or coordinate.xy!=alias.xy):
        raise TransitionError('conflict','Stale midpoint coordinate snapshot')
    if any(v.free_symbols or v.is_real is not True or v.is_finite is not True for v in coordinate.xy):
        raise TransitionError('undetermined','Numeric midpoint alias coordinate required')
    if (midpoint is None or midpoint.alias_point!=alias.point
            or not set((*alias.sources,coordinate.fact_id)).issubset(midpoint.sources)
            or any(sp.simplify(a-b)!=0 for a,b in zip(midpoint.xy,coordinate.xy))):
        raise TransitionError('conflict','Midpoint value or provenance contradicts alias snapshot')
