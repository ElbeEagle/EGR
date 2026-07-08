import unittest

from scripts.theorems_v2.measure_sequence_quality import (
    evaluate_rows,
    select_rows,
)


class _FakeBenchmark:
    def __init__(self, results):
        self.results = iter(results)

    def evaluate_row(self, *args, **kwargs):
        return next(self.results)


def _result(sequence_ok, goal_status, progress=False, failure=None):
    return {
        "sequence_success": sequence_ok,
        "goal": {"status": goal_status},
        "goal_progress": progress,
        "first_failure": failure,
    }


class SequenceQualityMeasurementTests(unittest.TestCase):
    def test_select_rows_reports_exclusion_reasons(self):
        rows = [
            {"models_v3_observed": [], "process": "x"},
            {"models_v3_observed": [1], "process": ""},
            {"models_v3_observed": [2], "process": "x"},
        ]
        selected, exclusions = select_rows(rows, "models_v3_observed")
        self.assertEqual(len(selected), 1)
        self.assertEqual(exclusions["empty_sequence"], 1)
        self.assertEqual(exclusions["empty_process"], 1)

    def test_rates_use_all_evaluated_sequences_as_main_denominator(self):
        rows = [{}, {}, {}]
        benchmark = _FakeBenchmark(
            [
                _result(True, "ANSWER_CORRECT", progress=True),
                _result(True, "GOAL_NOT_REACHED"),
                _result(
                    False,
                    "ANSWER_INCORRECT",
                    failure={"status": "NO_MATCH"},
                ),
            ]
        )
        summary = evaluate_rows(
            rows, benchmark, "models_v3_observed", progress_every=0
        )
        self.assertEqual(summary["execution_success"]["rows"], 2)
        self.assertAlmostEqual(summary["execution_success"]["rate"], 2 / 3)
        self.assertEqual(summary["final_answer_correct"]["rows"], 1)
        self.assertAlmostEqual(summary["final_answer_correct"]["rate"], 1 / 3)
        self.assertEqual(
            summary["answer_accuracy_when_evaluable"]["denominator"], 2
        )
        self.assertEqual(summary["first_failure_statuses"], {"NO_MATCH": 1})


if __name__ == "__main__":
    unittest.main()
