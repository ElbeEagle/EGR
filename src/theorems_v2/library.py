"""Registry for the separate v2 theorem implementation."""

from __future__ import annotations

from typing import Dict, Iterable, List, Optional

from .base import TheoremModelV2
from .models import (
    CircleStandardEquationV2,
    EccentricityFormulaV2,
    EllipseDefinitionV2,
    HyperbolaAsymptoteV2,
    HyperbolaDefinitionV2,
    ParabolaDefinitionV2,
    ParabolaDirectrixV2,
    ParameterRelationV2,
    standard_equation_models,
)


class TheoremLibraryV2:
    """High-frequency v2 registry; does not alter the legacy library."""

    def __init__(self, models: Optional[Iterable[TheoremModelV2]] = None):
        self.models: Dict[int, TheoremModelV2] = {}
        for model in models or self._default_models():
            self.register(model)

    @staticmethod
    def _default_models() -> List[TheoremModelV2]:
        return [
            EllipseDefinitionV2(),
            HyperbolaDefinitionV2(),
            ParabolaDefinitionV2(),
            *standard_equation_models(),
            ParameterRelationV2(11, "Ellipse"),
            ParameterRelationV2(12, "Hyperbola"),
            EccentricityFormulaV2(),
            HyperbolaAsymptoteV2(),
            ParabolaDirectrixV2(),
            CircleStandardEquationV2(),
        ]

    def register(self, model: TheoremModelV2) -> None:
        if model.model_id in self.models:
            raise ValueError(f"duplicate v2 model id: {model.model_id}")
        self.models[model.model_id] = model

    def get_model(self, model_id: int) -> Optional[TheoremModelV2]:
        return self.models.get(model_id)

    def get_available_models(self) -> List[int]:
        return sorted(self.models)

    def __len__(self) -> int:
        return len(self.models)
