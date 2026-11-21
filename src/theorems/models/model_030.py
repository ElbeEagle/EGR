"""Numeric bound ellipse focal-triangle area; legacy execution is unsupported."""
from ..base_model import TheoremModel


class EllipseFocalTriangleArea(TheoremModel):
    def __init__(self):
        super().__init__(30, 'Ellipse_Focal_Triangle_Area', '椭圆焦点三角形面积')

    def can_apply(self, state):
        return False

    def apply(self, state):
        return False

    def propose_bound(self, state, action):
        from ..focal_area_proposals import derive_focal_area
        return derive_focal_area(state, action)
