# Round 2 Eval Slice Report Handoff

Date: 2026-05-19

Subagent: `eval-slice-report`

Shared checkout: `/Users/ebeleagel/Documents/GitHub/EGR`

## Scope and Safety

- Worked only in the shared checkout.
- No worktree was created.
- No commit, push, reset, restore, checkout, clean, unstage, or `.env` edit was performed.
- Did not edit forbidden implementation or paper files.
- Existing unrelated untracked round2 artifacts were present and left untouched:
  - `outputs/entropy/round2_correctness_join/`
  - `outputs/evaluation/round2_error_audit/`
  - `scripts/entropy/join_entropy_correctness.py`
  - `scripts/evaluation/compare_eval_runs.py`

## Runner Parameter Inspection

Inspected `scripts/evaluation/run_eval_protocol.py` before running evaluation.

Available parameters:

```bash
--num
--seed
--data
--output-dir
--selector-report
--quiet
```

There is no dedicated full-set flag. Full valid-set evaluation is triggered by
passing `--num` greater than or equal to the valid sample count because
`scripts/reasoning/batch_test.py:load_test_data(...)` returns all valid samples
when `num_samples >= len(valid)`.

Dataset counts from `data/train_with_models_v2.json`:

- total rows: `7757`
- valid rows with facts/query/answer: `7624`

Python environment note:

- `/usr/bin/python3` failed because `torch` is not installed.
- `/opt/anaconda3/bin/python` worked with `torch 2.9.1`.
- All successful evaluation commands below used `python`.

## Files Added

- `scripts/evaluation/run_eval_slices.py`
  - Post-processes existing unified eval summaries into compact slice tables.
  - Can also run the same unified evaluation in compact mode and write summary/table artifacts without full sample-level reports.

## Commands Run

Parameter and dataset inspection:

```bash
sed -n '1,260p' scripts/evaluation/run_eval_protocol.py
sed -n '1,240p' scripts/reasoning/batch_test.py
python3 -c "import json; data=json.load(open('data/train_with_models_v2.json')); valid=[d for d in data if d.get('fact_expressions') and d.get('query_expressions') and d.get('answer_expressions')]; print(len(data)); print(len(valid))"
python -c "import sys; print(sys.executable); import torch; print(torch.__version__)"
```

500-sample unified evaluation:

```bash
python scripts/evaluation/run_eval_protocol.py --num 500 --seed 42 --output-dir outputs/evaluation/round2_eval_500 --quiet
python scripts/evaluation/run_eval_slices.py --eval-dir outputs/evaluation/round2_eval_500
```

Full valid-set compact unified evaluation:

```bash
python scripts/evaluation/run_eval_slices.py --run-eval --num 999999 --seed 42 --output-dir outputs/evaluation/round2_eval_full --quiet
```

Validation:

```bash
python -m py_compile scripts/evaluation/run_eval_slices.py
python3 -m py_compile scripts/evaluation/run_eval_slices.py
```

## Main Metrics

Primary metric: final answer accuracy.

Reasoning success is reported separately and should not be used as a substitute
for final answer accuracy.

| Run | Samples | Final answer correct | Final answer accuracy | Reasoning success | Reasoning success rate | Answer accuracy among successful reasoning |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| first-wave integrated 200 | 200 | 21 | 0.1050 | 130 | 0.6500 | 0.1615 |
| round2 500 | 500 | 34 | 0.0680 | 319 | 0.6380 | 0.1066 |
| round2 full valid | 7624 | 391 | 0.0513 | 4879 | 0.6400 | 0.0801 |

Theorem-selection diagnostic:

| Run | Labeled steps | Top-1 | Top-3 | Top-5 |
| --- | ---: | ---: | ---: | ---: |
| first-wave integrated 200 | 374 | 0.1096 | 0.2701 | 0.3690 |
| round2 500 | 886 | 0.1151 | 0.2664 | 0.3600 |
| round2 full valid | 13541 | 0.1218 | 0.2631 | 0.3548 |

## Stability Read

The exact `10.5%` final answer accuracy from the 200-sample integrated slice is
not stable under larger sampling:

- 500-sample run: `34/500 = 6.80%`
- full valid-set run: `391/7624 = 5.13%`

The result still appears above the original first-wave pre-integration
200-sample baseline of `5/200 = 2.5%`, but that is not a matched large-slice
before/after comparison. The defensible statement is:

> The 200-sample 10.5% result was optimistic for the broader valid set. Larger
> round2 runs put current final answer accuracy around 5-7%, while reasoning
> success stays near 64% and remains separate from final answer correctness.

## Full Valid-Set Slice Highlights

Query-type table highlights:

| Query type | Total | Correct | Final answer accuracy | Reasoning success |
| --- | ---: | ---: | ---: | ---: |
| Coordinate | 400 | 49 | 0.1225 | 0.2350 |
| Range | 478 | 57 | 0.1192 | 0.5000 |
| Eccentricity | 1210 | 101 | 0.0835 | 0.8818 |
| Length | 299 | 16 | 0.0535 | 0.4883 |
| Value | 2714 | 102 | 0.0376 | 0.5892 |
| Distance | 526 | 17 | 0.0323 | 0.4829 |
| Equation | 1699 | 49 | 0.0288 | 0.8064 |
| Area | 298 | 0 | 0.0000 | 0.3691 |

