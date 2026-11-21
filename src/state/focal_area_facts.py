"""Vertex-preserving angle identities and read-only focal-area queries."""
from dataclasses import dataclass
import re
import sympy as sp
from src.solver.transition_primitives import parse_expression

@dataclass(frozen=True)
class AngleFact:
    vertex: str
    endpoints: tuple[str,str]
    value: sp.Expr
    sources: tuple[str,...]

@dataclass(frozen=True)
class FocalAreaQuery:
    points: tuple[str,str,str]

def area_owner(pair,point):
    return 'area:'+':'.join((pair.curve,*pair.points,point))

def collect_angles(state,parts):
    consumed=set()
    for i,text in enumerate(parts):
        m=re.fullmatch(r'AngleOf\(\s*(\w+)\s*,\s*(\w+)\s*,\s*(\w+)\s*\)\s*=\s*(.+)',text)
        if not m:continue
        left,vertex,right,expr=m.groups();ends=tuple(sorted((left,right)))
        if len({left,vertex,right})!=3 or any(state.entities.get(p)!='Point' for p in (left,vertex,right)):
            raise ValueError('Angle requires three distinct declared points')
        value=parse_expression(expr,{**state.symbols,"pi":sp.pi})[0]
        if value.free_symbols or value.is_real is not True or value.is_finite is not True:
            raise ValueError('Only finite numeric radians supported')
        key=(vertex,ends);old=state.angle_facts.get(key)
        if old and sp.simplify(old.value-value)!=0:raise ValueError('Conflicting angle values')
        state.angle_facts[key]=AngleFact(vertex,ends,value,(*(old.sources if old else ()),f'f{i}'));consumed.add(i)
    return consumed

def read_area(state,query):
    owners=[]
    for pair in state.focus_pairs.values():
        rest=set(query.points)-set(pair.points)
        if set(pair.points)<=set(query.points) and len(rest)==1:
            point=next(iter(rest))
            if any(i.point==point and i.curve==pair.curve for i in state.incidences.values()):owners.append(area_owner(pair,point))
    return state.properties.get((owners[0],'area')) if len(owners)==1 else None
