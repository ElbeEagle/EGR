# Theorem Audit Handoff

Date: 2026-04-28
Worker: Theorem Audit

## What I Did

- Read and followed `agent_prompt/03_theorem_audit_agent.md`.
- Audited registered model coverage against `model/conic_model_ids.json` and
  `data/train_with_models_v2.json`.
- Checked stored batch failures in `outputs/reasoning/batch_test_report.json`.
- Added four focused model files for high-frequency missing IDs.
- Added focused tests for the new model files.
- Wrote the detailed audit report at
  `dev_logs/aaai2027/theorem_audit_report.md`.

## Files Changed

- `src/theorems/models/model_018.py`
- `src/theorems/models/model_027.py`
- `src/theorems/models/model_038.py`
- `src/theorems/models/model_064.py`
- `tests/test_theorem_missing_models.py`
- `dev_logs/aaai2027/theorem_audit_report.md`
- `dev_logs/aaai2027/theorem_audit_handoff.md`

## New/Fixed Model IDs

- 18: `Ellipse_Latus_Rectum`
- 27: `Ellipse_Directrix`
- 38: `Ellipse_Tangent_Line`
- 64: `Basic_Inequality_Equal_Condition`

These files are intentionally not registered in `TheoremLibrary`.

## Tests Run

```bash
python tests/analyze_missing_models.py
python tests/analyze_model_failures.py
python -m pytest tests/test_theorem_missing_models.py
python -m pytest tests/test_theorem_*.py
git diff --check
git status --short
```

Result: pytest theorem tests passed (`4 passed`). The two analysis scripts ran
successfully and are documented in the audit report. `git diff --check`
reported no whitespace errors.

## Known Risks

- New models are not reachable through `TheoremLibrary` until an integration
  patch imports and registers them.
- Model 38 assumes a known tangent point from `x0/y0`, `x_0/y_0`, or a named
  coordinate referenced by `TangentAt(...)` or `PointOnCurve(...)`.
- Model 27 infers ellipse focus axis from existing relations or denominator
  comparison. Ambiguous symbolic denominator cases default to x-axis.
- Model 64 depends on explicit AM-GM/basic-inequality context and terms; it
  will not infer arbitrary equality conditions from free-form optimization
  text.
- Existing `apply()` ownership of `state.applied_models` is inconsistent with
  `TheoremLibrary.apply_model()`, which can duplicate model IDs after
  registration. I did not change that shared behavior.

## Integration Notes

Recommended integration registration IDs:

```text
18, 27, 38, 64
```

Suggested patch shape for `src/theorems/theorem_library.py`:

```python
from .models.model_018 import EllipseLatusRectum
from .models.model_027 import EllipseDirectrix
from .models.model_038 import EllipseTangentLine
from .models.model_064 import BasicInequalityEqualCondition

self.register_model(EllipseLatusRectum())
self.register_model(EllipseDirectrix())
self.register_model(EllipseTangentLine())
self.register_model(BasicInequalityEqualCondition())
```

Do this only in the integration thread, after checking for concurrent changes.

Next candidates from the audit:

```text
39 Parabola_Tangent_Line
45 Point_Difference_Method_Ellipse
58 Triangle_Area_Coordinate
67 Discriminant_Intersect_Condition
71 Equal_Area_Method
```

The highest-impact failure signal is not missing IDs alone. Stored max-step
failures show repeated no-op selection of broad models, especially IDs 62, 1,
0, 53, 56, 47, 13, and 43. That should be handled by a later integration or
search/selector worker, not this file-bounded theorem audit worker.

## Forbidden Files

No forbidden files were edited. In particular, I did not modify:

- `src/theorems/theorem_library.py`
- `src/reasoning/`
- `src/selector/`
- `tex/icml2026.tex`
- checkpoints or raw data files
