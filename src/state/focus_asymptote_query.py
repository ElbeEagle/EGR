"""Same-hyperbola common distance target; not a general set distance."""
from dataclasses import dataclass

@dataclass(frozen=True)
class FocusAsymptoteDistanceQuery:
    curve: str

def read_focus_asymptote_distance(state,query):
    equations=[f for f in state.equations.values() if f.owner==query.curve and f.role=='curve']
    key=f'property:{query.curve}:focus_asymptote_distance'
    if len(equations)!=1 or equations[0].fact_id not in state.provenance.get(key,()):return None
    return state.properties.get((query.curve,'focus_asymptote_distance'))
