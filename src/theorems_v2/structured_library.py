"""Third-stage library with structured algebra and geometry executors."""

from __future__ import annotations

from .complete_library import ModelCapability, SupportLevel
from .expanded_library import ExpandedTheoremLibraryV2
from .models.structured_algebra import algebra_models
from .models.structured_geometry import analytic_geometry_models
from .structured_requirements import structured_requirement


class StructuredTheoremLibraryV2(ExpandedTheoremLibraryV2):
    def __init__(self):
        super().__init__()
        for model in (*algebra_models(), *analytic_geometry_models()):
            requirement = structured_requirement(model.model_id)
            setattr(model, "requirement", requirement)
            setattr(model, "executable", True)
            self.models[model.model_id] = model
            self.capabilities[model.model_id] = ModelCapability(
                requirement, SupportLevel.CONCRETE
            )
