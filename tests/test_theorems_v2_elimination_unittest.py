import unittest
from fractions import Fraction

from src.theorems_v2.elimination import ExactEliminationClosure
from src.theorems_v2.expressions import add, equation, mul, square
from src.theorems_v2.quantity_closure import QuantityGeometryClosure
from src.theorems_v2.replay_benchmark import ReplayBenchmarkV3
from src.theorems_v2.schema import Term
from src.theorems_v2.state import InformationState


class ExactEliminationTests(unittest.TestCase):
    def setUp(self):
        self.closure = ExactEliminationClosure()

    def test_solves_two_symbol_linear_system(self):
        x = Term("symbol", ("x",))
        y = Term("symbol", ("y",))
        state = InformationState().declare("x", "Real").declare("y", "Real")
        state.add_given("EquationConstraint", equation(add(x, y), 5))
        state.add_given("EquationConstraint", equation(add(x, mul(-1, y)), 1))
        result = self.closure.close(state)
        self.assertEqual(result.state.value("SymbolValueOf", "x"), 3)
        self.assertEqual(result.state.value("SymbolValueOf", "y"), 2)
        self.assertEqual(len(result.steps), 2)

    def test_solves_scoped_parameter_without_overwriting_expression(self):
        a2 = Term("parameter", ("G", "semi_axis_a_squared"))
        b2 = Term("parameter", ("G", "semi_axis_b_squared"))
        c2 = Term("parameter", ("G", "focal_half_distance_squared"))
        state = InformationState().declare("G", "Ellipse")
        state.add_given("ParameterOf", "G", "semi_axis_a_squared", value=9)
        state.add_given(
            "ParameterOf",
            "G",
            "semi_axis_b_squared",
            value=Term("symbol", ("b2",)),
        )
        state.add_given("ParameterOf", "G", "focal_half_distance_squared", value=4)
        state.add_given("EquationConstraint", equation(a2, add(b2, c2)))
        result = self.closure.close(state)
        self.assertEqual(
            result.state.value(
                "ResolvedParameterOf", "G", "semi_axis_b_squared"
            ),
            5,
        )
        self.assertIsInstance(
            result.state.value("ParameterOf", "G", "semi_axis_b_squared"),
            Term,
        )

    def test_quantity_closure_runs_elimination(self):
        x = Term("symbol", ("x",))
        state = InformationState().declare("x", "Real")
        state.add_given("EquationConstraint", equation(x, 7))
        enriched = QuantityGeometryClosure().enrich(state)
        self.assertEqual(enriched.value("SymbolValueOf", "x"), 7)

    def test_asymptote_and_focal_length_eliminate_axis_parameters(self):
        row = {
            "id": "axis_elimination",
            "fact_expressions": (
                "G: Hyperbola;a: Number;b: Number;a>0;b>0;"
                "Expression(G)=(-y^2/b^2+x^2/a^2=1);"
                "Slope(OneOf(Asymptote(G)))=3/4;FocalLength(G)=10"
            ),
            "query_expressions": "Expression(G)",
            "answer_expressions": "x^2/16-y^2/9=1",
            "process": "由渐近线和焦距消元",
            "models_v3_executable": [5, 21, 12],
        }
        result = ReplayBenchmarkV3().evaluate_row(
            row, "models_v3_executable", True
        )
        self.assertTrue(result["sequence_success"])
        self.assertEqual(result["goal"]["status"], "ANSWER_CORRECT")
        closure_predicates = {
            fact["predicate"]
            for step in result["trajectory"]
            for fact in step["closure_delta"]
        }
        self.assertIn("ResolvedParameterOf", closure_predicates)

    def test_axis_ratio_resolves_eccentricity_without_scale(self):
        row = {
            "id": "ratio_elimination",
            "fact_expressions": (
                "G: Hyperbola;a: Number;b: Number;a>0;b>0;"
                "Expression(G)=(-y^2/b^2+x^2/a^2=1);"
                "Expression(Asymptote(G))=(y=pm*sqrt(3)*x)"
            ),
            "query_expressions": "Eccentricity(G)",
            "answer_expressions": "2",
            "process": "由渐近线斜率求离心率",
            "models_v3_executable": [5, 21, 12, 13],
        }
        result = ReplayBenchmarkV3().evaluate_row(
            row, "models_v3_executable", False
        )
        self.assertEqual(result["goal"]["status"], "ANSWER_CORRECT")

    def test_focus_directrix_distance_resolves_parabola_scale(self):
        row = {
            "id": "parabola_scale",
            "fact_expressions": (
                "G: Parabola;p: Number;p>0;"
                "Expression(G)=(y^2=2*p*x);"
                "Distance(Focus(G),Directrix(G))=1"
            ),
            "query_expressions": "Expression(G)",
            "answer_expressions": "y^2=2*x",
            "process": "由焦点到准线距离求参数",
            "models_v3_executable": [7, 29],
        }
        result = ReplayBenchmarkV3().evaluate_row(
            row, "models_v3_executable", False
        )
        self.assertEqual(result["goal"]["status"], "ANSWER_CORRECT")

    def test_focus_pair_distance_resolves_hyperbola_scale(self):
        row = {
            "id": 579,
            "fact_expressions": (
                "G: Hyperbola;a: Number;a>0;F1:Point;F2:Point;"
                "Focus(G)={F1,F2};"
                "Expression(G)=(-y^2+x^2/a^2=1);Distance(F1,F2)=4"
            ),
            "query_expressions": "Expression(Asymptote(G))",
            "answer_expressions": "y=sqrt(3)*x/3",
            "process": "focus separation and parameter relation",
            "models_v3_executable": [5, 12, 21],
        }
        result = ReplayBenchmarkV3().evaluate_row(
            row, "models_v3_executable", False
        )
        self.assertEqual(result["unparsed_fact_count"], 0)
        self.assertEqual(result["goal"]["status"], "ANSWER_CORRECT")

    def test_axis_length_ratio_resolves_hyperbola_parameters(self):
        row = {
            "id": 1651,
            "fact_expressions": (
                "G: Hyperbola;a: Number;b: Number;a>0;b>0;"
                "Expression(G)=(-y^2/b^2+x^2/a^2=1);"
                "FocalLength(G)=2*sqrt(5);"
                "2*Length(ImageinaryAxis(G))=Length(RealAxis(G))"
            ),
            "query_expressions": "Expression(G)",
            "answer_expressions": "x^2/4-y^2=1",
            "process": "focal length and axis ratio",
            "models_v3_executable": [5, 12],
        }
        result = ReplayBenchmarkV3().evaluate_row(
            row, "models_v3_executable", False
        )
        self.assertEqual(result["unparsed_fact_count"], 0)
        self.assertEqual(result["goal"]["status"], "ANSWER_CORRECT")

    def test_point_on_asymptote_resolves_eccentricity(self):
        row = {
            "id": 2109,
            "fact_expressions": (
                "C: Hyperbola;a: Number;b: Number;P: Point;"
                "Expression(C)=(-y^2/b^2+x^2/a^2=1);"
                "Coordinate(P)=(2,1);PointOnCurve(P,Asymptote(C))"
            ),
            "query_expressions": "Eccentricity(C)",
            "answer_expressions": "sqrt(5)/2",
            "process": "point coordinates determine asymptote slope",
            "models_v3_executable": [5, 21, 13],
        }
        result = ReplayBenchmarkV3().evaluate_row(
            row, "models_v3_executable", False
        )
        self.assertEqual(result["unparsed_fact_count"], 0)
        self.assertEqual(result["goal"]["status"], "ANSWER_CORRECT")

    def test_point_on_asymptote_and_focal_length_resolve_scale(self):
        row = {
            "id": 4553,
            "fact_expressions": (
                "C: Hyperbola;a: Number;b: Number;P: Point;"
                "Expression(C)=(-x^2/b^2+y^2/a^2=1);"
                "FocalLength(C)=10*sqrt(5);Coordinate(P)=(1,2);"
                "PointOnCurve(P,Asymptote(C))"
            ),
            "query_expressions": "Expression(C)",
            "answer_expressions": "y^2/100-x^2/25=1",
            "process": "asymptote point and focal length determine scale",
            "models_v3_executable": [6, 12, 21],
        }
        result = ReplayBenchmarkV3().evaluate_row(
            row, "models_v3_executable", False
        )
        self.assertEqual(result["goal"]["status"], "ANSWER_CORRECT")

    def test_implicit_square_positivity_does_not_ambiguous_multi_conic(self):
        row = {
            "id": 2305,
            "fact_expressions": (
                "C1: Hyperbola;Expression(C1)=(x^2/a^2-y^2/b^2=1);"
                "a: Number;b: Number;C2: Hyperbola;"
                "Expression(C2)=(x^2/4-y^2/16=1)"
            ),
            "query_expressions": "a;b",
            "answer_expressions": "1\n2",
            "process": "multi-conic binding remains conservative",
            "models_v3_executable": [5, 21, 12],
        }
        result = ReplayBenchmarkV3().evaluate_row(
            row, "models_v3_executable", False
        )
        self.assertTrue(result["sequence_success"])

    def test_underdetermined_system_stays_unresolved(self):
        x = Term("symbol", ("x",))
        y = Term("symbol", ("y",))
        state = InformationState()
        state.add_given("EquationConstraint", equation(add(x, y), 5))
        result = self.closure.close(state)
        self.assertIsNone(result.state.value("SymbolValueOf", "x"))
        self.assertIsNone(result.state.value("SymbolValueOf", "y"))
        self.assertEqual(result.steps, ())

    def test_rejects_solution_that_violates_positive_fact(self):
        x = Term("symbol", ("x",))
        state = InformationState().declare("x", "Real")
        state.add_given("Positive", x, value=True)
        state.add_given("EquationConstraint", equation(x, -1))
        result = self.closure.close(state)
        self.assertIsNone(result.state.value("SymbolValueOf", "x"))

    def test_positive_fact_selects_unique_quadratic_root(self):
        x = Term("symbol", ("x",))
        state = InformationState().declare("x", "Real")
        state.add_given("Positive", x, value=True)
        state.add_given("EquationConstraint", equation(square(x), 9))
        result = self.closure.close(state)
        self.assertEqual(result.state.value("SymbolValueOf", "x"), 3)

    def test_quadratic_with_two_roots_stays_unresolved(self):
        x = Term("symbol", ("x",))
        state = InformationState().declare("x", "Real")
        state.add_given("EquationConstraint", equation(square(x), 9))
        result = self.closure.close(state)
        self.assertIsNone(result.state.value("SymbolValueOf", "x"))

    def test_positive_irrational_root_stays_exact(self):
        x = Term("symbol", ("x",))
        state = InformationState().declare("x", "Real")
        state.add_given("Positive", x, value=True)
        state.add_given("EquationConstraint", equation(square(x), 2))
        result = self.closure.close(state)
        value = result.state.value("SymbolValueOf", "x")
        self.assertIsInstance(value, Term)
        self.assertEqual(value.operator, "sqrt_positive")

    def test_reports_constant_contradiction(self):
        state = InformationState()
        fact = state.add_given("EquationConstraint", equation(1, 2))
        result = self.closure.close(state)
        self.assertEqual(result.inconsistent_constraints, (fact.fact_id,))


if __name__ == "__main__":
    unittest.main()