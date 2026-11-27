"""Unordered point-pair target and read-only distance evidence."""
from dataclasses import dataclass
import hashlib
import sympy as sp
from src.solver.transition_primitives import TransitionError


@dataclass(frozen=True)
class PointPairDistanceQuery:
    points: tuple[str, str]

    def __post_init__(self):
        object.__setattr__(self, 'points', tuple(sorted(self.points)))

    @property
    def owner(self):
        return 'point_pair:' + ':'.join(self.points)


@dataclass(frozen=True)
class PointPairDistanceSnapshot:
    points: tuple[str, str]
    coordinate_ids: tuple[str, str]
    digest: str
    value: sp.Expr


def pair_inputs(state, points):
    if len(points) != 2 or tuple(sorted(points)) != points:
        raise TransitionError('inapplicable', 'Canonical point pair required')
    coordinates=[];reads=[]
    for point in points:
        c=state.coordinates.get(point)
        if state.entities.get(point)!='Point' or c is None or c.point!=point:
            raise TransitionError('inapplicable', 'Declared point coordinates required')
        if not state.provenance.get(c.fact_id):
            raise TransitionError('inapplicable', 'Coordinate source required')
        if any(v.free_symbols or v.is_real is not True or v.is_finite is not True for v in c.xy):
            raise TransitionError('undetermined', 'Finite numeric coordinates required')
        coordinates.append(c);reads.extend((f'entity:{point}',c.fact_id))
    payload=(points,tuple(map(repr,coordinates)),tuple((k,state.provenance.get(k)) for k in reads))
    digest=hashlib.sha256(repr(payload).encode()).hexdigest()
    return tuple(coordinates),tuple(dict.fromkeys(reads)),digest


def pair_snapshot(state, points, value):
    coords,_,digest=pair_inputs(state,points)
    return PointPairDistanceSnapshot(points,tuple(c.fact_id for c in coords),digest,value)


def read_pair_distance(state, query):
    key=(query.owner,'distance');value=state.properties.get(key);evidence=state.point_pair_snapshots.get(key)
    if value is None or evidence is None:return None
    try:
        _,reads,_=pair_inputs(state,query.points)
        if evidence!=pair_snapshot(state,query.points,value):return None
        sources=state.provenance.get(f'property:{key[0]}:{key[1]}',())
        if any(k not in sources for k in reads):return None
    except TransitionError:
        return None
    return value
