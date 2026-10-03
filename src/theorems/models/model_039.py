"""RM39: v0*v=s*p*(u+u0) for v²=2*s*p*u; bound interface only."""
from ..base_model import TheoremModel


class ParabolaTangentLine(TheoremModel):
    def __init__(self):
        super().__init__(39, 'Parabola_Tangent_Line', '抛物线切线方程')

    def can_apply(self, state):
        return False  # Legacy unbound execution is not implemented.

    def apply(self, state):
        return False

    def propose_bound(self, state, action):
        from ..tangent_proposals import derive_parabola_tangent
        return derive_parabola_tangent(state, action)
