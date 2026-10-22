"""Segment and named-endpoint midpoint aliases and immutable input-coordinate snapshots."""
from dataclasses import dataclass, replace
import re
import sympy as sp
from .chord_facts import store_chord_midpoint
from src.solver.transition_primitives import TransitionError


@dataclass(frozen=True)
class ChordMidpointAlias:
    chord_id: str
    segment: str | None
    point: str
    sources: tuple[str, ...]
    coordinate_id: str | None = None
    xy: tuple[sp.Expr, sp.Expr] | None = None
    pair_id: str | None = None
    endpoints: tuple[str, str] | None = None


def collect_midpoint_aliases(state, parts):
    consumed = set()
    for i,text in enumerate(parts):
        match = re.fullmatch(r'MidPoint\(\s*([A-Za-z]\w*)\s*\)\s*=\s*([A-Za-z]\w*)',text)
        pair_id = None
        endpoints = None
        if match:
            segment,point = match.groups()
            relation = state.segment_chords.get(segment)
            if relation is None:
                raise ValueError('Midpoint alias requires a segment chord')
            key = f'@chord:{relation.line}:{relation.curve}'
        else:
            named = re.fullmatch(r'MidPoint\(\s*LineSegmentOf\(\s*([A-Za-z]\w*)\s*,\s*([A-Za-z]\w*)\s*\)\s*\)\s*=\s*([A-Za-z]\w*)',text)
            if not named:
                continue
            a,b,point = named.groups()
            endpoints = tuple(sorted((a,b)))
            if a==b or point in endpoints:
                raise ValueError('Midpoint must differ from two distinct chord endpoints')
            matches = [c for c in state.chords.values()
                       if c.pair_id in state.chord_endpoint_names
                       and state.chord_endpoint_names[c.pair_id].points==endpoints]
            if len(matches)!=1:
                raise ValueError('Midpoint alias requires unique named endpoint chord')
            key,pair_id = matches[0].chord_id,matches[0].pair_id
            segment = None
        if state.entities.get(point)!='Point':
            raise ValueError('Midpoint alias requires declared Point')
        old = state.midpoint_aliases.get(key)
        if old and (old.point!=point or old.segment!=segment or old.pair_id!=pair_id or old.endpoints!=endpoints):
            raise ValueError('Conflicting midpoint aliases for one chord')
        sources = (*old.sources,f'f{i}') if old else (f'f{i}',)
        state.midpoint_aliases[key] = ChordMidpointAlias(key,segment,point,sources, pair_id=pair_id,endpoints=endpoints)
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
    if alias.chord_id!=chord.chord_id or state.entities.get(alias.point)!='Point' or not alias.sources:
        raise TransitionError('inapplicable','Mismatched midpoint alias binding')
    if alias.segment is not None:
        relation = state.segment_chords.get(alias.segment)
        if (relation is None or (relation.line,relation.curve)!=(chord.line,chord.curve)
                or alias.pair_id is not None or alias.endpoints is not None):
            raise TransitionError('inapplicable','Mismatched segment midpoint alias')
    else:
        names = state.chord_endpoint_names.get(chord.pair_id)
        if (names is None or alias.pair_id!=chord.pair_id or names.pair_id!=chord.pair_id
                or alias.endpoints!=names.points or len(set(names.points))!=2
                or alias.point in names.points
                or any(state.entities.get(p)!='Point' for p in names.points)):
            raise TransitionError('inapplicable','Mismatched named endpoint midpoint alias')
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
