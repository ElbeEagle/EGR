import unittest

from scripts.theorems_v2.sample_nonempty_sequences import (
    review_record,
    sample_rows,
)


class SampleNonemptySequenceTests(unittest.TestCase):
    def test_only_nonempty_sequences_are_sampled_reproducibly(self):
        rows = [
            {"id": 1, "models_v3_executable": []},
            {"id": 2, "models_v3_executable": [2]},
            {"id": 3, "models_v3_executable": [3]},
            {"id": 4, "models_v3_executable": [4]},
        ]
        first, eligible = sample_rows(
            rows, "models_v3_executable", sample_size=2, seed=7
        )
        second, _ = sample_rows(
            rows, "models_v3_executable", sample_size=2, seed=7
        )
        self.assertEqual(eligible, 3)
        self.assertEqual(first, second)
        self.assertTrue(all(row["models_v3_executable"] for row in first))

    def test_review_record_adds_readable_model_names(self):
        row = {
            "dataset_index": 9,
            "id": 10,
            "models_v3_executable": [3, 99],
        }
        item = review_record(
            row,
            "models_v3_executable",
            {3: "Ellipse_Equation_Standard_X"},
            sample_number=1,
        )
        self.assertEqual(
            item["theorem_names"],
            ["Ellipse_Equation_Standard_X", "Unknown(99)"],
        )
        self.assertEqual(
            item["theorem_content_sequence"][0]["formula"],
            "x^2/a^2+y^2/b^2=1",
        )

    def test_review_record_includes_applicator_result(self):
        row = {
            "dataset_index": 0,
            "id": 1,
            "models_v3_executable": [3],
        }
        replay = {
            "sequence_success": True,
            "step_statuses": ["APPLIED"],
            "support_model_ids": [[]],
            "first_failure": None,
            "initial_goal": {"status": "GOAL_NOT_REACHED"},
            "goal": {"status": "ANSWER_CORRECT"},
            "goal_progress": True,
            "selector_usable": True,
        }
        item = review_record(
            row,
            "models_v3_executable",
            {},
            sample_number=1,
            replay_result=replay,
        )
        self.assertTrue(item["applicator_result"]["can_complete_sequence"])
        self.assertTrue(item["applicator_result"]["answer_correct"])

    def test_rejects_sample_larger_than_population(self):
        with self.assertRaisesRegex(ValueError, "only 1"):
            sample_rows(
                [{"models": [1]}], "models", sample_size=2, seed=1
            )


if __name__ == "__main__":
    unittest.main()
