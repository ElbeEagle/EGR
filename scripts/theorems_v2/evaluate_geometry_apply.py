"""Run the standard audit with constructed-geometry closure enabled."""

from __future__ import annotations

import evaluate_expanded_apply as evaluation

from src.theorems_v2.geometry_closure import GeometryApplicatorV2
from src.theorems_v2.geometry_library import GeometryTheoremLibraryV2
from src.theorems_v2.geometry_raw_adapter import GeometryRawFactAdapter


evaluation.ApplicatorV2 = GeometryApplicatorV2
evaluation.ExpandedTheoremLibraryV2 = GeometryTheoremLibraryV2
evaluation.ExpandedRawFactAdapter = GeometryRawFactAdapter


if __name__ == "__main__":
    evaluation.main()
