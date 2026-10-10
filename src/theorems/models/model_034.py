"""Numeric bound focal-chord product; legacy execution is unsupported."""
from ..base_model import TheoremModel


class ParabolaFocalChordAxialProduct(TheoremModel):
    def __init__(self):
        super().__init__(34, 'Parabola_Focal_Chord_Product_X', '抛物线焦点弦轴向积')

    def can_apply(self, state):
        return False

    def apply(self, state):
        return False

    def propose_bound(self, state, action):
        from ..focal_chord_proposals import derive_coordinate_product
        return derive_coordinate_product(state, action)
