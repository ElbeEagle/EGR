"""RM45 numeric ellipse midpoint chord, bound execution only."""
from ..base_model import TheoremModel


class EllipsePointDifference(TheoremModel):
    def __init__(self):
        super().__init__(45,'Point_Difference_Method_Ellipse','椭圆点差法')

    def can_apply(self, state):
        return False

    def apply(self, state):
        return False

    def propose_bound(self, state, action):
        from ..midpoint_proposals import derive_point_difference_chord
        return derive_point_difference_chord(state,action)
