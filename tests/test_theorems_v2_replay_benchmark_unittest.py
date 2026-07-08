import unittest

from src.theorems_v2.replay_benchmark import ReplayBenchmarkV3


class ReplayBenchmarkTests(unittest.TestCase):
    def setUp(self):
        self.benchmark = ReplayBenchmarkV3()

    def test_successful_replay_reaches_correct_goal(self):
        row = {
            "id": "ellipse",
            "fact_expressions": (
                "G: Ellipse;"
                "Expression(G)=(x^2/4+y^2/3=1)"
            ),
            "query_expressions": "Eccentricity(G)",
            "answer_expressions": "1/2",
            "process": "由标准方程求离心率",
            "models_v3_observed": [3, 11, 13],
        }
        result = self.benchmark.evaluate_row(row)
        self.assertTrue(result["sequence_success"])
        self.assertEqual(result["goal"]["status"], "ANSWER_CORRECT")
        self.assertTrue(result["selector_usable"])
        self.assertEqual(len(result["trajectory"]), 3)
        self.assertIn(
            3,
            result["trajectory"][0]["applicable_model_ids"],
        )

    def test_initially_correct_goal_is_not_selector_progress(self):
        row = {
            "id": "already_solved",
            "fact_expressions": (
                "G: Ellipse;Expression(G)=(x^2/4+y^2/3=1);"
                "Eccentricity(G)=1/2"
            ),
            "query_expressions": "Eccentricity(G)",
            "answer_expressions": "1/2",
            "process": "答案已经在题面给出",
            "models_v3_observed": [3],
        }
        result = self.benchmark.evaluate_row(row)
        self.assertTrue(result["sequence_success"])
        self.assertEqual(result["initial_goal"]["status"], "ANSWER_CORRECT")
        self.assertEqual(result["goal"]["status"], "ANSWER_CORRECT")
        self.assertFalse(result["goal_progress"])
        self.assertFalse(result["selector_usable"])

    def test_failure_reports_first_missing_step(self):
        row = {
            "id": "wrong",
            "fact_expressions": (
                "G: Ellipse;"
                "Expression(G)=(x^2/4+y^2/3=1)"
            ),
            "query_expressions": "Eccentricity(G)",
            "answer_expressions": "1/2",
            "process": "错误序列",
            "models_v3_observed": [5, 13],
        }
        result = self.benchmark.evaluate_row(row)
        self.assertFalse(result["sequence_success"])
        self.assertEqual(
            result["first_failure"]["model_id"],
            5,
        )
        self.assertEqual(
            result["first_failure"]["status"],
            "NO_MATCH",
        )
        self.assertNotIn("trajectory", result)

    def test_assisted_apply_expands_abstract_parameter_step(self):
        benchmark = ReplayBenchmarkV3(assisted_apply=True)
        row = {
            "id": "macro-ellipse-parameter",
            "fact_expressions": (
                "G: Ellipse;"
                "Expression(G)=(x^2/4+y^2/3=1)"
            ),
            "query_expressions": "Eccentricity(G)",
            "answer_expressions": "1/2",
            "process": "由椭圆参数关系和离心率公式可得答案",
            "models_v3_observed": [11, 13],
        }
        result = benchmark.evaluate_row(row)
        self.assertTrue(result["sequence_success"])
        self.assertEqual(result["goal"]["status"], "ANSWER_CORRECT")
        self.assertEqual(result["support_model_ids"][0], [3])
        self.assertEqual(
            result["trajectory"][0]["support_applications"][0]["model_id"],
            3,
        )

    def test_assisted_apply_rolls_back_unhelpful_support(self):
        benchmark = ReplayBenchmarkV3(assisted_apply=True)
        row = {
            "id": "macro-rollback",
            "fact_expressions": (
                "G: Ellipse;"
                "Expression(G)=(x^2/4+y^2/3=1)"
            ),
            "query_expressions": "Eccentricity(G)",
            "answer_expressions": "1/2",
            "process": "错误地使用双曲线标准式",
            "models_v3_observed": [5],
        }
        result = benchmark.evaluate_row(row)
        self.assertFalse(result["sequence_success"])
        self.assertEqual(result["support_model_ids"], [[]])
        self.assertEqual(result["first_failure"]["status"], "NO_MATCH")

    def test_assisted_definition_materializes_derived_directrix(self):
        benchmark = ReplayBenchmarkV3(assisted_apply=True)
        row = {
            "id": "macro-parabola-definition",
            "fact_expressions": (
                "G: Parabola;P: Point;F: Point;"
                "Expression(G)=(y^2=4*x);Focus(G)=F;"
                "PointOnCurve(P,G)"
            ),
            "query_expressions": "Expression(Directrix(G))",
            "answer_expressions": "x=-1",
            "process": "由抛物线定义及准线公式可得",
            "models_v3_observed": [7, 2, 29],
        }
        result = benchmark.evaluate_row(row)
        self.assertTrue(result["sequence_success"])
        self.assertEqual(result["support_model_ids"][1], [29])
        self.assertEqual(result["goal"]["status"], "ANSWER_CORRECT")


if __name__ == "__main__":
    unittest.main()
