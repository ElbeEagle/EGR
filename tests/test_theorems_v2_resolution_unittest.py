import unittest

from src.theorems_v2.applicator import ApplicatorV2
from src.theorems_v2.expanded_library import ExpandedTheoremLibraryV2
from src.theorems_v2.expanded_raw_adapter import ExpandedRawFactAdapter
from src.theorems_v2.goal_checker import GoalCheckerV3, GoalStatus
from src.theorems_v2.models.common import parameter_fact
from src.theorems_v2.schema import (
    ApplicationStatus,
    Fact,
    Provenance,
    StateDelta,
    Term,
)
from src.theorems_v2.state import InformationState


class StateResolutionTests(unittest.TestCase):
    def test_assignment_is_symbol_value_and_resolves_parameter_chain(self):
        adapted = ExpandedRawFactAdapter().adapt(
            "G: Ellipse;a: Number;b: Number;a>b;b>0;"
            "Expression(G)=(x^2/a^2+y^2/b^2=1);a=4;b=3"
        )
        state = adapted.state
        self.assertEqual(state.value("SymbolValueOf", "a"), 4)
        self.assertIsNone(state.value("ParameterOf", "G", "semi_axis_a"))

        result = ApplicatorV2().apply(
            ExpandedTheoremLibraryV2().get_model(3), state
        )
        self.assertEqual(result.status, ApplicationStatus.APPLIED)
        resolved = parameter_fact(
            result.state_after, "G", "semi_axis_a"
        )
        self.assertEqual(resolved.value, 4)
        goal = GoalCheckerV3().check(
            result.state_after, "Length(MajorAxis(G))", "8"
        )
        self.assertEqual(goal.status, GoalStatus.ANSWER_CORRECT)

    def test_axis_length_and_focal_length_resolve_standard_equation(self):
        adapted = ExpandedRawFactAdapter().adapt(
            "G: Ellipse;a: Number;b: Number;a>b;b>0;"
            "Expression(G)=(x^2/a^2+y^2/b^2=1);"
            "Length(MajorAxis(G))=4;FocalLength(G)=2"
        )
        state = adapted.state
        for model_id in (3, 11):
            result = ApplicatorV2().apply(
                ExpandedTheoremLibraryV2().get_model(model_id), state
            )
            self.assertEqual(result.status, ApplicationStatus.APPLIED)
            state = result.state_after
        self.assertEqual(
            state.value("ResolvedParameterOf", "G", "semi_axis_b_squared"),
            3,
        )
        goal = GoalCheckerV3().check(
            state, "Expression(G)", "x^2/4+y^2/3=1"
        )
        self.assertEqual(goal.status, GoalStatus.ANSWER_CORRECT)

    def test_commit_accepts_values_equal_after_explicit_substitution(self):
        state = InformationState().declare("G", "Ellipse")
        state.declare("a", "Number")
        state.add_given("SymbolValueOf", "a", value=4)
        state.add_given(
            "ParameterOf",
            "G",
            "semi_axis_a",
            value=Term("symbol", ("a",)),
        )
        derived = Fact(
            "ParameterOf",
            ("G", "semi_axis_a"),
            value=4,
            provenance=Provenance.theorem(3),
        )
        commit = state.commit_delta(StateDelta(add_facts=(derived,)))
        self.assertEqual(commit.conflicts, ())
        self.assertEqual(commit.added_count, 0)

    def test_eccentricity_formula_keeps_given_value_and_adds_constraint(self):
        state = InformationState().declare("G", "Ellipse")
        state.add_given("ParameterOf", "G", "semi_axis_a", value=2)
        state.add_given("ParameterOf", "G", "focal_half_distance", value=1)
        state.add_given("ParameterOf", "G", "eccentricity", value=1 / 2)
        result = ApplicatorV2().apply(
            ExpandedTheoremLibraryV2().get_model(13), state
        )
        self.assertEqual(result.status, ApplicationStatus.APPLIED)
        self.assertEqual(
            result.state_after.value("ParameterOf", "G", "eccentricity"),
            1 / 2,
        )
        self.assertTrue(result.state_after.find("EquationConstraint"))


if __name__ == "__main__":
    unittest.main()