# Task

Round 2 AAAI2027 integration for EGR, focused on explaining and hardening the
first-wave metric split:

- Final answer accuracy improved from `5/200 = 2.5%` to `21/200 = 10.5%`.
- Reasoning success dropped from `147/200 = 73.5%` to `130/200 = 65.0%`.

This round prioritized sample-level error audit and targeted solver hardening,
not new theorem/selector feature stacking.

# Starting State

- Shared checkout: `/Users/ebeleagel/Documents/GitHub/EGR`.
- No worktree was used.
- No commit or push was performed.
- Initial `git status --short` was clean in this thread.
- Protected hot files were not edited:
  - `src/reasoning/reasoning_engine.py`
  - `src/reasoning/model_selector.py`
  - `src/theorems/`
  - `src/selector/`
  - `tex/icml2026.tex`

# Subagents Completed

- `integration-error-audit`
  - Added offline before/after sample comparison.
  - Found `18` wrong-to-correct and `2` correct-to-wrong samples in the
    first-wave integration.
  - Found reasoning success transitions: `35` success-to-failure and `18`
    failure-to-success.
  - Critical diagnosis: `model_sequence_changed = 0/200` and
    `num_steps_changed = 0/200`, so the original success drop came from
    post-trace answer extraction / success marking, not selector route drift.

- `eval-slice-report`
  - Ran 500-sample and compact full-valid evaluations before solver hardening.
  - Showed the first-wave 200-sample `10.5%` accuracy was optimistic:
    `34/500 = 6.80%`, full valid `391/7624 = 5.13%`.

- `entropy-correctness-join`
  - Joined entropy data to eval by `problem_id == sample_id`.
  - Join key is stable for matched rows, but coverage is only `33/200 = 16.5%`.
  - Result is diagnostic only; it does not support claiming learned entropy
    predicts final answer correctness.

- `solver-hardening`
  - Added focused regression tests and exact-pattern symbolic extraction fixes
    for Parabola/Value regressions.
  - Restored samples `360` and `2252`.
  - Preserved all first-wave symbolic extraction gains.

# Files Changed

Analysis and evaluation:

- `scripts/evaluation/compare_eval_runs.py`
- `scripts/evaluation/run_eval_slices.py`
- `scripts/entropy/join_entropy_correctness.py`
- `dev_logs/aaai2027/round2_integration_error_audit_handoff.md`
- `dev_logs/aaai2027/round2_eval_slice_report_handoff.md`
- `dev_logs/aaai2027/round2_entropy_correctness_join_handoff.md`
- `dev_logs/aaai2027/round2_solver_hardening_handoff.md`
- `dev_logs/aaai2027/round2_integration_handoff.md`

Solver hardening:

- `src/reasoning/answer_extractor.py`
- `src/solver/symbolic_solver.py`
- `src/state/state_constructor.py`
- `tests/test_answer_extractor_symbolic_solver.py`
- `tests/test_solver_symbolic.py`

New artifacts:

- `outputs/evaluation/round2_error_audit/`
- `outputs/evaluation/round2_eval_500/`
- `outputs/evaluation/round2_eval_full/`
- `outputs/evaluation/round2_solver_smoke/`
- `outputs/evaluation/round2_main_integration_200/`
- `outputs/evaluation/round2_main_integration_500/`
- `outputs/evaluation/round2_main_integration_full/`
- `outputs/evaluation/round2_main_delta_200/`
- `outputs/evaluation/round2_main_delta_500/`
- `outputs/entropy/round2_correctness_join/`

Unowned/unintegrated note:

- `docs/learned_state_entropy.md` is currently untracked but was not part of
  the declared round2 integration or solver-hardening write scope.

# New Interfaces

- `scripts/evaluation/compare_eval_runs.py`
  - Offline JSONL before/after comparison with transition matrices and top
    gain/regression tables.
- `scripts/evaluation/run_eval_slices.py`
  - Generates compact query/curve/failure slice tables from unified eval
    summaries, and can run compact summary-only full-set eval.
- `scripts/entropy/join_entropy_correctness.py`
  - Conservative entropy/eval correctness join with explicit claim boundaries.
- `AnswerExtractor`
  - Added routing for `LineSegmentOf`, `Slope`, `Min`/`Max`, `AngleOf`, and
    algebraic expressions containing `Abs(LineSegmentOf(...))`.
- `SymbolicSolver`
  - Added focused parabola/value helpers for line segments, chord slopes,
    focal distances, reflected minimum distance, and related formal patterns.
- `StateConstructor`
  - Now preserves unmatched coordinate forms and `IsChordOf(...)` as geometric
    relations instead of dropping them.

# Metrics Before / After

Primary metric is final answer accuracy. Reasoning success is separate.

