# Theorem Audit Report

Date: 2026-04-28
Worker: Theorem Audit

## 1. Current Registered Model IDs

`TheoremLibrary` currently registers 52 models:

```text
0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 16, 17, 19, 21, 22, 24,
29, 32, 33, 41, 42, 43, 44, 46, 47, 49, 51, 52, 53, 54, 55, 56, 57, 59, 61,
62, 63, 65, 66, 68, 70, 72, 75, 76, 77, 78, 79
```

The new files created in this audit are not registered, by design.

## 2. Training Models Used But Not Registered

`data/train_with_models_v2.json` contains 7757 samples, 5359 non-empty model
sequences, 20226 total model steps, and 79 unique model IDs. Among these,
27 model IDs appear in training sequences but are not currently registered:

```text
15, 18, 20, 23, 25, 26, 27, 28, 30, 31, 34, 35, 36, 37, 38, 39, 40, 45, 48,
58, 60, 64, 67, 69, 71, 73, 74
```

Model 50 is defined in `model/conic_model_ids.json` but did not appear in
`train_with_models_v2.json` in this audit.

## 3. High-Frequency Missing Models

| Rank | ID | Training steps | Samples | Model name |
|---:|---:|---:|---:|---|
| 1 | 38 | 154 | 154 | Ellipse_Tangent_Line |
| 2 | 27 | 53 | 53 | Ellipse_Directrix |
| 3 | 71 | 43 | 43 | Equal_Area_Method |
| 4 | 18 | 39 | 39 | Ellipse_Latus_Rectum |
| 5 | 39 | 39 | 39 | Parabola_Tangent_Line |
| 6 | 45 | 37 | 37 | Point_Difference_Method_Ellipse |
| 7 | 23 | 32 | 32 | Hyperbola_Common_Asymptote_System |
| 8 | 58 | 32 | 32 | Triangle_Area_Coordinate |
| 9 | 69 | 30 | 30 | Trapezoid_Midline_Theorem |
| 10 | 64 | 26 | 26 | Basic_Inequality_Equal_Condition |
| 11 | 67 | 22 | 22 | Discriminant_Intersect_Condition |
| 12 | 30 | 19 | 19 | Ellipse_Focal_Triangle_Area |
| 13 | 48 | 18 | 18 | Sine_Law |
| 14 | 28 | 18 | 18 | Hyperbola_Directrix |
| 15 | 15 | 17 | 17 | Hyperbola_Eccentricity_Range |

First batch implemented in files only: 18, 27, 38, 64. These were selected
because they are high-frequency and have direct structured outputs. I did not
implement 71, 39, 45, or 58 in this pass because they need tighter downstream
contracts or have formula convention ambiguity.

## 4. Batch Failure Association

From `outputs/reasoning/batch_test_report.json`:

```text
total_samples = 200
success_count = 147
success_rate = 0.735
answer_correct = 5
accuracy = 0.025
failure_reasons = {max_steps: 42, no_model: 11}
```

Only 20 failure details are stored in the report. In those details,
`max_steps` is dominated by repeated application of broad models:

| Rank | Model ID | Model name | Tried count in stored max-step failures |
|---:|---:|---|---:|
| 1 | 62 | Vector_Collinear_Condition | 73 |
| 2 | 1 | Hyperbola_Definition | 50 |
| 3 | 0 | Ellipse_Definition | 49 |
| 4 | 53 | Two_Points_Distance | 19 |
| 5 | 56 | Triangle_Area_Formula | 15 |
| 6 | 47 | Cosine_Law | 15 |
| 7 | 13 | Eccentricity_Formula | 14 |
| 8 | 43 | Vieta_Theorem_Product | 12 |
| 9 | 54 | Midpoint_Formula | 5 |
| 10 | 42 | Vieta_Theorem_Sum | 3 |

The stored `no_model` failures have empty `models_tried`. Their matched
training labels were:

