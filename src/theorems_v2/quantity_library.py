"""Fifth-stage library with canonical quantities."""

from __future__ import annotations

from .complete_library import ModelCapability, SupportLevel
from .geometry_library import GeometryTheoremLibraryV2
from .models.quantity_conics import quantity_conic_models
from .quantity_conic_requirements import quantity_conic_requirement


class QuantityTheoremLibraryV2(GeometryTheoremLibraryV2):
    def __init__(self):
        super().__init__()
        for model in quantity_conic_models():
            requirement = quantity_conic_requirement(model.model_id)
            setattr(model, "requirement", requirement)
            setattr(model, "executable", True)
            self.models[model.model_id] = model
            self.capabilities[model.model_id] = ModelCapability(
                requirement, SupportLevel.CONCRETE
            )
