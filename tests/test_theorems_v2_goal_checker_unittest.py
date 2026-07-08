import unittest
from fractions import Fraction

from src.theorems_v2.expressions import add, equation, sqrt_positive
from src.theorems_v2.goal_checker import GoalCheckerV3, GoalStatus
from src.theorems_v2.schema import (
    AxisLine,
    LineThroughOrigin,
    StandardConicForm,
    Term,
)
from src.theorems_v2.state import InformationState
from src.theorems_v2.structured_schema import Point2D


class GoalCheckerTests(unittest.TestCase):
    def setUp(self):
        self.checker = GoalCheckerV3()

    def test_equivalent_radical_forms_are_correct(self):
        state = InformationState().declare("G", "Ellipse")
        state.add_given(
            "ParameterOf",
            "G",
            "eccentricity",
            value=sqrt_positive(Fraction(1, 3)),
        )
        result = self.checker.check(
            state,
            "Eccentricity(G)",
            "sqrt(3)/3",
        )
        self.assertEqual(result.status, GoalStatus.ANSWER_CORRECT)

    def test_parabola_focus_directrix_distance(self):
        state = InformationState().declare("G", "Parabola")
        state.add_given("ParameterOf", "G", "p", value=2)
        result = self.checker.check(
            state, "Distance(Focus(G), Directrix(G))", "2"
        )
        self.assertEqual(result.status, GoalStatus.ANSWER_CORRECT)

    def test_focus_asymptote_distance(self):
        state = InformationState().declare("G", "Hyperbola")
        state.add_given("FocusAsymptoteDistanceOf", "G", value=3)
        result = self.checker.check(
            state, "Distance(Focus(G), Asymptote(G))", "3"
        )
        self.assertEqual(result.status, GoalStatus.ANSWER_CORRECT)

    def test_focal_triangle_perimeter(self):
        state = InformationState().declare("G", "Ellipse")
        for point in ("P", "F1", "F2"):
            state.declare(point, "Point")
        state.add_given("FocusOf", "G", "F1", value=True)
        state.add_given("FocusOf", "G", "F2", value=True)
        state.add_given("PointOnCurve", "P", "G", value=True)
        state.add_given("FocalTrianglePerimeterOf", "G", value=16)
        result = self.checker.check(
            state, "Perimeter(TriangleOf(P,F1,F2))", "16"
        )
        self.assertEqual(result.status, GoalStatus.ANSWER_CORRECT)

    def test_ellipse_definition_distance_sum(self):
        state = InformationState().declare("G", "Ellipse")
        state.add_given("FocusOf", "G", "F1", value=True)
        state.add_given("FocusOf", "G", "F2", value=True)
        relation = equation(
            add(
                Term("distance", ("P", "F1")),
                Term("distance", ("P", "F2")),
            ),
            8,
        )
        state.add_given("DefinitionRelation", "G", "P", value=relation)
        result = self.checker.check(
            state, "Distance(P,F1)+Distance(P,F2)", "8"
        )
        self.assertEqual(result.status, GoalStatus.ANSWER_CORRECT)

    def test_hyperbola_definition_does_not_answer_distance_sum(self):
        state = InformationState().declare("G", "Hyperbola")
        state.add_given("FocusOf", "G", "F1", value=True)
        state.add_given("FocusOf", "G", "F2", value=True)
        relation = equation(Term("distance_difference", ("P", "F1", "F2")), 2)
        state.add_given("DefinitionRelation", "G", "P", value=relation)
        result = self.checker.check(
            state, "Distance(P,F1)+Distance(P,F2)", "2"
        )
        self.assertEqual(result.status, GoalStatus.GOAL_NOT_REACHED)

    def test_asymptote_family_equation(self):
        state = InformationState().declare("G", "Hyperbola")
        state.add_given(
            "AsymptoteFamilyOf",
            "G",
            value=(
                LineThroughOrigin("y", Fraction(4, 3)),
                LineThroughOrigin("y", Fraction(-4, 3)),
            ),
        )
        result = self.checker.check(
            state, "Expression(Asymptote(G))", "y=pm*(4/3)*x"
        )
        self.assertEqual(result.status, GoalStatus.ANSWER_CORRECT)

    def test_directrix_axis_equation(self):
        state = InformationState().declare("G", "Parabola")
        state.add_given(
            "DirectrixExpressionOf",
            "G",
            value=AxisLine("y", Fraction(1, 16)),
        )
        result = self.checker.check(
            state, "Expression(Directrix(G))", "y=1/16"
        )
        self.assertEqual(result.status, GoalStatus.ANSWER_CORRECT)

    def test_standard_equation_accepts_equivalent_scaled_form(self):
        state = InformationState().declare("G", "Ellipse")
        state.add_given(
            "ConicStandardForm",
            "G",
            value=StandardConicForm(
                "ellipse", "horizontal", a2=4, b2=3
            ),
        )
        result = self.checker.check(
            state, "Expression(G)", "3*x^2+4*y^2=12"
        )
        self.assertEqual(result.status, GoalStatus.ANSWER_CORRECT)

    def test_symbolic_standard_equation_remains_unresolved(self):
        state = InformationState().declare("G", "Ellipse")
        state.add_given(
            "ConicStandardForm",
            "G",
            value=StandardConicForm(
                "ellipse",
                "horizontal",
                a2=Term("symbol", ("a2",)),
                b2=3,
            ),
        )
        result = self.checker.check(
            state, "Expression(G)", "x^2/4+y^2/3=1"
        )
        self.assertEqual(result.status, GoalStatus.VALUE_UNRESOLVED)

    def test_axis_length(self):
        state = InformationState().declare("G", "Ellipse")
        state.add_given(
            "ParameterOf", "G", "semi_axis_a", value=3
        )
        result = self.checker.check(
            state,
            "Length(MajorAxis(G))",
            "6",
        )
        self.assertEqual(result.status, GoalStatus.ANSWER_CORRECT)

    def test_coordinate(self):
        state = InformationState().declare("P", "Point")
        state.add_given(
            "PointPositionOf", "P", value=Point2D(1, 2)
        )
        result = self.checker.check(
            state,
            "Coordinate(P)",
            "(1,2)",
        )
        self.assertEqual(result.status, GoalStatus.ANSWER_CORRECT)

    def test_reached_but_wrong_answer(self):
        state = InformationState().declare("G", "Hyperbola")
        state.add_given(
            "ParameterOf", "G", "eccentricity", value=2
        )
        result = self.checker.check(
            state,
            "Eccentricity(G)",
            "3",
        )
        self.assertEqual(result.status, GoalStatus.ANSWER_INCORRECT)

    def test_declared_numeric_symbol_does_not_alias_conic_parameter(self):
        state = InformationState().declare("G", "Ellipse")
        state.declare("a", "Real")
        state.add_given("ParameterOf", "G", "semi_axis_a", value=5)
        result = self.checker.check(state, "a", "-1/3")
        self.assertEqual(result.status, GoalStatus.GOAL_NOT_REACHED)

    def test_explicit_parameter_alias_resolves_simple_parameter(self):
        state = InformationState().declare("G", "Ellipse")
        state.declare("e", "Real")
        state.add_given("ParameterAlias", "e", value=("G", "eccentricity"))
        state.add_given("ParameterOf", "G", "eccentricity", value=Fraction(1, 2))
        result = self.checker.check(state, "e", "1/2")
        self.assertEqual(result.status, GoalStatus.ANSWER_CORRECT)

    def test_unsupported_query_is_not_failure(self):
        state = InformationState()
        result = self.checker.check(
            state,
            "LocusEquation(P)",
            "x^2+y^2=1",
        )
        self.assertEqual(result.status, GoalStatus.GOAL_UNSUPPORTED)


if __name__ == "__main__":
    unittest.main()
