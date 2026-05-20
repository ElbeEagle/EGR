import os
import sys

import sympy as sp

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.solver import SymbolicSolver
from src.state.symbolic_state import SymbolicState


def test_expression_assignment_handles_nested_target():
    solver = SymbolicSolver()
    target, expression = solver.parse_expression_assignment(
        "Expression(OneOf(Asymptote(G))) = (x + sqrt(3)*y = 0)"
    )
    assert target == "OneOf(Asymptote(G))"
    assert expression == "x + sqrt(3)*y = 0"


def test_centered_hyperbola_model_and_asymptote():
    solver = SymbolicSolver()
    state = SymbolicState(
        entities={"G": "Hyperbola"},
        equations=["Expression(G) = (x^2/9 - y^2/4 = 1)"],
    )
    model = solver.curve_models(state)["G"]
    assert solver.format_centered_conic(model.x_denom, model.y_denom, "Hyperbola") == "x^2/9-y^2/4=1"
    assert solver.conic_asymptote(model) == "y=pm*2/3*x"


def test_centered_ellipse_eccentricity():
    solver = SymbolicSolver()
    state = SymbolicState(
        entities={"H": "Ellipse"},
        equations=["Expression(H) = (x^2 + 4*y^2 = 16)"],
    )
    model = solver.curve_models(state)["H"]
    assert solver.conic_eccentricity(model) == "sqrt(3)/2"


def test_parabola_focus_and_directrix_distance():
    solver = SymbolicSolver()
    state = SymbolicState(
        entities={"G": "Parabola"},
        equations=["Expression(G) = (y^2 = 4*x)"],
    )
    assert solver.solve_coordinate(state, "Focus(G)") == "(1, 0)"
    assert solver.solve_distance(state, "Distance(Focus(G), Directrix(G))") == "2"


def test_range_for_ellipse_denominators_excludes_circle_case():
    solver = SymbolicSolver()
    state = SymbolicState(
        entities={"G": "Ellipse", "a": "Number"},
        equations=["Expression(G) = (x^2/(2 - a) + y^2/(a - 1) = 1)"],
    )
    assert solver.solve_range(state, "a") == "(1, 3/2)+(3/2, 2)"


def test_range_for_hyperbola_denominators():
    solver = SymbolicSolver()
    state = SymbolicState(
        entities={"H": "Curve", "k": "Number"},
        equations=["Expression(H) = (x^2/(k + 4) + y^2/(1 - k) = 1)"],
    )
    assert solver.solve_range(state, "k") == "(-oo, -4)+(1, +oo)"


def test_line_slope_from_implicit_line():
    solver = SymbolicSolver()
    assert sp.simplify(solver.line_slope("x + sqrt(3)*y = 0") - sp.sqrt(3) / 3) == 0


def test_distance_between_coordinates():
    solver = SymbolicSolver()
    state = SymbolicState(coordinates={"A": ("0", "0"), "B": ("3", "4")})
    assert solver.solve_distance(state, "Distance(A, B)") == "5"


def test_parabola_chord_slope_from_midpoint():
    solver = SymbolicSolver()
    state = SymbolicState(
        entities={"G": "Parabola", "A": "Point", "B": "Point", "P": "Point"},
        equations=["Expression(G) = (y^2 = 4*x)"],
        coordinates={"P": ("1", "1")},
        geometric_relations=[
            "IsChordOf(LineSegmentOf(A, B), G) = True",
            "MidPoint(LineSegmentOf(A, B)) = P",
        ],
    )
    assert solver.solve_slope(state, "Slope(OverlappingLine(LineSegmentOf(A, B)))") == "2"


def test_parabola_chord_length_from_line_intersection():
    solver = SymbolicSolver()
    state = SymbolicState(
        entities={"l": "Line", "C": "Parabola", "A": "Point", "B": "Point"},
        equations=[
            "Expression(C) = (y^2 = 4*x)",
            "Expression(l) = (y = x - 1)",
        ],
        geometric_relations=["Intersection(l, C) = {A, B}"],
    )
    assert solver.solve_line_segment(state, "LineSegmentOf(A, B)") == "8"


def test_parabola_focus_distance_from_x_coordinate():
    solver = SymbolicSolver()
    state = SymbolicState(
        entities={"G": "Parabola", "P": "Point", "F": "Point"},
        equations=["Expression(G) = (y^2 = 8*x)"],
        geometric_relations=[
            "Focus(G) = F",
            "PointOnCurve(P, G)",
            "XCoordinate(P)=4",
        ],
    )
    assert solver.solve_line_segment(state, "LineSegmentOf(P, F)") == "6"


def test_parabola_focus_distance_from_axis_distance():
    solver = SymbolicSolver()
    state = SymbolicState(
        entities={"G": "Parabola", "P": "Point", "F": "Point"},
        equations=["Expression(G) = (y^2 = 16*x)"],
        geometric_relations=[
            "Focus(G)=F",
            "PointOnCurve(P, G)",
            "Distance(P, xAxis) = 12",
        ],
    )
    assert solver.solve_line_segment(state, "LineSegmentOf(P, F)") == "13"


def test_parabola_min_point_focus_sum_uses_directrix_distance():
    solver = SymbolicSolver()
    state = SymbolicState(
        entities={"G": "Parabola", "P": "Point", "A": "Point", "F": "Point"},
        equations=["Expression(G) = (x^2 = 8*y)"],
        coordinates={"A": ("-2", "4")},
        geometric_relations=["PointOnCurve(P, G)", "Focus(G) = F"],
    )
    assert solver.solve_optimization(
        state,
        "Min(Abs(LineSegmentOf(P, A)) + Abs(LineSegmentOf(P, F)))",
    ) == "6"
