import unittest
from fractions import Fraction

from src.theorems_v2.applicator import ApplicatorV2
from src.theorems_v2.schema import ApplicationStatus
from src.theorems_v2.structured_library import StructuredTheoremLibraryV2
from src.theorems_v2.structured_raw_adapter import StructuredRawFactAdapter
from src.theorems_v2.structured_schema import (
    LineEquation,
    Point2D,
    QuadraticPolynomial,
)


class StructuredInformationSpaceTests(unittest.TestCase):
    def setUp(self):
        self.adapter = StructuredRawFactAdapter()
        self.library = StructuredTheoremLibraryV2()
        self.applicator = ApplicatorV2()

    def apply(self, state, model_id):
        result = self.applicator.apply(
            self.library.get_model(model_id), state
        )
        self.assertEqual(result.status, ApplicationStatus.APPLIED, result)
        return result.state_after

    def test_library_has_51_concrete_models(self):
        self.assertEqual(len(self.library), 80)
        self.assertEqual(len(self.library.get_executable_models()), 51)

    def test_substitution_vieta_and_discriminant_chain(self):
        adapted = self.adapter.adapt(
            "l: Line;G: Parabola;A: Point;B: Point;"
            "Expression(l) = (y = x);Expression(G) = (y^2 = 4*x);"
            "Intersection(l, G) = {A, B};NumIntersection(l, G)=2"
        )
        state = adapted.state
        for model_id in (78, 42, 43, 65, 67):
            state = self.apply(state, model_id)

        quadratic = state.value("QuadraticPolynomialOf", "l", "G")
        self.assertIsInstance(quadratic, QuadraticPolynomial)
        self.assertEqual(quadratic.variable, "x")
        self.assertEqual(quadratic.a, 1)
        self.assertEqual(quadratic.b, -4)
        self.assertEqual(state.value("RootSumOf", "l", "G"), 4)
        self.assertEqual(state.value("RootProductOf", "l", "G"), 0)
        self.assertEqual(state.value("DiscriminantOf", "l", "G"), 16)

    def test_tangent_discriminant_chain(self):
        adapted = self.adapter.adapt(
            "l: Line;G: Parabola;A: Point;"
            "Expression(l) = (y = x + 1);"
            "Expression(G) = (y^2 = 4*x);"
            "Intersection(l, G) = A;NumIntersection(l, G)=1"
        )
        state = adapted.state
        for model_id in (78, 65, 66):
            state = self.apply(state, model_id)
        self.assertEqual(state.value("DiscriminantOf", "l", "G"), 0)

    def test_coordinate_formula_chain(self):
        adapted = self.adapter.adapt(
            "A: Point;B: Point;M: Point;"
            "Coordinate(A) = (0, 0);Coordinate(B) = (3, 4);"
            "Abs(LineSegmentOf(A,B))=5;"
            "Slope(LineSegmentOf(A,B))=4/3;"
            "MidPoint(LineSegmentOf(A,B))=M"
        )
        state = adapted.state
        for model_id in (53, 54, 55):
            state = self.apply(state, model_id)

        self.assertEqual(state.value("DistanceFormulaOf", "A", "B"), 5)
        self.assertEqual(
            state.value("PointPositionOf", "M"),
            Point2D(Fraction(3, 2), 2),
        )
        self.assertEqual(
            state.value("SlopeFormulaOf", "A", "B"),
            Fraction(4, 3),
        )

    def test_point_line_distance(self):
        adapted = self.adapter.adapt(
            "P: Point;l: Line;Coordinate(P)=(1,2);"
            "Expression(l)=(3*x+4*y-5=0);Distance(P,l)=6/5"
        )
        state = self.apply(adapted.state, 52)
        normal = state.value("LineNormalFormOf", "l")
        self.assertIsInstance(normal, LineEquation)
        self.assertEqual(
            state.value("DistanceFormulaOf", "P", "l"),
            Fraction(6, 5),
        )

    def test_vector_chain(self):
        adapted = self.adapter.adapt(
            "A: Point;B: Point;C: Point;D: Point;"
            "Coordinate(A)=(0,0);Coordinate(B)=(1,0);"
            "Coordinate(C)=(0,1);Coordinate(D)=(1,1);"
            "DotProduct(VectorOf(A,B),VectorOf(A,C))=0;"
            "VectorOf(A,B)=1*VectorOf(C,D)"
        )
        state = adapted.state
        for model_id in (59, 61, 62):
            state = self.apply(state, model_id)

        self.assertEqual(
            state.value("DotProductFormulaOf", ("A", "B"), ("A", "C")),
            0,
        )
        self.assertTrue(
            state.value(
                "CollinearVectorPair",
                ("A", "B"),
                ("C", "D"),
            )
        )

    def test_line_forms(self):
        point_slope = self.adapter.adapt(
            "l: Line;P: Point;Coordinate(P)=(2,3);"
            "PointOnCurve(P,l);Slope(l)=4"
        )
        state = self.apply(point_slope.state, 72)
        self.assertEqual(
            state.value("LinePointSlopeFormOf", "l"),
            LineEquation(-4, 1, 5),
        )

        two_point = self.adapter.adapt(
            "h: Line;A: Point;B: Point;"
            "Coordinate(A)=(0,1);Coordinate(B)=(2,3);"
            "PointOnCurve(A,h);PointOnCurve(B,h)"
        )
        state = self.apply(two_point.state, 73)
        self.assertEqual(
            state.value("LineTwoPointFormOf", "h"),
            LineEquation(-2, 2, -2),
        )


if __name__ == "__main__":
    unittest.main()
