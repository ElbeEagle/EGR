# Round 2 Integration Error Audit Handoff

Date: 2026-05-19

## Scope

Subagent: `integration-error-audit`

Shared checkout only. No worktree, commit, push, reset, restore, checkout, clean,
unstage, `.env`, or business-code changes were performed.

Inputs compared:

- `outputs/evaluation/protocol_200_smoke/samples.jsonl`
- `outputs/evaluation/main_integration_200/samples.jsonl`
- `outputs/evaluation/main_integration_200/summary.json`

## Files Added / Updated

- `scripts/evaluation/compare_eval_runs.py`
  - Offline JSONL comparison CLI.
  - Reads two sample-level eval runs and writes delta JSON, CSV tables, and a
    Markdown summary.
  - Does not import or execute the reasoning engine, solver, selector, or
    theorem library.
- `outputs/evaluation/round2_error_audit/delta.json`
  - Machine-readable full audit payload with per-sample deltas, transition
    matrices, query/curve summaries, model usage deltas, top cases, and repair
    priorities.
- `outputs/evaluation/round2_error_audit/sample_deltas.csv`
  - Per-sample before/after table.
- `outputs/evaluation/round2_error_audit/transition_matrices.csv`
  - Flattened transition matrices for final correctness, reasoning success,
    failure reason, reasoning failure reason, query type, curve type, first/last
    model, and num-step deltas.
- `outputs/evaluation/round2_error_audit/accuracy_gain_top20.csv`
  - Top wrong-to-correct samples.
- `outputs/evaluation/round2_error_audit/success_regression_top20.csv`
  - Top reasoning-success-to-failure samples.
- `outputs/evaluation/round2_error_audit/summary.md`
  - Human-readable audit summary and solver-hardening priorities.
- `dev_logs/aaai2027/round2_integration_error_audit_handoff.md`
  - This handoff.

## Commands Run

```bash
python3 -m py_compile scripts/evaluation/compare_eval_runs.py
python3 scripts/evaluation/compare_eval_runs.py --before outputs/evaluation/protocol_200_smoke/samples.jsonl --after outputs/evaluation/main_integration_200/samples.jsonl --output-dir outputs/evaluation/round2_error_audit
python3 -c "import json; p=json.load(open('outputs/evaluation/round2_error_audit/delta.json')); print(p['summary']); print(len(p['samples']), len(p['top_accuracy_gain_samples']), len(p['top_success_regression_samples']))"
git diff --check
git status --short
```

Validation result:

- `py_compile` passed.
- Comparison completed and wrote `outputs/evaluation/round2_error_audit/`.
- `delta.json` contains `200` sample deltas, `18` accuracy-gain samples, and
  `20` listed success-regression samples.
- `git diff --check` passed.
- `git status --short` showed this worker's new files plus pre-existing
  unrelated untracked round2/entropy slice artifacts outside this worker's
  scope; those were left untouched.

## Headline Findings

Primary metric:

- Final answer accuracy improved from `5/200 = 2.5%` to `21/200 = 10.5%`.
- Net primary-metric delta is `+16` correct samples.
- Sample-level transitions:
  - wrong -> correct: `18`
  - correct -> wrong: `2`
  - correct -> correct: `3`
  - wrong -> wrong: `177`

Reasoning success, reported separately:

- Reasoning success dropped from `147/200 = 73.5%` to `130/200 = 65.0%`.
- Net reasoning-success delta is `-17` samples.
- Sample-level transitions:
  - success -> success: `112`
  - success -> failure: `35`
  - failure -> success: `18`
  - failure -> failure: `35`

Critical diagnostic:

- `model_sequence_changed_count = 0/200`
- `num_steps_changed_count = 0/200`
- Model usage deltas are all zero.
- Therefore the reasoning-success drop is not theorem-route or model-selection
  drift. It is post-trace behavior: the same traces now produce different
  `answer` / `result.success` / `failure_reason` outcomes, primarily through
  answer extraction and final success marking.

Failure-reason transitions:

