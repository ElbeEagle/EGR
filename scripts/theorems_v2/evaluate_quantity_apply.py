"""Run the standard audit with canonical quantity closure."""

from __future__ import annotations

import evaluate_expanded_apply as evaluation

from src.theorems_v2.quantity_closure import QuantityApplicatorV2
from src.theorems_v2.quantity_library import QuantityTheoremLibraryV2
from src.theorems_v2.quantity_raw_adapter import QuantityRawFactAdapter


evaluation.ApplicatorV2 = QuantityApplicatorV2
evaluation.ExpandedTheoremLibraryV2 = QuantityTheoremLibraryV2
evaluation.ExpandedRawFactAdapter = QuantityRawFactAdapter


if __name__ == "__main__":
    evaluation.main()
