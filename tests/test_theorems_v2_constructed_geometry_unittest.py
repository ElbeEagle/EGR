import unittest

from src.theorems_v2.geometry_closure import (
    GeometryApplicatorV2,
    GeometryClosure,
)
from src.theorems_v2.geometry_library import GeometryTheoremLibraryV2
from src.theorems_v2.geometry_raw_adapter import GeometryRawFactAdapter
from src.theorems_v2.schema import ApplicationStatus, Term
from src.theorems_v2.structured_schema import LineEquation, Point2D


class ConstructedGeometryTests(unittest.TestCase):
    def setUp(self):
        self.adapter = GeometryRawFactAdapter()
        self.library = GeometryTheoremLibraryV2()
        self.applicator = GeometryApplicatorV2()

    def apply(self, state, model_id):
        result = self.applicator.apply(
            self.library.get_model(model_id), state
        )
        self.assertEqual(result.status, ApplicationStatus.APPLIED, result)
        return result.state_after

    def test_library_has_62_concrete_models(self):
        self.assertEqual(len(self.library), 80)
        self.assertEqual(len(self.library.get_executable_models()), 62)

    def test_focus_vertex_and_origin_coordinate_closure(self):
        adapted = self.adapter.adapt(
            "G: Ellipse;F1: Point;F2: Point;A: Point;O: Origin;"
            "Expression(G)=(x^2/9+y^2/4=1);"
            "LeftFocus(G)=F1;RightFocus(G)=F2;RightVertex(G)=A"
        )
        state = adapted.state
        for model_id in (3, 11):
            state = self.apply(state, model_id)

        left = state.value("PointPositionOf", "F1")
        right = state.value("PointPositionOf", "F2")
        self.assertEqual(left.x, Term("mul", (-1, Term("sqrt_positive", (5,)))))
        self.assertEqual(right.x, Term("sqrt_positive", (5,)))
        self.assertEqual(state.value("PointPositionOf", "A"), Point2D(3, 0))
        self.assertEqual(state.value("PointPositionOf", "O"), Point2D(0, 0))

    def test_named_center_without_curve_form_has_no_assumed_coordinate(self):
        adapted = self.adapter.adapt("C: Circle;C1: Point;Center(C)=C1")
        state = GeometryClosure().enrich(adapted.state)
        self.assertIsNone(state.value("PointPositionOf", "C1"))

    def test_nested_line_and_line_intersection_closure(self):
        adapted = self.adapter.adapt(
            "A: Point;B: Point;P: Point;h: Line;"
            "Coordinate(A)=(0,0);Coordinate(B)=(2,2);"
            "Expression(h)=(x=1);"
            "Intersection(LineOf(A,B),h)=P"
        )
        state = GeometryClosure().enrich(adapted.state)
        self.assertTrue(state.has_type("LineOf(A,B)", "Line"))
        self.assertEqual(
            state.value("PointPositionOf", "P"),
            Point2D(1, 1),
        )

    def test_line_normal_form_from_one_known_point_and_slope(self):
        adapted = self.adapter.adapt(
            "P: Point;l: Line;Coordinate(P)=(1,2);"
            "PointOnCurve(P,l);Slope(l)=3"
        )
        state = GeometryClosure().enrich(adapted.state)
        self.assertEqual(
            state.value("LineNormalFormOf", "l"),
            LineEquation(3, -1, -1),
        )

    def test_point_difference_chain(self):
        adapted = self.adapter.adapt(
            "G: Ellipse;l: Line;A: Point;B: Point;"
            "Expression(G)=(x^2/9+y^2/4=1);"
            "Expression(l)=(y=x+1);Intersection(l,G)={A,B}"
        )
        state = adapted.state
        state = self.apply(state, 44)
        state = self.apply(state, 45)
        self.assertIsNotNone(
            state.get("PointDifferenceRelationOf", "l", "G")
        )
        self.assertIsNotNone(
            state.get("EllipsePointDifferenceRelationOf", "l", "G")
        )

    def test_substitution_to_chord_length_chain(self):
        adapted = self.adapter.adapt(
            "G: Parabola;l: Line;A: Point;B: Point;"
            "Expression(G)=(y^2=4*x);Expression(l)=(y=x);"
            "Intersection(l,G)={A,B}"
        )
        state = adapted.state
        for model_id in (78, 42, 43, 51):
            state = self.apply(state, model_id)
        self.assertIsNotNone(
            state.get("ChordLengthWithKFormulaOf", "l", "G")
        )

    def test_triangle_laws_and_area_chain(self):
        adapted = self.adapter.adapt(
            "A: Point;B: Point;C: Point;"
            "Coordinate(A)=(0,0);Coordinate(B)=(3,0);"
            "Coordinate(C)=(0,4);AngleOf(B,A,C)=pi/2;"
            "Area(TriangleOf(A,B,C))=6"
        )
        state = adapted.state
        for model_id in (47, 49, 56, 57, 58):
            state = self.apply(state, model_id)
        self.assertEqual(
            state.value("CoordinateAreaFormulaOf", ("A", "B", "C")),
            6,
        )


if __name__ == "__main__":
    unittest.main()
