# V3 replay correctness iteration 12: chord-distance bridge

## Scope

This iteration deliberately adds one applicator closure rule only.  A derived
chord-length formula is exposed as `DistanceFormulaOf(A, B)` when `A` and `B`
are the two points in the corresponding line/conic `IntersectionOf` fact.

Supported source predicates:

- `ChordLengthFormulaOf`
- `ChordLengthWithKFormulaOf`
- `ParabolaFocalChordLengthOf`

The rule does not solve new intersections or change theorem matching.  It only
connects an already-derived chord length to the endpoint-distance predicate
used by the goal checker and quantity space.

## Fixed 500-row replay

Baseline: `stage_line_point_slope_500_summary.json`  
Candidate: `stage_chord_distance_500_summary.json`

| Metric | Baseline | Candidate | Delta |
|---|---:|---:|---:|
| Sequence complete | 104/500 (20.80%) | 104/500 (20.80%) | 0 |
| Answer correct | 21/500 (4.20%) | 26/500 (5.20%) | +5 |
| Selector usable | 20/500 (4.00%) | 24/500 (4.80%) | +4 |
| Accuracy when evaluable | 21/21 (100%) | 26/26 (100%) | unchanged |

New correct rows: 322, 487, 541, 631, and 655.  Rows 487, 541, 631,
and 655 also became selector-usable.  Row 544 moved from `GOAL_NOT_REACHED`
to `VALUE_UNRESOLVED`, showing that the bridge is present but the symbolic
coordinate sum still needs a separate derivation.  There were no losses in
sequence completion, selector usability, or answer correctness.

## Verification

- 108 theorem-v2 unit tests pass.
- The new regression test replays the ID 487 theorem chain and checks the
  resulting segment goal as `ANSWER_CORRECT`.

## Interpretation

This is a high-leverage applicator compatibility fix: theorem 51 was already
computing the right numeric value, but the result remained under a theorem-
specific predicate that the goal/quantity layer could not consume.  The gain
therefore comes from improving information flow, not changing the theorem
sequence or adding search.
