"""RM50 chord length from committed root relations; bound interface only."""
from ..base_model import TheoremModel


class ChordLengthFormula(TheoremModel):
    def __init__(self):
        super().__init__(50, 'Chord_Length_Formula', '弦长公式')

    def can_apply(self, state):
        return False

    def apply(self, state):
        return False

    def propose_bound(self, state, action):
        from ..intersection_proposals import derive_chord_length
        return derive_chord_length(state, action)
