"""RM53 bound point-pair proposal; no line identity or coordinate recovery."""
from src.solver.transition_primitives import TransitionError
from src.solver.point_pair_operations import point_pair_distance
from src.state.point_pair_distance import PointPairDistanceQuery,pair_inputs,pair_snapshot,read_pair_distance


def check_point_pair_binding(state, action):
    if (action.mode!='derive_point_distance' or action.points is None or any(v is not None for v in (
        action.curve,action.equation_id,action.line_equation_id,action.relation_id,action.peer_curve,
        action.peer_equation_id,action.point,action.coordinate_id,action.line,action.point_role,
        action.incidence_id,action.slope_sum_id))):
        raise TransitionError('inapplicable','Only point-pair binding supported')
    coords,reads,digest=pair_inputs(state,action.points)
    if action.coordinate_ids!=tuple(c.fact_id for c in coords) or action.coordinate_snapshot!=digest:
        raise TransitionError('inapplicable','Stale point-pair binding')
    return coords,reads


def derive_point_distance(state,action):
    from .bound_application import Proposal
    coords,reads=check_point_pair_binding(state,action)
    query=PointPairDistanceQuery(action.points);key=(query.owner,'distance')
    value,delta,squared=point_pair_distance(*(c.xy for c in coords))
    if key in state.properties:
        if state.properties[key]!=value:raise TransitionError('conflict','Conflicting point distance')
        if read_pair_distance(state,query) is None:
            raise TransitionError('inapplicable','Existing point distance evidence missing or stale')
    return Proposal(properties={key:value},point_pair_snapshots={key:pair_snapshot(state,action.points,value)},
                    read_facts=reads,operations=[{'operation':'point_pair_distance','points':action.points,
                    'coordinates':tuple(c.xy for c in coords),'delta':delta,'squared_distance':squared,'distance':value}])
