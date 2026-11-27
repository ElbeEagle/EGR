"""Numeric bound two-point line; legacy mutation is unsupported."""
from ..base_model import TheoremModel


class LineTwoPointForm(TheoremModel):
    def __init__(self):
        super().__init__(73, 'Line_Two_Point_Form', '两点式直线')

    def can_apply(self, state):
        return False

    def apply(self, state):
        return False

    def propose_bound(self, state, action):
        from ..two_point_line_proposals import derive_two_point_line
        return derive_two_point_line(state, action)
