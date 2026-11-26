"""Finite bound RM28; no legacy mutation path."""
from ..base_model import TheoremModel


class HyperbolaDirectrix(TheoremModel):
    def __init__(self):
        super().__init__(28, 'Hyperbola_Directrix', '双曲线准线')

    def can_apply(self, state):
        return False

    def apply(self, state):
        return False

    def propose_bound(self, state, action):
        from ..directrix_pair_proposals import derive_directrix_pair
        return derive_directrix_pair(state, action)
