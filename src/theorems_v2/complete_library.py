"""Complete 80-model v2 registry with explicit support levels."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, Iterable, List, Mapping, Optional, Tuple

from .base import TheoremModelV2
from .catalog import THEOREM_CATALOG, TheoremRequirement
from .expressions import ConservativeSolver
from .library import TheoremLibraryV2
from .schema import Derivation
from .state import InformationState


class SupportLevel(str, Enum):
    CONCRETE = "CONCRETE"
    SPECIFICATION_ONLY = "SPECIFICATION_ONLY"


@dataclass(frozen=True)
class ModelCapability:
    requirement: TheoremRequirement
    support_level: SupportLevel


class SpecificationOnlyTheoremV2(TheoremModelV2):
    """Non-executable model carrying a complete formal requirement entry."""

    executable = False

    def __init__(self, requirement: TheoremRequirement):
        self.requirement = requirement
        self.model_id = requirement.model_id
        self.name = f"{requirement.name}_V2_SPEC"

    def match(self, state: InformationState) -> List[Dict[str, Any]]:
        return []

    def derive(
        self,
        state: InformationState,
        binding: Dict[str, Any],
        solver: ConservativeSolver,
    ) -> Derivation:
        raise NotImplementedError(
            f"model {self.model_id} has a v2 specification but no concrete executor"
        )

    def inspect_requirements(
        self, state: InformationState
    ) -> Tuple[str, ...]:
        missing = []
        for type_name in self.requirement.required_types:
            if not any(
                symbol.type_name == type_name
                for symbol in state.symbols.values()
            ):
                missing.append(f"type:{type_name}")
        for predicate in self.requirement.required_predicates:
            if not state.find(predicate):
                missing.append(f"predicate:{predicate}")
        return tuple(missing)


class CompleteTheoremLibraryV2:
    """Expose all 80 models while preserving concrete/spec-only boundaries."""

    def __init__(self):
        concrete_library = TheoremLibraryV2()
        self.models: Dict[int, TheoremModelV2] = {}
        self.capabilities: Dict[int, ModelCapability] = {}
        for model_id in range(80):
            requirement = THEOREM_CATALOG[model_id]
            concrete = concrete_library.get_model(model_id)
            if concrete is not None:
                model = concrete
                level = SupportLevel.CONCRETE
                setattr(model, "requirement", requirement)
                setattr(model, "executable", True)
            else:
                model = SpecificationOnlyTheoremV2(requirement)
                level = SupportLevel.SPECIFICATION_ONLY
            self.models[model_id] = model
            self.capabilities[model_id] = ModelCapability(requirement, level)

    def get_model(self, model_id: int) -> Optional[TheoremModelV2]:
        return self.models.get(model_id)

    def get_requirement(self, model_id: int) -> Optional[TheoremRequirement]:
        capability = self.capabilities.get(model_id)
        return capability.requirement if capability else None

    def get_capability(self, model_id: int) -> Optional[ModelCapability]:
        return self.capabilities.get(model_id)

    def get_available_models(self) -> List[int]:
        return list(range(80))

    def get_executable_models(self) -> List[int]:
        return [
            model_id
            for model_id, capability in self.capabilities.items()
            if capability.support_level == SupportLevel.CONCRETE
        ]

    def specification_coverage(self) -> float:
        return len(self.capabilities) / 80.0

    def executable_coverage(self) -> float:
        return len(self.get_executable_models()) / 80.0

    def __len__(self) -> int:
        return len(self.models)
