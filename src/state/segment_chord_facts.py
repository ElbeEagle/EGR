"""Limited declared-segment ellipse/hyperbola chords; no midpoint aliases or endpoint solving."""
from dataclasses import dataclass
import re
from .chord_facts import ChordIdentity, AnonymousEndpointPair, store_chord_midpoint


@dataclass(frozen=True)
class SegmentChord:
    segment: str
    line: str
    curve: str
    sources: tuple[str, ...]


def collect_segment_chords(state, parts):
    """Resolve IsChordOf then its numeric midpoint, independent of fact order."""
    consumed = set()
    name = r'([A-Za-z]\w*)'
    for i, text in enumerate(parts):
        match = re.fullmatch(rf'IsChordOf\(\s*{name}\s*,\s*{name}\s*\)(?:\s*=\s*True)?', text)
        if not match:
            continue
        segment,curve = match.groups()
        if state.entities.get(segment)!='LineSegment' or state.entities.get(curve) not in ('Ellipse','Hyperbola'):
            raise ValueError('Segment chord requires declared LineSegment and Ellipse/Hyperbola')
        old = state.segment_chords.get(segment)
        if old and old.curve!=curve:
            raise ValueError('Ambiguous segment chord curve')
        line = f'@overlap:{segment}'
        sources = (*old.sources,f'f{i}') if old else (f'f{i}',)
        state.segment_chords[segment] = SegmentChord(segment,line,curve,sources)
        state.entities[line] = 'Line'
        state.provenance[f'entity:{line}'] = sources
        key = f'@chord:{line}:{curve}'
        pair = f'{key}:endpoints'
        state.chords[key] = ChordIdentity(key,line,curve,pair,sources)
        state.chord_endpoint_pairs[pair] = AnonymousEndpointPair(pair,key,sources)
        state.provenance[key] = state.provenance[pair] = sources
        consumed.add(i)
    for i, text in enumerate(parts):
        match = re.fullmatch(rf'Coordinate\(\s*MidPoint\(\s*{name}\s*\)\s*\)\s*=\s*\(([^,]+),([^,]+)\)', text)
        if not match:
            continue
        segment,xt,yt = match.groups()
        relation = state.segment_chords.get(segment)
        if relation is None:
            raise ValueError('Segment midpoint requires explicit chord relation')
        store_chord_midpoint(state,relation.line,relation.curve,xt,yt,f'f{i}')
        consumed.add(i)
    return consumed
