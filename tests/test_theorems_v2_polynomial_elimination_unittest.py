import unittest

from src.theorems_v2.expressions import add, equation, mul, square, sub
from src.theorems_v2.elimination import ExactEliminationClosure
from src.theorems_v2.replay_benchmark import ReplayBenchmarkV3
from src.theorems_v2.schema import Term
from src.theorems_v2.state import InformationState


class PolynomialEliminationTests(unittest.TestCase):
    def setUp(self):
        self.closure = ExactEliminationClosure()

    def test_eliminates_shared_quadratic_monomial(self):
        x = Term("symbol", ("x",))
        y = Term("symbol", ("y",))
        state = InformationState().declare("x", "Number").declare("y", "Number")
        state.add_given("NonNegative", x, value=True)
        state.add_given("EquationConstraint", equation(square(y), mul(8, x)))
        state.add_given(
            "EquationConstraint",
            equation(add(square(sub(x, 2)), square(y)), 9),
        )

        result = self.closure.close(state)
        self.assertEqual(result.state.value("SymbolValueOf", "x"), 1)
        self.assertIsNone(result.state.value("SymbolValueOf", "y"))

    def test_keeps_two_root_target_unresolved_without_sign(self):
        x = Term("symbol", ("x",))
        y = Term("symbol", ("y",))
        state = InformationState().declare("x", "Number").declare("y", "Number")
        state.add_given("EquationConstraint", equation(square(y), mul(8, x)))
        state.add_given(
            "EquationConstraint",
            equation(add(square(sub(x, 2)), square(y)), 9),
        )

        result = self.closure.close(state)
        self.assertIsNone(result.state.value("SymbolValueOf", "x"))
        self.assertIsNone(result.state.value("SymbolValueOf", "y"))

    def test_parabola_distance_resolves_x_coordinate(self):
        row = {
            "id": 7104,
            "fact_expressions": (
                "G: Parabola;P: Point;F: Point;"
                "Expression(G)=(y^2=8*x);Focus(G)=F;"
                "PointOnCurve(P,G);Abs(LineSegmentOf(P,F))=3"
            ),
            "query_expressions": "XCoordinate(P)",
            "answer_expressions": "1",
            "process": "eliminate y squared from parabola and distance",
            "models_v3_executable": [7, 17],
        }
        result = ReplayBenchmarkV3().evaluate_row(
            row, "models_v3_executable", True
        )
        self.assertEqual(result["goal"]["status"], "ANSWER_CORRECT")

    def test_quadrant_selects_negative_coordinate_root(self):
        row = {
            "id": 7571,
            "fact_expressions": (
                "G: Parabola;M: Point;F: Point;"
                "Expression(G)=(y^2=12*x);Focus(G)=F;"
                "PointOnCurve(M,G);Quadrant(M)=4;"
                "Abs(LineSegmentOf(M,F))=7"
            ),
            "query_expressions": "Coordinate(M)",
            "answer_expressions": "(4,-4*sqrt(3))",
            "process": "quadrant selects the negative y branch",
            "models_v3_executable": [7, 17],
        }
        result = ReplayBenchmarkV3().evaluate_row(
            row, "models_v3_executable", True
        )
        self.assertEqual(result["unparsed_fact_count"], 0)
        self.assertEqual(result["goal"]["status"], "ANSWER_CORRECT")


if __name__ == "__main__":
    unittest.main()