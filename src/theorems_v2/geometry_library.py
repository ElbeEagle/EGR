"""Fourth-stage library with constructed-geometry executors."""

from __future__ import annotations

from .complete_library import ModelCapability, SupportLevel
from .constructed_geometry_requirements import (
    constructed_geometry_requirement,
)
from .models.constructed_geometry import constructed_geometry_models
from .structured_library import StructuredTheoremLibraryV2


class GeometryTheoremLibraryV2(StructuredTheoremLibraryV2):
    def __init__(self):
        super().__init__()
        for model in constructed_geometry_models():
            requirement = constructed_geometry_requirement(model.model_id)
            setattr(model, "requirement", requirement)
            setattr(model, "executable", True)
            self.models[model.model_id] = model
            self.capabilities[model.model_id] = ModelCapability(
                requirement, SupportLevel.CONCRETE
            )