Curve-type table highlights:

| Curve type | Total | Correct | Final answer accuracy | Reasoning success |
| --- | ---: | ---: | ---: | ---: |
| Hyperbola | 2650 | 217 | 0.0819 | 0.7879 |
| Ellipse | 2392 | 132 | 0.0552 | 0.7793 |
| Parabola | 2168 | 42 | 0.0194 | 0.3381 |
| Other | 310 | 0 | 0.0000 | 0.4161 |
| Circle | 104 | 0 | 0.0000 | 0.6250 |

Failure-reason table highlights:

| Failure reason | Count | Notes |
| --- | ---: | --- |
| answer_mismatch | 4488 | Reasoning succeeded but final answer was wrong. |
| max_steps | 2418 | Reasoning failure. |
| no_model | 313 | Reasoning failure. |
| exception | 14 | Reasoning failure. |

Reasoning-failure-only distribution:

| Reasoning failure reason | Count |
| --- | ---: |
| max_steps | 2418 |
| no_model | 313 |
| exception | 14 |

## Artifact List

500-sample artifacts:

- `outputs/evaluation/round2_eval_500/report.json`
- `outputs/evaluation/round2_eval_500/samples.jsonl`
- `outputs/evaluation/round2_eval_500/summary.json`
- `outputs/evaluation/round2_eval_500/summary.csv`
- `outputs/evaluation/round2_eval_500/slice_tables.md`
- `outputs/evaluation/round2_eval_500/slice_artifact_manifest.json`
- `outputs/evaluation/round2_eval_500/slice_tables/overall_table.csv`
- `outputs/evaluation/round2_eval_500/slice_tables/query_type_table.csv`
- `outputs/evaluation/round2_eval_500/slice_tables/curve_type_table.csv`
- `outputs/evaluation/round2_eval_500/slice_tables/failure_reason_table.csv`
- `outputs/evaluation/round2_eval_500/slice_tables/failure_reason_distribution.csv`
- `outputs/evaluation/round2_eval_500/slice_tables/reasoning_failure_reason_distribution.csv`

Full valid-set artifacts:

- `outputs/evaluation/round2_eval_full/run_metadata.json`
- `outputs/evaluation/round2_eval_full/summary.json`
- `outputs/evaluation/round2_eval_full/summary.csv`
- `outputs/evaluation/round2_eval_full/slice_tables.md`
- `outputs/evaluation/round2_eval_full/slice_artifact_manifest.json`
- `outputs/evaluation/round2_eval_full/slice_tables/overall_table.csv`
- `outputs/evaluation/round2_eval_full/slice_tables/query_type_table.csv`
- `outputs/evaluation/round2_eval_full/slice_tables/curve_type_table.csv`
- `outputs/evaluation/round2_eval_full/slice_tables/failure_reason_table.csv`
- `outputs/evaluation/round2_eval_full/slice_tables/failure_reason_distribution.csv`
- `outputs/evaluation/round2_eval_full/slice_tables/reasoning_failure_reason_distribution.csv`

## Artifact Size Control

500-sample official runner output sizes:

- `report.json`: `15M`
- `samples.jsonl`: `9.1M`
- `summary.json`: `32K`
- `summary.csv`: `8.0K`
- each slice table: about `4.0K` on disk or less

The 500-sample `report.json` and `samples.jsonl` are kept because the task asked
for completed 500-sample outputs and they are the official unified protocol
artifacts.

Full valid-set artifact control:

- The official runner lacks a summary-only flag and would write a much larger
  full sample-level `report.json` and `samples.jsonl`.
- To keep artifact size controlled, the full valid-set run used
  `run_eval_slices.py --run-eval`, which reuses the unified protocol and writes
  compact summary/table artifacts only.
- Full valid-set compact files are small: `summary.json` is `36K`,
  `summary.csv` is `8.0K`, `run_metadata.json` is `4.0K`, and each slice table
  is about `4.0K` on disk or less.

## Risks and Notes

- The full compact run did not write sample-level traces. This was intentional
  for artifact-size control. If exact exception samples are needed, rerun with
  `--write-samples` or the official runner, expecting large artifacts.
- The full run emitted one Python `SyntaxWarning`: `'tuple' object is not callable`.
  The run completed. The final summary records `14` exception failures, but
  compact mode does not retain sample-level raw exception details.
- There is no matched pre-integration 500/full-valid run in this handoff, so
  larger-slice stability should be stated as post-integration current accuracy,
  not as a rigorous large-slice before/after lift.
- Query/curve slices show that current correctness is concentrated in
  Coordinate/Range/Eccentricity and Hyperbola/Ellipse cases; Area/Circle/Other
  remain at zero final answer accuracy in the full valid-set run.