| Sample ID | Query | Training model sequence | Missing registered IDs |
|---:|---|---|---|
| 1158 | `Max(x1^2+2*y1)` | `[3, 79]` | none |
| 6085 | `Expression(G)` | `[5, 6, 21, 12]` | none |
| 578 | `Min(z)` | `[7, 72, 78, 65, 66, 79]` | none |

Interpretation: stored `no_model` failures are more likely due to state
construction, selector filtering, or overly strict `can_apply()` gates than
unregistered model IDs.

## 5. Low-Quality `apply()` Issues

Observed issues that should be handled by future model hardening:

1. Several `apply()` implementations add natural-language relations only,
   with little or no structured state. Examples: `model_063.py`,
   `model_056.py`, `model_029.py`.
2. Broad models can be selected repeatedly and append duplicate/no-op facts,
   causing `max_steps` loops. The stored failures show this for IDs 0, 1, 53,
   56, and 62.
3. Many model `apply()` methods append `state.applied_models`, while
   `TheoremLibrary.apply_model()` also appends. This can duplicate model IDs
   when library-level application is used.
4. Some `can_apply()` methods are deliberately loose from earlier stage-2
   expansion. This improves coverage but weakens selector feedback because
   "applicable" does not always imply "adds useful new information".
5. Some formulas use display-only strings that are hard for the solver or
   answer extractor to consume. Future model fixes should prefer
   `parameters`, `equations`, `coordinates`, and `constraints`.

## 6. First-Batch Fixes/New Models

Added focused, unregistered model files:

| ID | File | Structured outputs |
|---:|---|---|
| 18 | `src/theorems/models/model_018.py` | `parameters["ellipse_latus_rectum"]`, `parameters["latus_rectum"]`, relation |
| 27 | `src/theorems/models/model_027.py` | `parameters["directrix_axis"]`, `parameters["directrix_distance"]`, `parameters["ellipse_directrix"]`, equation |
| 38 | `src/theorems/models/model_038.py` | `parameters["tangent_point"]`, `parameters["tangent_line"]`, equation |
| 64 | `src/theorems/models/model_064.py` | `parameters["basic_inequality_equality_condition"]`, `constraints`, relation |

Focused tests were added in `tests/test_theorem_missing_models.py`.

## 7. Integration Registration Needed

Do not register these automatically in this worker. Integration should review
and then patch `src/theorems/theorem_library.py` to import and register:

```text
18 Ellipse_Latus_Rectum
27 Ellipse_Directrix
38 Ellipse_Tangent_Line
64 Basic_Inequality_Equal_Condition
```

Suggested next implementation candidates after integration:

```text
39 Parabola_Tangent_Line
45 Point_Difference_Method_Ellipse
58 Triangle_Area_Coordinate
67 Discriminant_Intersect_Condition
71 Equal_Area_Method
```

For model 39, first reconcile the repository convention for `p`: existing
parabola standard models use `y^2 = 2px`, while the description table lists
the tangent formula as `y0*y = 2p(x+x0)`.

## 8. Commands Run

```bash
sed -n '1,260p' agent_prompt/03_theorem_audit_agent.md
rg -n "EGR|Conic10K|theorem|AAAI2027|reasoning_engine|theorem_library" /Users/ebeleagel/.codex/memories/MEMORY.md
find . -maxdepth 3 -type f | sort | sed -n '1,240p'
git status --short
rg --files src/theorems tests | sort
sed -n '1,260p' src/theorems/base_model.py
sed -n '1,260p' src/theorems/theorem_library.py
sed -n '1,260p' tests/analyze_missing_models.py
sed -n '1,300p' tests/analyze_model_failures.py
jq 'length' model/conic_model_ids.json
jq '.summary, .failure_reasons' outputs/reasoning/batch_test_report.json
python tests/analyze_missing_models.py
python tests/analyze_model_failures.py
python -m pytest tests/test_theorem_missing_models.py
python -m pytest tests/test_theorem_*.py
git diff --check
git status --short
```
