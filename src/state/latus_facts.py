"""Given focal-segment and perpendicular-axis evidence; no geometry calculation."""
from dataclasses import dataclass
import re

@dataclass(frozen=True)
class SegmentLengthQuery:
    segment: str

@dataclass(frozen=True)
class LatusEvidence:
    segment: str
    kind: str
    target: str
    source: str


def collect_latus_facts(state,parts):
    consumed=set()
    for i,text in enumerate(parts):
        focus=re.fullmatch(r'PointOnCurve\(\s*Focus\(\s*(\w+)\s*\)\s*,\s*(\w+)\s*\)(?:\s*=\s*True)?',text)
        perpendicular=re.fullmatch(r'IsPerpendicular\(\s*(\w+)\s*,\s*(xAxis|yAxis|SymmetryAxis\(\s*\w+\s*\))\s*\)(?:\s*=\s*True)?',text)
        if focus and state.entities.get(focus[2])=='LineSegment':
            target,segment=focus.groups();kind='focus'
        elif perpendicular:
            segment,target=perpendicular.groups();kind='perpendicular';target=re.sub(r'\s+','',target)
        else:continue
        chord=state.segment_chords.get(segment)
        if chord is None:raise ValueError('Latus evidence requires declared segment chord')
        if kind=='focus' and target!=chord.curve:raise ValueError('Focus belongs to another curve')
        if target.startswith('SymmetryAxis(') and target!=f'SymmetryAxis({chord.curve})':raise ValueError('Axis belongs to another curve')
        key=f'f{i}';state.latus_evidence[key]=LatusEvidence(segment,kind,target,key);consumed.add(i)
    return consumed