| Run | Final answer correct | Final answer accuracy | Reasoning success | Answer accuracy among successful reasoning |
| --- | ---: | ---: | ---: | ---: |
| protocol baseline 200 | `5/200` | `2.50%` | `147/200 = 73.50%` | `3.40%` |
| first-wave integrated 200 | `21/200` | `10.50%` | `130/200 = 65.00%` | `16.15%` |
| round2 hardened 200 | `33/200` | `16.50%` | `140/200 = 70.00%` | `23.57%` |
| first-wave integrated 500 | `34/500` | `6.80%` | `319/500 = 63.80%` | `10.66%` |
| round2 hardened 500 | `47/500` | `9.40%` | `337/500 = 67.40%` | `13.95%` |
| first-wave compact full valid | `391/7624` | `5.13%` | `4879/7624 = 64.00%` | `8.01%` |
| round2 compact full valid | `453/7624` | `5.94%` | `4971/7624 = 65.20%` | `9.11%` |

Matched first-wave integrated 200 -> round2 hardened 200:

- Wrong -> correct: `12`
- Correct -> wrong: `0`
- Failure -> success: `10`
- Success -> failure: `0`

Matched first-wave integrated 500 -> round2 hardened 500:

- Wrong -> correct: `13`
- Correct -> wrong: `0`
- Failure -> success: `18`
- Success -> failure: `0`

# Tests Run

```bash
python -m pytest tests/test_evaluation_protocol.py tests/test_answer_extractor_symbolic_solver.py tests/test_solver_symbolic.py tests/test_entropy_estimator.py tests/test_entropy_dataset.py
```

Result: `56 passed`.

```bash
python scripts/evaluation/run_eval_protocol.py --num 200 --seed 42 --output-dir outputs/evaluation/round2_main_integration_200
python scripts/evaluation/run_eval_protocol.py --num 500 --seed 42 --output-dir outputs/evaluation/round2_main_integration_500
python scripts/evaluation/run_eval_slices.py --run-eval --num 999999 --seed 42 --output-dir outputs/evaluation/round2_main_integration_full --quiet
```

Result: completed. The compact full run emitted the pre-existing warning
`SyntaxWarning: 'tuple' object is not callable`, but wrote valid summary tables.

```bash
python scripts/evaluation/run_eval_slices.py --eval-dir outputs/evaluation/round2_main_integration_200
python scripts/evaluation/run_eval_slices.py --eval-dir outputs/evaluation/round2_main_integration_500
python scripts/evaluation/compare_eval_runs.py --before outputs/evaluation/main_integration_200/samples.jsonl --after outputs/evaluation/round2_main_integration_200/samples.jsonl --output-dir outputs/evaluation/round2_main_delta_200
python scripts/evaluation/compare_eval_runs.py --before outputs/evaluation/round2_eval_500/samples.jsonl --after outputs/evaluation/round2_main_integration_500/samples.jsonl --output-dir outputs/evaluation/round2_main_delta_500
git diff --check
python -m compileall src scripts
```

Result: completed; `git diff --check` passed and compileall reported no errors.

# Known Risks

- The solver hardening is exact-pattern based. Unsupported tangent, chord,
  angle, and optimization variants still return `not found`.
- Full-valid final answer accuracy is still low: `5.94%`. The round2 change is
  a real improvement but not enough for a strong AAAI claim by itself.
- Remaining full-valid failures are dominated by `answer_mismatch` and
  `max_steps`; these should not be collapsed into a single metric.
- Entropy correctness evidence is underpowered: only `33/200` joined eval
  samples and `3` final-correct positives in the joined subset.
- `docs/learned_state_entropy.md` is present as an untracked, unowned file and
  should be reviewed separately before staging.

# Integration Notes

- The original first-wave success drop is now explained: same trace/step counts
  became different final outcomes due to answer extraction / success marking.
- The round2 hardening improves both primary accuracy and reasoning success on
  matched 200/500 samples, with no final-answer or reasoning-success
  regressions in those matched comparisons.
- The 200-sample result after hardening (`16.5%`) is still optimistic relative
  to 500/full (`9.4%` / `5.94%`), so paper text should use larger-slice numbers
  when making broad claims.
- Theorem-selection diagnostics should remain auxiliary. Final answer accuracy
  is the gating metric.
- No commit or push was performed.

# Next Round Recommendations

1. Run a dedicated remaining-error audit on `round2_main_integration_500` and
   full-valid slice tables, starting with `answer_mismatch` not `max_steps`.
2. Add focused tests before extending tangent/chord/angle/optimization support.
3. Build actual eval-applied entropy trajectories or regenerate entropy labels
   over full eval coverage before making answer-correctness entropy claims.
4. Decide whether to keep, revise, or discard `docs/learned_state_entropy.md`
   before any Git handoff.
5. Continue separating final answer accuracy, reasoning success, and
   theorem-selection diagnostics in all reports.
