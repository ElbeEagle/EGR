"""Numeric bound parabola latus rectum; legacy execution is unsupported."""
from ..base_model import TheoremModel


class ParabolaLatusRectum(TheoremModel):
    def __init__(self):
        super().__init__(20, 'Parabola_Latus_Rectum', '抛物线通径')

    def can_apply(self, state):
        return False

    def apply(self, state):
        return False

    def propose_bound(self, state, action):
        from ..latus_proposals import derive_latus
        return derive_latus(state, action)
