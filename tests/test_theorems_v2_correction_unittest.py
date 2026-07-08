import unittest
from fractions import Fraction

from src.theorems_v2.assistant import (
    AuxiliaryReasoner,
    ConstraintClosure,
    GoalEvaluator,
)
from src.theorems_v2.catalog import THEOREM_CATALOG
from src.theorems_v2.complete_library import (
    CompleteTheoremLibraryV2,
    SupportLevel,
)
from src.theorems_v2.correction import IssueKind, SequenceCorrector
from src.theorems_v2.expressions import equation
from src.theorems_v2.raw_adapter import RawFactAdapter
from src.theorems_v2.schema import Term
from src.theorems_v2.state import InformationState


class CompleteCatalogTests(unittest.TestCase):
    def test_all_80_models_have_v2_requirements(self):
        library = CompleteTheoremLibraryV2()
        self.assertEqual(len(THEOREM_CATALOG), 80)
        self.assertEqual(len(library), 80)
        self.assertEqual(library.get_available_models(), list(range(80)))
        self.assertEqual(library.specification_coverage(), 1.0)
        self.assertEqual(
            library.get_capability(47).support_level,
            SupportLevel.SPECIFICATION_ONLY,
        )
        self.assertEqual(
            library.get_capability(21).support_level,
            SupportLevel.CONCRETE,
        )


class CorrectionTests(unittest.TestCase):
    def setUp(self):
        self.adapter = RawFactAdapter()
        self.corrector = SequenceCorrector()

    def test_raw_numeric_hyperbola_chain_replays(self):
        adapted = self.adapter.adapt(
            "G: Hyperbola;Expression(G) = (x^2/9 - y^2/16 = 1)",
            "Expression(Asymptote(G))",
        )
        result = self.corrector.repair([5, 21], adapted.state)
        self.assertEqual(result.repaired_sequence, (5, 21))
        self.assertEqual([step.status for step in result.trace], ["APPLIED", "APPLIED"])
        self.assertTrue(GoalEvaluator.all_satisfied(result.state_after))

    def test_directional_parabola_label_is_replaced_from_state_evidence(self):
        adapted = self.adapter.adapt(
            "G: Parabola;Expression(G) = (x^2 = -2*y)"
        )
        result = self.corrector.repair([7, 29], adapted.state)
        self.assertEqual(result.repaired_sequence, (10, 29))
        self.assertTrue(
            any(issue.kind == IssueKind.DIRECTION_MISMATCH for issue in result.issues)
        )

    def test_parameter_dependency_is_inserted_before_eccentricity(self):
        adapted = self.adapter.adapt(
            "G: Ellipse;Expression(G) = (x^2/9 + y^2/5 = 1)"
        )
        result = self.corrector.repair([3, 13], adapted.state)
        self.assertEqual(result.repaired_sequence, (3, 11, 13))
        self.assertEqual(
            result.state_after.value("ParameterOf", "G", "eccentricity"),
            Fraction(2, 3),
        )

    def test_directrix_is_reordered_before_parabola_definition(self):
        adapted = self.adapter.adapt(
            "G: Parabola;P: Point;Expression(G) = (y^2 = 4*x);"
            "PointOnCurve(P,G)"
        )
        result = self.corrector.repair([7, 2, 29], adapted.state)
        self.assertEqual(result.repaired_sequence[:3], (7, 29, 2))
        self.assertTrue(
            any(issue.kind == IssueKind.DEPENDENCY_REORDERED for issue in result.issues)
        )
        self.assertEqual(result.trace[-1].status, "NO_MATCH")

    def test_axis_pair_is_reported_as_branch(self):
        adapted = self.adapter.adapt(
            "G: Ellipse;Expression(G) = (x^2/5 + y^2/3 = 1)"
        )
        result = self.corrector.repair([3, 4], adapted.state)
        self.assertEqual(result.branches, ((3,), (4,)))
        self.assertTrue(
            any(issue.kind == IssueKind.BRANCH_REQUIRED for issue in result.issues)
        )

    def test_specification_only_is_not_reported_as_no_match(self):
        state = InformationState().declare("T", "Triangle")
        result = self.corrector.repair([47], state)
        self.assertEqual(result.trace[0].status, "SPECIFICATION_ONLY")
        self.assertEqual(result.issues[0].kind, IssueKind.SPECIFICATION_ONLY)

    def test_unparsed_facts_are_preserved(self):
        adapted = self.adapter.adapt("G: Hyperbola;Negation(A=B)")
        self.assertEqual(adapted.unparsed_facts, ("Negation(A=B)",))
        self.assertEqual(
            adapted.state.value("UnparsedFact", 0), "Negation(A=B)"
        )


class AssistantTests(unittest.TestCase):
    def test_auxiliary_reasoner_closes_high_frequency_chain(self):
        state = RawFactAdapter().adapt(
            "G: Ellipse;Expression(G) = (x^2/9 + y^2/5 = 1)"
        ).state
        result = AuxiliaryReasoner().saturate(state)
        self.assertTrue(result.reached_fixed_point)
        self.assertEqual(
            result.state.value("ParameterOf", "G", "eccentricity"),
            Fraction(2, 3),
        )

    def test_linear_constraint_closure_solves_scoped_parameter(self):
        state = InformationState().declare("G", "Ellipse")
        target = Term("parameter", ("G", "unknown"))
        state.add_given("EquationConstraint", equation(target, 5))
        result = ConstraintClosure().close(state)
        self.assertEqual(
            result.state.value("ParameterOf", "G", "unknown"), Fraction(5)
        )

    def test_goal_evaluator_requires_explicit_goal_fact(self):
        state = InformationState().declare("G", "Ellipse")
        GoalEvaluator.add_goal(state, "ParameterOf", "G", "eccentricity")
        self.assertFalse(GoalEvaluator.all_satisfied(state))
        state.add_given("ParameterOf", "G", "eccentricity", value=Fraction(1, 2))
        self.assertTrue(GoalEvaluator.all_satisfied(state))


if __name__ == "__main__":
    unittest.main()
