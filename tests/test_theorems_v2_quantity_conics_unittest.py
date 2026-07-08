import unittest

from src.theorems_v2.quantity_closure import (
    QuantityApplicatorV2,
    QuantityGeometryClosure,
)
from src.theorems_v2.quantity_library import QuantityTheoremLibraryV2
from src.theorems_v2.quantity_raw_adapter import QuantityRawFactAdapter
from src.theorems_v2.quantity_schema import QuantityRef
from src.theorems_v2.goal_checker import GoalCheckerV3, GoalStatus
from src.theorems_v2.schema import ApplicationStatus
from src.theorems_v2.structured_schema import Point2D


class QuantityConicTests(unittest.TestCase):
    def setUp(self):
        self.adapter = QuantityRawFactAdapter()
        self.library = QuantityTheoremLibraryV2()
        self.applicator = QuantityApplicatorV2()

    def apply(self, state, model_id):
        result = self.applicator.apply(
            self.library.get_model(model_id), state
        )
        self.assertEqual(result.status, ApplicationStatus.APPLIED, result)
        return result.state_after

    def test_library_has_72_concrete_models(self):
        self.assertEqual(len(self.library), 80)
        self.assertEqual(len(self.library.get_executable_models()), 72)

    def test_canonical_quantities(self):
        state = self.adapter.adapt(
            "A: Point;B: Point;H: Circle;"
            "Abs(LineSegmentOf(A,B))=5;Radius(H)=3"
        ).state
        self.assertEqual(
            state.value(
                "QuantityValueOf",
                QuantityRef.of("distance", "A", "B"),
            ),
            5,
        )
        self.assertEqual(
            state.value(
                "QuantityValueOf",
                QuantityRef.of("radius", "H"),
            ),
            3,
        )

    def test_ellipse_focal_triangle_area(self):
        adapted = self.adapter.adapt(
            "G: Ellipse;F1: Point;F2: Point;P: Point;"
            "Expression(G)=(x^2/5+y^2/4=1);"
            "LeftFocus(G)=F1;RightFocus(G)=F2;"
            "PointOnCurve(P,G);AngleOf(F1,P,F2)=pi/2;"
            "Area(TriangleOf(F1,P,F2))=4"
        )
        state = adapted.state
        for model_id in (3, 11, 30):
            state = self.apply(state, model_id)
        self.assertIsNotNone(
            state.get("FocalTriangleAreaFormulaOf", "G")
        )

    def test_parabola_focal_chord_chain(self):
        adapted = self.adapter.adapt(
            "G: Parabola;l: Line;F: Point;A: Point;B: Point;"
            "Expression(G)=(y^2=4*x);Focus(G)=F;"
            "PointOnCurve(F,l);Expression(l)=(y=x-1);"
            "Intersection(l,G)={A,B};Inclination(l)=pi/4"
        )
        state = adapted.state
        for model_id in (7, 33, 34, 35, 36):
            state = self.apply(state, model_id)
        self.assertIsNotNone(
            state.get("ParabolaFocalChordLengthOf", "l", "G")
        )
        self.assertIsNotNone(
            state.get("FocalChordAngleLengthOf", "l", "G")
        )

    def test_chord_formula_materializes_endpoint_distance(self):
        adapted = self.adapter.adapt(
            "l: Line;G: Parabola;A: Point;B: Point;F: Point;"
            "Expression(G)=(y^2=4*x);Slope(l)=1;"
            "PointOnCurve(F,l);Focus(G)=F;Intersection(l,G)={A,B}"
        )
        state = adapted.state
        for model_id in (7, 78, 42, 51):
            state = self.apply(state, model_id)
        self.assertIsNotNone(state.value("DistanceFormulaOf", "A", "B"))
        goal = GoalCheckerV3().check(
            state, "Abs(LineSegmentOf(A, B))", "8"
        )
        self.assertEqual(goal.status, GoalStatus.ANSWER_CORRECT)

    def test_midpoint_chord_and_intercept_forms(self):
        adapted = self.adapter.adapt(
            "G: Ellipse;l: Line;A: Point;B: Point;M: Point;"
            "Expression(G)=(x^2/4+y^2=1);"
            "Expression(l)=(x+y=2);Intersection(l,G)={A,B};"
            "MidPoint(LineSegmentOf(A,B))=M;Coordinate(M)=(1,1)"
        )
        state = self.apply(adapted.state, 40)
        state = self.apply(state, 74)
        self.assertIsNotNone(
            state.get("MidpointChordSlopeRelationOf", "l", "G")
        )
        self.assertEqual(
            state.value("LineInterceptsOf", "l"),
            (2, 2),
        )

    def test_geometric_dot_product(self):
        adapted = self.adapter.adapt(
            "P: Point;A: Point;B: Point;"
            "DotProduct(VectorOf(P,A),VectorOf(P,B))=2;"
            "AngleOf(A,P,B)=pi/3"
        )
        state = self.apply(adapted.state, 60)
        self.assertIsNotNone(
            state.get(
                "GeometricDotProductOf",
                ("P", "A"),
                ("P", "B"),
            )
        )

    def test_directrix_circle_tangent_chain(self):
        adapted = self.adapter.adapt(
            "G: Parabola;H: Circle;"
            "Expression(G)=(y^2=4*x);"
            "Expression(H)=((x-3)^2+y^2=16);"
            "IsTangent(H,Directrix(G))"
        )
        state = adapted.state
        for model_id in (7, 29, 75, 76):
            state = self.apply(state, model_id)
        self.assertIsNotNone(
            state.get("CircleTangentConditionOf", "H", "Directrix(G)")
        )

    def test_tangent_point_projection(self):
        adapted = self.adapter.adapt(
            "H: Circle;l: Line;P: Point;"
            "Expression(H)=(x^2+y^2=1);Expression(l)=(x=1);"
            "TangentPoint(l,H)=P"
        )
        state = self.apply(adapted.state, 75)
        state = QuantityGeometryClosure().enrich(state)
        self.assertEqual(
            state.value("PointPositionOf", "P"),
            Point2D(1, 0),
        )


if __name__ == "__main__":
    unittest.main()
