"""Unordered ellipse focus identities and read-only perimeter targets."""
from dataclasses import dataclass
import re

@dataclass(frozen=True)
class FocusPair:
    curve: str
    points: tuple[str,str]
    sources: tuple[str,...]

@dataclass(frozen=True)
class FocalPerimeterQuery:
    points: tuple[str,str,str]


def perimeter_owner(pair,point):
    return 'perimeter:'+':'.join((pair.curve,*pair.points,point))


def collect_focus_pairs(state,parts):
    consumed=set()
    for i,text in enumerate(parts):
        m=re.fullmatch(r'Focus\(\s*(\w+)\s*\)\s*=\s*\{\s*(\w+)\s*,\s*(\w+)\s*\}',text)
        if not m:continue
        curve,a,b=m.groups();points=tuple(sorted((a,b)))
        if state.entities.get(curve)!='Ellipse' or a==b or any(state.entities.get(p)!='Point' for p in points):
            raise ValueError('Focus pair requires ellipse and distinct declared points')
        old=state.focus_pairs.get(curve)
        if old and old.points!=points:raise ValueError('Ambiguous focus pair')
        state.focus_pairs[curve]=FocusPair(curve,points,(*(old.sources if old else ()),f'f{i}'))
        consumed.add(i)
    return consumed


def read_perimeter(state,query):
    matches=[]
    for pair in state.focus_pairs.values():
        rest=set(query.points)-set(pair.points)
        if set(pair.points)<=set(query.points) and len(rest)==1:
            point=next(iter(rest))
            if any(i.point==point and i.curve==pair.curve for i in state.incidences.values()):
                matches.append(perimeter_owner(pair,point))
    return state.properties.get((matches[0],'perimeter')) if len(matches)==1 else None
