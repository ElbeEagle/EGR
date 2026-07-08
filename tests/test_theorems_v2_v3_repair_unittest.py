import unittest

from src.theorems_v2.v3_repair import V3DryRunRepairer


class V3DryRunRepairTests(unittest.TestCase):
    def setUp(self):
        self.repairer = V3DryRunRepairer()

    @staticmethod
    def row(models, facts, process=""):
        return {
            "id": "test",
            "models": models,
            "fact_expressions": facts,
            "query_expressions": "",
            "process": process,
        }

    def test_replaces_wrong_conic_standard_model(self):
        result = self.repairer.repair_row(
            self.row(
                [5],
                "G: Ellipse;Expression(G)=(x^2/9+y^2/4=1)",
            )
        )
        self.assertEqual(result["models_v3_observed"], [3])
        operation = result["observed_operations"][0]
        self.assertEqual(operation["operation"], "replace_misaligned_model")
        self.assertEqual(operation["confidence"], "high")

    def test_verified_dependency_only_changes_executable(self):
        result = self.repairer.repair_row(
            self.row(
                [11],
                "G: Ellipse;Expression(G)=(x^2/9+y^2/4=1)",
            )
        )
        self.assertEqual(result["models_v3_observed"], [11])
        self.assertEqual(result["models_v3_executable"], [3, 11])
        self.assertEqual(
            result["executable_operations"][0]["operation"],
            "insert_verified_dependency",
        )

    def test_rolls_back_dependency_that_does_not_unlock_consumer(self):
        result = self.repairer.repair_row(
            self.row(
                [46],
                "G: Ellipse;l: Line;A: Point;B: Point;"
                "Expression(G)=(x^2/4+y^2=1);"
                "Expression(l)=(y=x);Intersection(l,G)={A,B}",
            )
        )
        self.assertEqual(result["models_v3_executable"], [46])
        self.assertEqual(result["executable_operations"], [])

    def test_removes_only_verified_adjacent_duplicate(self):
        result = self.repairer.repair_row(
            self.row(
                [3, 3],
                "G: Ellipse;Expression(G)=(x^2/9+y^2/4=1)",
            )
        )
        self.assertEqual(result["models_v3_observed"], [3])
        self.assertEqual(
            result["observed_operations"][0]["operation"],
            "remove_adjacent_duplicate",
        )

    def test_does_not_cross_replace_when_original_type_exists(self):
        result = self.repairer.repair_row(
            self.row(
                [3],
                "G: Parabola;H: Ellipse;"
                "Expression(G)=(y^2=8*x)",
                process="根据抛物线焦点信息求椭圆H的方程",
            )
        )
        self.assertEqual(result["models_v3_observed"], [3])
        self.assertEqual(result["observed_operations"], [])

    def test_flags_likely_semantic_drift(self):
        result = self.repairer.repair_row(
            self.row(
                [79],
                "G: Hyperbola;H: Line;"
                "Expression(G)=(x^2/4-y^2=1);"
                "Expression(H)=(y=x+m)",
                process="联立方程后由判别式大于零得到参数范围",
            )
        )
        self.assertEqual(
            result["semantic_flags"][0]["status"],
            "likely_semantic_drift",
        )
        self.assertEqual(result["quality_candidate"], "D")


if __name__ == "__main__":
    unittest.main()
