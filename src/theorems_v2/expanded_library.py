"""Expanded v2 library including the second concrete executor batch."""

from __future__ import annotations

from .complete_library import (
    CompleteTheoremLibraryV2,
    ModelCapability,
    SupportLevel,
)
from .models.conic_properties import second_batch_models


class ExpandedTheoremLibraryV2(CompleteTheoremLibraryV2):
    def __init__(self):
        super().__init__()
        for model in second_batch_models():
            requirement = self.get_requirement(model.model_id)
            setattr(model, "requirement", requirement)
            setattr(model, "executable", True)
            self.models[model.model_id] = model
            self.capabilities[model.model_id] = ModelCapability(
                requirement, SupportLevel.CONCRETE
            )
