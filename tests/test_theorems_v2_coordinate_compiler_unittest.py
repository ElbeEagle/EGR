import unittest
from fractions import Fraction

from src.theorems_v2.expressions import equation
from src.theorems_v2.quantity_closure import QuantityGeometryClosure
from src.theorems_v2.quantity_raw_adapter import QuantityRawFactAdapter
from src.theorems_v2.replay_benchmark import ReplayBenchmarkV3
from src.theorems_v2.schema import Term
from src.theorems_v2.state import InformationState
from src.theorems_v2.structured_schema import Point2D


class CoordinateEquationCompilerTests(unittest.TestCase):
    def setUp(self):
        self.closure = QuantityGeometryClosure()

    @staticmethod
    def _point(state, name, x, y):
        state.declare(name, "Point")
        state.add_given("PointPositionOf", name, value=Point2D(x, y))

    @staticmethod
    def _line(state, name, first, second):
        state.declare(name, "Line")
        state.add_given("EndpointsOf", name, value=(first, second))

    def test_right_angle_real_sample_resolves_standard_equation(self):
        row = {
            "id": 1106,
            "fact_expressions": (
                "C: Hyperbola;b: Number;a: Number;P: Point;F: Point;"
                "O: Origin;a>0;b>0;"
                "Expression(C)=(-y^2/b^2+x^2/a^2=1);"
                "Coordinate(P)=(1,sqrt(3));"
                "PointOnCurve(P,Asymptote(C));RightFocus(C)=F;"
                "AngleOf(F,P,O)=ApplyUnit(90,degree)"
            ),
            "query_expressions": "Expression(C)",
            "answer_expressions": "x^2/4-y^2/12=1",
            "process": "right angle compiles to a focal-parameter equation",
            "models_v3_executable": [5, 21, 12],
        }
        result = ReplayBenchmarkV3().evaluate_row(
            row, "models_v3_executable", True
        )
        self.assertEqual(result["goal"]["status"], "ANSWER_CORRECT")
        compiled = {
            fact["arguments"][1]
            for step in result["trajectory"]
            for fact in step["closure_delta"]
            if fact["predicate"] == "CompiledCoordinateEquation"
        }
        self.assertIn("right_angle", compiled)

    def test_perpendicular_lines_compile_dot_product(self):
        x = Term("symbol", ("x",))
        state = InformationState().declare("x", "Number")
        self._point(state, "A", 0, 0)
        self._point(state, "B", x, 1)
        self._point(state, "C", 0, 0)
        self._point(state, "D", 1, 0)
        self._line(state, "l1", "A", "B")
        self._line(state, "l2", "C", "D")
        state.add_given("PerpendicularOf", "l1", "l2", value=True)

        enriched = self.closure.enrich(state)
        self.assertEqual(enriched.value("SymbolValueOf", "x"), 0)
        self.assertTrue(enriched.find("CompiledCoordinateEquation"))

    def test_parallel_lines_compile_cross_product(self):
        y = Term("symbol", ("y",))
        state = InformationState().declare("y", "Number")
        self._point(state, "A", 0, 0)
        self._point(state, "B", 1, y)
        self._point(state, "C", 0, 0)
        self._point(state, "D", 2, 0)
        self._line(state, "l1", "A", "B")
        self._line(state, "l2", "C", "D")
        state.add_given("ParallelOf", "l1", "l2", value=True)

        enriched = self.closure.enrich(state)
        self.assertEqual(enriched.value("SymbolValueOf", "y"), 0)

    def test_midpoint_compiles_two_coordinate_equations(self):
        x = Term("symbol", ("x",))
        state = InformationState().declare("x", "Number")
        self._point(state, "A", 0, 0)
        self._point(state, "B", 4, 0)
        self._point(state, "M", x, 0)
        state.add_given("MidPointOf", "A", "B", value="M")

        enriched = self.closure.enrich(state)
        self.assertEqual(enriched.value("SymbolValueOf", "x"), 2)

    def test_distance_compiles_positive_quadratic(self):
        x = Term("symbol", ("x",))
        state = InformationState().declare("x", "Number")
        state.add_given("Positive", x, value=True)
        self._point(state, "O", 0, 0)
        self._point(state, "P", x, 0)
        state.add_given("RequestedDistanceOf", "O", "P", value=3)

        enriched = self.closure.enrich(state)
        self.assertEqual(enriched.value("SymbolValueOf", "x"), 3)

    def test_numeric_segment_ratio_compiles_squared_distance_equation(self):
        x = Term("symbol", ("x",))
        state = InformationState().declare("x", "Number")
        state.add_given("Positive", x, value=True)
        self._point(state, "A", 0, 0)
        self._point(state, "B", x, 0)
        self._point(state, "C", 0, 0)
        self._point(state, "D", 2, 0)
        state.add_given(
            "DistanceRatioOf", "A", "B", "C", "D", value=Fraction(3, 2)
        )

        enriched = self.closure.enrich(state)
        self.assertEqual(enriched.value("SymbolValueOf", "x"), 3)

    def test_numeric_segment_ratio_is_parsed_exactly(self):
        adapted = QuantityRawFactAdapter().adapt(
            "A: Point;B: Point;C: Point;D: Point;"
            "2*Abs(LineSegmentOf(A,B))=3*Abs(LineSegmentOf(C,D))"
        )
        self.assertEqual(adapted.unparsed_facts, ())
        self.assertEqual(
            adapted.state.value("DistanceRatioOf", "A", "B", "C", "D"),
            Fraction(3, 2),
        )

    def test_vector_scale_compiles_component_equations(self):
        x = Term("symbol", ("x",))
        state = InformationState().declare("x", "Number")
        self._point(state, "A", 0, 0)
        self._point(state, "B", x, 0)
        self._point(state, "C", 0, 0)
        self._point(state, "D", 2, 0)
        state.add_given(
            "VectorScaleRelation",
            "A",
            "B",
            "C",
            "D",
            value=3,
        )

        enriched = self.closure.enrich(state)
        self.assertEqual(enriched.value("SymbolValueOf", "x"), 6)

    def test_numeric_multi_vector_relation_resolves_eccentricity(self):
        row = {
            "id": "numeric-vector-linear-relation",
            "fact_expressions": (
                "G: Hyperbola;a: Number;b: Number;P: Point;A: Point;"
                "F1: Point;F2: Point;a>0;b>0;"
                "Expression(G)=(-y^2/b^2+x^2/a^2=1);"
                "LeftFocus(G)=F1;RightFocus(G)=F2;LeftVertex(G)=A;"
                "PointOnCurve(P,G);"
                "3*VectorOf(P,A)=2*VectorOf(P,F1)+VectorOf(P,F2)"
            ),
            "query_expressions": "Eccentricity(G)",
            "answer_expressions": "3",
            "process": "展开向量坐标关系可得c=3a",
            "models_v3_observed": [5, 1, 62, 13],
        }
        result = ReplayBenchmarkV3(assisted_apply=True).evaluate_row(row)
        self.assertEqual(result["unparsed_fact_count"], 0)
        self.assertEqual(result["goal"]["status"], "ANSWER_CORRECT")
        self.assertTrue(result["sequence_success"])
        self.assertTrue(result["selector_usable"])

    def test_partial_coordinate_materializes_only_missing_axis(self):
        state = InformationState()
        state.declare("P", "Point")
        state.add_given("XCoordinateOf", "P", value=1)
        self._point(state, "A", 0, 0)
        self._point(state, "B", 2, 2)
        self._line(state, "l", "A", "B")
        state.add_given("PointOnCurve", "P", "l", value=True)

        enriched = self.closure.enrich(state)
        position = enriched.value("PointPositionOf", "P")
        self.assertEqual(position.x, 1)
        self.assertEqual(
            enriched.value("SymbolValueOf", "__coord_P_y"),
            1,
        )

    def test_point_on_line_compiles_determinant(self):
        x = Term("symbol", ("x",))
        state = InformationState().declare("x", "Number")
        self._point(state, "A", 0, 0)
        self._point(state, "B", 2, 2)
        self._point(state, "P", x, 1)
        self._line(state, "l", "A", "B")
        state.add_given("PointOnCurve", "P", "l", value=True)

        enriched = self.closure.enrich(state)
        self.assertEqual(enriched.value("SymbolValueOf", "x"), 1)

    def test_nested_circle_center_on_parabola_resolves_parameter(self):
        row = {
            "id": "nested-center-on-parabola",
            "fact_expressions": (
                "G: Parabola;p: Number;H: Circle;p>0;"
                "Expression(G)=(y^2=2*p*x);"
                "Expression(H)=(x^2+y^2-4*x+8*y+19=0);"
                "PointOnCurve(Center(H),G)"
            ),
            "query_expressions": "Expression(Directrix(G))",
            "answer_expressions": "x=-2",
            "process": "将圆心坐标代入抛物线方程",
            "models_v3_observed": [7, 29, 75],
        }
        result = ReplayBenchmarkV3(assisted_apply=True).evaluate_row(row)
        self.assertEqual(result["goal"]["status"], "ANSWER_CORRECT")
        self.assertEqual(result["unparsed_fact_count"], 0)

    def test_nested_focus_distance_compiles_coordinate_equations(self):
        row = {
            "id": "nested-focus-distance",
            "fact_expressions": (
                "G: Parabola;P: Point;Quadrant(P)=1;"
                "Expression(G)=(y^2=4*x);PointOnCurve(P,G);"
                "Distance(P,Focus(G))=3"
            ),
            "query_expressions": "Coordinate(P)",
            "answer_expressions": "(2,2*sqrt(2))",
            "process": "由抛物线定义和第一象限求点坐标",
            "models_v3_observed": [7, 29, 17],
        }
        result = ReplayBenchmarkV3(assisted_apply=True).evaluate_row(row)
        self.assertEqual(result["goal"]["status"], "ANSWER_CORRECT")
        self.assertEqual(result["unparsed_fact_count"], 0)


if __name__ == "__main__":
    unittest.main()
