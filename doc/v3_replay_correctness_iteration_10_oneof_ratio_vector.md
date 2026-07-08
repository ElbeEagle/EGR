# V3 Replay Correctness Iteration 10: OneOf, Ratios, and Vector Semantics

## Baseline

Input: `data/train_with_models_v3_candidate.json`

Sequence: `models_v3_observed`, assisted macro apply enabled.

i22 baseline:

- complete sequences: 956 / 5,355 = 17.85%;
- correct answers: 297 / 5,355 = 5.55%;
- selector-usable trajectories: 277 / 5,355 = 5.17%;
- accuracy among evaluable answers: 297 / 300 = 99.00%.

## Stage A: symmetric OneOf semantics

Implemented typed membership for `OneOf(Focus(G))=F`,
`OneOf(Asymptote(G))=l`, and
`PointOnCurve(P,OneOf(Asymptote(G)))` without choosing a left/right branch.

Full result:

| Metric | i22 | Stage A | Delta |
| --- | ---: | ---: | ---: |
| Complete sequences | 956 (17.85%) | 974 (18.19%) | +18 |
| Correct answers | 297 (5.55%) | 300 (5.60%) | +3 |
| Selector usable | 277 (5.17%) | 278 (5.19%) | +1 |
| Evaluable accuracy | 99.00% | 300/303 (99.01%) | no regression |
| Unparsed facts | 3,222 | 2,989 | -233 |

## Stage B: exact segment-length ratios

Positive numeric relations such as
`3*Abs(AB)=2*Abs(CD)` now produce a canonical `DistanceRatioOf` and a squared
coordinate equation.  Compatibility output preserves `RequestedDistanceOf`
for legacy model 53.

Among the 21 formerly unparsed numeric-ratio rows, complete-sequence and answer
counts did not change because most endpoints still lack coordinates.  Across
the full dataset, the stronger equation solves row 5965, which was previously
parsed only as a nested symbolic distance expression:

- newly correct answers: +1;
- new complete sequences: 0;
- new selector-usable trajectories: 0;
- new evaluable-answer accuracy: 1/1.

This stage is primarily reusable information-space infrastructure.

## Stage C: numeric linear vector relations

The adapter now parses exact multi-term vector identities, the coordinate
compiler lowers them to two component equations, and the condition closure can
extract `c/a` only when:

- ordinary point coefficients cancel exactly;
- every remaining point is a signed focus or vertex of one conic;
- a standard conic form has already been established;
- the resulting ratio is unique and positive.

Legacy model 62 returns auditable `ALREADY_KNOWN` when such a relation has
already produced compiled coordinate equations or a unique `c/a` ratio.  It
does not invent a collinearity fact.

Affected-set result over 134 rows containing non-symbolic vector text:

| Metric | Before | After |
| --- | ---: | ---: |
| Complete sequences | 3/134 (2.24%) | 4/134 (2.99%) |
| Correct answers | 0 | 1/134 (0.75%) |
| Selector usable | 0 | 1/134 (0.75%) |
| Evaluable accuracy | n/a | 1/1 (100%) |

The newly certified trajectory is row 83, whose vector relation yields
`c=3a` and therefore eccentricity 3.

## Final cumulative result

The full i24 run was followed by a compatibility correction for three model-53
rows.  Re-evaluating every affected row restores all three sequences while
preserving the two new correct answers.

| Metric | i22 baseline | Final | Delta |
| --- | ---: | ---: | ---: |
| Complete sequences | 956 (17.85%) | 975 (18.21%) | +19 |
| Correct answers | 297 (5.55%) | 302 (5.64%) | +5 |
| Selector usable | 277 (5.17%) | 279 (5.21%) | +2 |
| Evaluable accuracy | 297/300 (99.00%) | 302/305 (99.02%) | no regression |

The incorrect set remains the audited rows 887, 1834, and 3743.  Row 3743
mixes the `y^2=2px` equation with the alternative `y^2=4px` answer convention.

## Validation

- 106 theorem-v2 unit tests pass;
- source, scripts, and relevant tests pass `compileall`;
- symbolic vector coefficients such as `lambda` remain unresolved rather than
  being guessed;
- failed macro support remains transactional.

## Artifacts

- `src/theorems_v2/expanded_raw_adapter.py`
- `src/theorems_v2/structured_raw_adapter.py`
- `src/theorems_v2/coordinate_equation_compiler.py`
- `src/theorems_v2/condition_closure.py`
- `src/theorems_v2/macro_applicator.py`
- `outputs/theorems_v2/stage_a_oneof_i23_summary.json`
- `outputs/theorems_v2/v3_replay_observed_macro_i24_summary.json`