- `answer_mismatch -> answer_mismatch`: `96`
- `answer_mismatch -> max_steps`: `33`
- `max_steps -> max_steps`: `24`
- `answer_mismatch -> none`: `13`
- `max_steps -> answer_mismatch`: `13`
- `no_model -> no_model`: `11`
- `max_steps -> none`: `5`
- `none -> none`: `3`
- `none -> max_steps`: `2`

Query types did not change; the matrix is fully diagonal.

## Query / Curve Slices

Largest final-accuracy gains:

- `Equation`: `0 -> 7` correct, `+7`
- `Eccentricity`: `1 -> 5` correct, `+4`
- `Range`: `0 -> 2` correct, `+2`
- `Coordinate`: `0 -> 2` correct, `+2`
- `Value`: `2 -> 3` correct, `+1`

Largest reasoning-success drops:

- `Value`: `64 -> 40`, `-24`
- `Range`: `14 -> 10`, `-4`
- `Distance`: `6 -> 3`, `-3`

Curve slices:

- `Hyperbola`: final correct `2 -> 12`, `+10`
- `Ellipse`: final correct `1 -> 8`, `+7`
- `Parabola`: final correct `2 -> 1`, `-1`; reasoning success `46 -> 19`,
  `-27`

## Top Cases

Accuracy-gain examples are in:

- `outputs/evaluation/round2_error_audit/accuracy_gain_top20.csv`

Notable gain samples:

- `5332`: Hyperbola/Equation, `Expression(H)`, predicted `3 -> y^2=-36*(x-4)`
- `926`: Ellipse/Range, `Range(a)`, predicted symbolic eccentricity expression
  -> `(1, 3/2)+(3/2, 2)`
- `2841`: Hyperbola/Range, `Range(k)`, predicted discriminant expression ->
  `(-oo, -4)+(1, +oo)`
- `6302`, `2710`: Hyperbola/Eccentricity, `not found -> exact value`
- `4551`, `2840`: Coordinate cases recovered from `max_steps` to correct

Success-regression examples are in:

- `outputs/evaluation/round2_error_audit/success_regression_top20.csv`

Notable regressions:

- `360`: Parabola/Value, correct before, now `LineSegmentOf not found`
- `2252`: Parabola/Value, correct before, now `Slope not found`
- Many Parabola/Value regressions now fail with `max_steps` and `not found`
  outputs for `Abs(LineSegmentOf(...))`, `Min(...)`, `Slope(...)`,
  `LineSegmentOf(...)`, and `AngleOf(...)`.

## Solver-Hardening Priorities

1. P0: Protect primary-metric regressions.
   - Start with samples `360` and `2252`.
   - Both were correct before and wrong after.
   - Add focused regression tests before broad answer-extractor changes.

2. P0: Recover reasoning-success regressions without conflating them with final
   accuracy.
   - `35` samples changed from reasoning success to reasoning failure.
   - Largest bucket is `max_steps / Value / Parabola` with `23` samples.
   - `model_sequence_changed = 0/35`, so replay through `AnswerExtractor` and
     `result.success` marking first.

3. P1: Preserve the symbolic answer-extraction gains.
   - `18` samples moved wrong -> correct.
   - Top gain buckets: `Equation=7`, `Eccentricity=4`, `Value=3`, `Range=2`,
     `Coordinate=2`.
   - Convert representative gain samples into regression tests before changing
     the same extractor paths.

4. P2: Reduce remaining successful-reasoning answer mismatches.
   - After-run still has `109` reasoning-successful but answer-wrong samples.
   - Largest query bucket is `Value` with `37` samples.
   - Tackle only after P0 regressions are covered.

5. P2: Add or tune no-progress loop handling.
   - `77` failed after-run samples repeatedly apply one model.
   - Model `29` appears in `25` loop-like failures.
   - This is a real solver-hardening target, but it is not the cause of the
     before/after route delta because traces are identical.

## Notes for Main Thread

- Use `outputs/evaluation/round2_error_audit/summary.md` as the human-readable
  source of truth for the round2 audit.
- Use `delta.json` for scripted follow-up slicing.
- Do not describe the integration as an unqualified reasoning-process
  improvement: final answer accuracy improved, while reasoning success dropped.
- The next implementation thread should stay focused on answer extraction /
  success marking and targeted Parabola/Value repairs before adding more theorem
  features.
