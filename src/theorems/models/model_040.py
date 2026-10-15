"""RM40 numeric ellipse midpoint chord, bound execution only."""
from ..base_model import TheoremModel


class EllipseMidpointChord(TheoremModel):
    def __init__(self):
        super().__init__(40,'Ellipse_Midpoint_Chord_Slope','椭圆中点弦方向')

    def can_apply(self, state):
        return False

    def apply(self, state):
        return False

    def propose_bound(self, state, action):
        from ..midpoint_proposals import derive_midpoint_chord
        return derive_midpoint_chord(state,action)
