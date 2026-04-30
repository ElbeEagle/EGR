from src.evaluation.protocol import (
    build_eval_report,
    build_sample_report,
    compute_trace_selection_metrics,
    summarize_samples,
)


class DummyResult:
    def __init__(self, success=True, answer="5", failure_reason=None):
        self.success = success
        self.answer = answer
        self.failure_reason = failure_reason
        self.model_sequence = [5, 21]
        self.model_names = ["Model5", "Model21"]
        self.reasoning_trace = [
            {
                "step": 1,
                "model_id": 5,
                "candidates": [
                    {"rank": 1, "model_id": 5},
                    {"rank": 2, "model_id": 12},
                    {"rank": 3, "model_id": 21},
                ],
            },
            {
                "step": 2,
                "model_id": 21,
                "candidates": [
                    {"rank": 1, "model_id": 12},
                    {"rank": 2, "model_id": 21},
                ],
            },
        ]
        self.num_steps = 2
        self.elapsed_time = 0.25


def test_trace_selection_metrics_topk_hits():
    metrics = compute_trace_selection_metrics(
        [
            {"candidates": [{"model_id": 5}, {"model_id": 7}]},
            {"candidates": [{"model_id": 1}, {"model_id": 2}, {"model_id": 9}]},
        ],
        [5, 9],
    )

    assert metrics["evaluated_steps"] == 2
    assert metrics["top1_hits"] == 1
    assert metrics["top3_hits"] == 2
    assert metrics["top5_accuracy"] == 1.0


def test_build_sample_report_records_required_schema_fields():
    sample = {
        "id": 2,
        "fact_expressions": "G: Hyperbola;Expression(G) = (x^2/4 - y^2/25 = 1)",
        "query_expressions": "m",
        "answer_expressions": "5",
        "models": [5, 21],
    }

    report = build_sample_report(sample, DummyResult(), final_answer_correct=True)

    assert report["sample_id"] == 2
    assert report["curve_type"] == "Hyperbola"
    assert report["query_type"] == "Value"
    assert report["reasoning_success"] is True
    assert report["final_answer_correct"] is True
    assert report["failure_reason"] is None
    assert report["theorem_selection"]["evaluated_steps"] == 2
    assert report["theorem_selection"]["top1_hits"] == 1
    assert report["theorem_selection"]["top3_hits"] == 2


def test_summarize_samples_groups_failures_and_model_usage():
    correct = build_sample_report(
        {
            "id": 1,
            "fact_expressions": "G: Ellipse",
            "query_expressions": "Eccentricity(G)",
            "answer_expressions": "sqrt(3)/3",
            "models": [5],
        },
        DummyResult(answer="sqrt(3)/3"),
        final_answer_correct=True,
    )
    wrong = build_sample_report(
        {
            "id": 2,
            "fact_expressions": "G: Hyperbola",
            "query_expressions": "Distance(A, Focus(G))",
            "answer_expressions": "5",
            "models": [5, 21],
        },
        DummyResult(answer="4"),
        final_answer_correct=False,
    )
    failed = build_sample_report(
        {
            "id": 3,
            "fact_expressions": "G: Parabola",
            "query_expressions": "Expression(G)",
            "answer_expressions": "x^2=4y",
            "models": [],
        },
        DummyResult(success=False, answer=None, failure_reason="Reached max steps (15)"),
        final_answer_correct=False,
    )

    summary = summarize_samples([correct, wrong, failed])

    assert summary["overall"]["total_samples"] == 3
    assert summary["overall"]["reasoning_success_count"] == 2
    assert summary["overall"]["final_answer_correct_count"] == 1
    assert summary["failure_reason_distribution"]["answer_mismatch"] == 1
    assert summary["failure_reason_distribution"]["max_steps"] == 1
    assert summary["by_curve_type"]["Ellipse"]["final_answer_accuracy"] == 1.0
    assert summary["by_query_type"]["Distance"]["total_samples"] == 1
    assert summary["model_id_usage"]["5"] == 3
    assert summary["by_model_id"]["21"]["total_samples"] == 3


def test_build_eval_report_includes_external_selector_summary():
    report = build_eval_report(
        [],
        selector_report={
            "total_predictions": 10,
            "top1_hits": 4,
            "top3_hits": 7,
            "top5_hits": 9,
        },
    )

    selector = report["summary"]["external_selector_report"]
    assert selector["top1_accuracy"] == 0.4
    assert selector["top3_accuracy"] == 0.7
    assert selector["top5_accuracy"] == 0.9
