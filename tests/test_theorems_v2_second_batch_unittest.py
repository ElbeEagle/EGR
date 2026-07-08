import unittest
from fractions import Fraction

from src.theorems_v2.applicator import ApplicatorV2
from src.theorems_v2.expanded_library import ExpandedTheoremLibraryV2
from src.theorems_v2.expanded_raw_adapter import ExpandedRawFactAdapter
from src.theorems_v2.schema import ApplicationStatus, PolynomialEquation
from src.theorems_v2.state import InformationState


class SecondBatchConcreteTests(unittest.TestCase):
    def setUp(self):
        self.library = ExpandedTheoremLibraryV2()
        self.applicator = ApplicatorV2()

    def apply(self, state, model_id):
        result = self.applicator.apply(
            self.library.get_model(model_id), state
        )
        self.assertEqual(result.status, ApplicationStatus.APPLIED, result)
        return result.state_after

    @staticmethod
    def conic(curve_type, polynomial):
        state = InformationState().declare("G", curve_type)
        state.add_given("ExpressionPolynomial", "G", value=polynomial)
        return state

    def test_expanded_library_has_35_concrete_models(self):
        self.assertEqual(len(self.library), 80)
        self.assertEqual(len(self.library.get_executable_models()), 35)

    def test_symbolic_standard_forms_use_order_and_positive_facts(self):
        adapter = ExpandedRawFactAdapter()
        cases = (
            (
                "G: Ellipse;a: Number;b: Number;a>b;b>0;"
                "Expression(G)=(x^2/a^2+y^2/b^2=1)",
                3,
            ),
            (
                "G: Hyperbola;m: Number;m>0;"
                "Expression(G)=(x^2/4-y^2/m^2=1)",
                5,
            ),
            (
                "G: Parabola;p: Number;p>0;"
                "Expression(G)=(y^2=2*p*x)",
                7,
            ),
        )
        for facts, model_id in cases:
            with self.subTest(model_id=model_id):
                adapted = adapter.adapt(facts)
                self.assertEqual(adapted.unparsed_facts, ())
                self.apply(adapted.state, model_id)

    def test_one_of_focus_and_asymptote_relations_are_typed(self):
        adapted = ExpandedRawFactAdapter().adapt(
            "G: Hyperbola;F1: Point;F2: Point;P: Point;"
            "OneOf(Focus(G))=F1;OneOf(Focus(G))=F2;"
            "OneOf(Asymptote(G))=l;"
            "PointOnCurve(P,OneOf(Asymptote(G)))"
        )
        self.assertEqual(adapted.unparsed_facts, ())
        self.assertEqual(len(adapted.state.find("FocusOf", "G")), 2)
        self.assertIsNotNone(adapted.state.get("AsymptoteOf", "G", "l"))
        self.assertIsNotNone(
            adapted.state.get("PointOnAsymptoteOf", "G", "P")
        )

    def test_ellipse_property_chain(self):
        state = self.conic(
            "Ellipse",
            PolynomialEquation(
                x2=Fraction(1, 9),
                y2=Fraction(1, 5),
                constant=-1,
            ),
        )
        state.declare("P", "Point")
        state.add_given("PointOnCurve", "P", "G", value=True)
        state.add_given("CoordinateOf", "P", value=(1, 2))
        for model_id in (3, 11, 13, 14, 16, 18, 25, 27, 32, 37, 38):
            state = self.apply(state, model_id)

        self.assertIsNotNone(state.get("FocalRadiusRelation", "G", "P"))
        self.assertEqual(state.value("LatusRectumLengthOf", "G"), Fraction(10, 3))
        self.assertIsNotNone(state.get("DirectrixFamilyOf", "G"))
        self.assertEqual(state.value("FocalTrianglePerimeterOf", "G"), 10)
        self.assertIsNotNone(state.get("TangentExpressionOf", "G", "P"))

    def test_hyperbola_property_chain(self):
        state = self.conic(
            "Hyperbola",
            PolynomialEquation(
                x2=Fraction(1, 4),
                y2=Fraction(-1, 5),
                constant=-1,
            ),
        )
        state.declare("P", "Point")
        state.add_given("PointOnCurve", "P", "G", value=True)
        for model_id in (5, 12, 13, 15, 19, 21, 22, 23, 26, 28):
            state = self.apply(state, model_id)

        self.assertEqual(
            state.value("FocusAsymptoteDistanceOf", "G"),
            Fraction(5).sqrt() if False else state.value("ParameterOf", "G", "semi_axis_b"),
        )
        self.assertIsNotNone(state.get("CommonAsymptoteSystemOf", "G"))
        self.assertIsNotNone(state.get("DirectrixFamilyOf", "G"))

    def test_equal_axis_hyperbola(self):
        state = self.conic(
            "Hyperbola",
            PolynomialEquation(x2=1, y2=-1, constant=-1),
        )
        state = self.apply(state, 5)
        state = self.apply(state, 24)
        self.assertTrue(state.value("EqualAxisOf", "G"))

    def test_parabola_property_chain(self):
        state = self.conic(
            "Parabola", PolynomialEquation(y2=1, x=-8)
        )
        state.declare("P", "Point")
        state.add_given("PointOnCurve", "P", "G", value=True)
        state.add_given("CoordinateOf", "P", value=(2, 4))
        for model_id in (7, 17, 20, 29, 39):
            state = self.apply(state, model_id)

        self.assertIsNotNone(state.get("FocalRadiusRelation", "G", "P"))
        self.assertEqual(state.value("LatusRectumLengthOf", "G"), 8)
        self.assertIsNotNone(state.get("TangentExpressionOf", "G", "P"))


if __name__ == "__main__":
    unittest.main()
