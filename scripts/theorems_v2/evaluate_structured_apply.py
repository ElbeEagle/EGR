"""Run the standard apply audit with the structured third-stage stack."""

from __future__ import annotations

import evaluate_expanded_apply as evaluation

from src.theorems_v2.structured_library import StructuredTheoremLibraryV2
from src.theorems_v2.structured_raw_adapter import StructuredRawFactAdapter


evaluation.ExpandedTheoremLibraryV2 = StructuredTheoremLibraryV2
evaluation.ExpandedRawFactAdapter = StructuredRawFactAdapter


if __name__ == "__main__":
    evaluation.main()
