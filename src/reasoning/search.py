"""
Standalone search strategies for AAAI2027 ablation experiments.

This module intentionally does not modify the main reasoning loop.  It provides
selector-compatible strategy objects that can be passed to ReasoningEngine for
independent experiments.
"""

from __future__ import annotations

import copy
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set, Tuple

import torch

from src.reasoning.entropy_estimator import EntropyEstimator


DEFAULT_LAMBDA_WEIGHTS: Tuple[float, float, float] = (0.6, 0.3, 0.1)
SEARCH_ABLATION_SCHEMA_VERSION = "egr_search_strategy_v1"


@dataclass(frozen=True)
class SearchStrategyConfig:
    """Run-level configuration shared by all search strategies."""

    name: str
    top_k: int = 10
    lambda_weights: Tuple[float, float, float] = DEFAULT_LAMBDA_WEIGHTS
    avoid_repeated_models: bool = True
    checkpoint_path: Optional[str] = None
    max_steps: Optional[int] = None
    seed: Optional[int] = None
    sample_size: Optional[int] = None

    def to_metadata(self) -> Dict[str, Any]:
        return {
            "schema_version": SEARCH_ABLATION_SCHEMA_VERSION,
            "strategy": self.name,
            "top_k": self.top_k,
            "lambda_weights": list(self.lambda_weights),
            "avoid_repeated_models": self.avoid_repeated_models,
            "checkpoint_path": self.checkpoint_path,
            "max_steps": self.max_steps,
            "seed": self.seed,
            "sample_size": self.sample_size,
        }


@dataclass
class SearchCandidate:
    """Serializable candidate-level record for selector traces."""

    rank: int
    model_id: int
    model_name: str
    model_available: bool
    excluded: bool = False
    can_apply: Optional[bool] = None
    probability: Optional[float] = None
    score: Optional[float] = None
    p_y_x: Optional[float] = None
    info_gain: Optional[float] = None
    h_y_x: Optional[float] = None
    h_current: Optional[float] = None
    h_next: Optional[float] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "rank": self.rank,
            "model_id": self.model_id,
            "model_name": self.model_name,
            "model_available": self.model_available,
            "excluded": self.excluded,
            "can_apply": self.can_apply,
            "probability": self.probability,
            "score": self.score,
            "p_y_x": self.p_y_x,
            "info_gain": self.info_gain,
            "h_y_x": self.h_y_x,
            "h_current": self.h_current,
            "h_next": self.h_next,
        }


@dataclass
class SearchDecision:
    """Strategy output with a ReasoningEngine-compatible view."""

    strategy: str
    selected_model: Optional[Any]
    selected_candidate: Optional[SearchCandidate]
    candidates: List[SearchCandidate] = field(default_factory=list)
    extra: Dict[str, Any] = field(default_factory=dict)

    def to_selection_info(self) -> Dict[str, Any]:
        info: Dict[str, Any] = {
            "strategy": self.strategy,
            "search_schema_version": SEARCH_ABLATION_SCHEMA_VERSION,
            "selected_model_id": (
                self.selected_candidate.model_id if self.selected_candidate else None
            ),
            "selected_rank": (
                self.selected_candidate.rank if self.selected_candidate else -1
            ),
            "candidates": [candidate.to_dict() for candidate in self.candidates],
            **self.extra,
        }

        if self.selected_candidate is not None:
            candidate = self.selected_candidate
            info["can_apply"] = candidate.can_apply
            info["model_available"] = candidate.model_available
            if candidate.probability is not None:
                info["predicted_confidence"] = candidate.probability
            if candidate.h_y_x is not None:
                info["prediction_entropy"] = candidate.h_y_x
            if candidate.info_gain is not None:
                info["info_gain"] = candidate.info_gain
            if candidate.score is not None:
                info["score"] = candidate.score
            if candidate.h_current is not None:
                info["h_current"] = candidate.h_current
            if candidate.h_next is not None:
                info["h_next"] = candidate.h_next

        return info


@dataclass
class SearchContext:
    """Inputs passed from the adapter to a search strategy."""

    symbolic_state: Any
    abstract_state: Any
    theorem_library: Any
    neural_network: Optional[Any] = None
    state_constructor: Optional[Any] = None
    entropy_estimator: Optional[EntropyEstimator] = None
    device: str = "cpu"
    top_k: int = 10
    lambda_weights: Tuple[float, float, float] = DEFAULT_LAMBDA_WEIGHTS
    excluded_models: Set[int] = field(default_factory=set)


class BaseSearchStrategy:
    """Base class for selector-compatible standalone strategies."""

    name = "base"
    uses_neural = False
    uses_rule_filter = False
    uses_info_gain = False

    def select(self, context: SearchContext) -> SearchDecision:
        raise NotImplementedError

    def metadata(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "uses_neural": self.uses_neural,
            "uses_rule_filter": self.uses_rule_filter,
            "uses_info_gain": self.uses_info_gain,
        }


class RuleOnlyStrategy(BaseSearchStrategy):
    """Fixed theorem-id order with can_apply filtering and no neural scores."""

    name = "rule_only"
    uses_rule_filter = True

    def select(self, context: SearchContext) -> SearchDecision:
        candidates: List[SearchCandidate] = []
        selected_model = None
        selected_candidate = None

        model_ids = context.theorem_library.get_available_models()
        for rank, model_id in enumerate(model_ids[: context.top_k], start=1):
            excluded = model_id in context.excluded_models
            model = context.theorem_library.get_model(model_id)
            can_apply = False
            if model is not None and not excluded:
                can_apply = _safe_can_apply(model, context.symbolic_state)

            candidate = SearchCandidate(
                rank=rank,
                model_id=model_id,
                model_name=_model_name(model, model_id),
                model_available=model is not None,
                excluded=excluded,
                can_apply=can_apply,
            )
            candidates.append(candidate)

            if selected_model is None and model is not None and can_apply and not excluded:
                selected_model = model
                selected_candidate = candidate

        return SearchDecision(
            strategy=self.name,
            selected_model=selected_model,
            selected_candidate=selected_candidate,
            candidates=candidates,
            extra={
                "top_k": context.top_k,
                "excluded_count": len(context.excluded_models),
            },
        )


class NeuralOnlyStrategy(BaseSearchStrategy):
    """P(Y|X) ranking without can_apply filtering or information gain."""

    name = "neural_only"
    uses_neural = True

    def select(self, context: SearchContext) -> SearchDecision:
        probs, prediction_entropy, top_ids, top_probs = _predict_top_k(context)
        candidates: List[SearchCandidate] = []
        selected_model = None
        selected_candidate = None

        for rank, (model_id, probability) in enumerate(zip(top_ids, top_probs), start=1):
            excluded = model_id in context.excluded_models
            model = context.theorem_library.get_model(model_id)
            can_apply = (
                _safe_can_apply(model, context.symbolic_state)
                if model is not None and not excluded
                else False
            )
            candidate = SearchCandidate(
                rank=rank,
                model_id=model_id,
                model_name=_model_name(model, model_id),
                model_available=model is not None,
                excluded=excluded,
                can_apply=can_apply,
                probability=float(probability),
                p_y_x=float(probability),
                h_y_x=prediction_entropy,
            )
            candidates.append(candidate)

            if selected_model is None and model is not None and not excluded:
                selected_model = model
                selected_candidate = candidate

        return SearchDecision(
            strategy=self.name,
            selected_model=selected_model,
            selected_candidate=selected_candidate,
            candidates=candidates,
            extra={
                "top_k": context.top_k,
                "excluded_count": len(context.excluded_models),
                "prediction_entropy": prediction_entropy,
                "uses_can_apply_filter": False,
            },
        )


class NeuralRuleStrategy(BaseSearchStrategy):
    """P(Y|X) ranking with can_apply filtering."""

    name = "neural_rule"
    uses_neural = True
    uses_rule_filter = True

    def select(self, context: SearchContext) -> SearchDecision:
        probs, prediction_entropy, top_ids, top_probs = _predict_top_k(context)
        candidates: List[SearchCandidate] = []
        selected_model = None
        selected_candidate = None

        for rank, (model_id, probability) in enumerate(zip(top_ids, top_probs), start=1):
            excluded = model_id in context.excluded_models
            model = context.theorem_library.get_model(model_id)
            can_apply = (
                _safe_can_apply(model, context.symbolic_state)
                if model is not None and not excluded
                else False
            )
            candidate = SearchCandidate(
                rank=rank,
                model_id=model_id,
                model_name=_model_name(model, model_id),
                model_available=model is not None,
                excluded=excluded,
                can_apply=can_apply,
                probability=float(probability),
                p_y_x=float(probability),
                h_y_x=prediction_entropy,
            )
            candidates.append(candidate)

            if selected_model is None and model is not None and can_apply and not excluded:
                selected_model = model
                selected_candidate = candidate

        return SearchDecision(
            strategy=self.name,
            selected_model=selected_model,
            selected_candidate=selected_candidate,
            candidates=candidates,
            extra={
                "top_k": context.top_k,
                "excluded_count": len(context.excluded_models),
                "prediction_entropy": prediction_entropy,
                "uses_can_apply_filter": True,
            },
        )


class FullEGRStrategy(BaseSearchStrategy):
    """P(Y|X) + InfoGain - H(Y|X) over rule-valid top-k candidates."""

    name = "full_egr"
    uses_neural = True
    uses_rule_filter = True
    uses_info_gain = True

    def select(self, context: SearchContext) -> SearchDecision:
        if context.state_constructor is None:
            raise ValueError("full_egr requires a state_constructor")
        if context.entropy_estimator is None:
            raise ValueError("full_egr requires an entropy_estimator")

        probs, prediction_entropy, top_ids, top_probs = _predict_top_k(context)
        lambda_1, lambda_2, lambda_3 = context.lambda_weights
        h_current = context.entropy_estimator.estimate(context.abstract_state)
        candidates: List[SearchCandidate] = []

        for rank, (model_id, probability) in enumerate(zip(top_ids, top_probs), start=1):
            excluded = model_id in context.excluded_models
            model = context.theorem_library.get_model(model_id)
            can_apply = (
                _safe_can_apply(model, context.symbolic_state)
                if model is not None and not excluded
                else False
            )
            info_gain = 0.0
            h_next = None
            score = None

            if model is not None and can_apply and not excluded:
                info_gain, h_next = _simulate_info_gain(
                    model=model,
                    context=context,
                    h_current=h_current,
                )
                score = (
                    lambda_1 * float(probability)
                    + lambda_2 * info_gain
                    - lambda_3 * prediction_entropy
                )

            candidates.append(
                SearchCandidate(
                    rank=rank,
                    model_id=model_id,
                    model_name=_model_name(model, model_id),
                    model_available=model is not None,
                    excluded=excluded,
                    can_apply=can_apply,
                    probability=float(probability),
                    p_y_x=float(probability),
                    info_gain=info_gain if can_apply and not excluded else None,
                    h_y_x=prediction_entropy,
                    h_current=h_current,
                    h_next=h_next,
                    score=score,
                )
            )

        scored_candidates = [candidate for candidate in candidates if candidate.score is not None]
        selected_candidate = (
            max(scored_candidates, key=lambda candidate: candidate.score)
            if scored_candidates
            else None
        )
        selected_model = (
            context.theorem_library.get_model(selected_candidate.model_id)
            if selected_candidate is not None
            else None
        )

        return SearchDecision(
            strategy=self.name,
            selected_model=selected_model,
            selected_candidate=selected_candidate,
            candidates=candidates,
            extra={
                "top_k": context.top_k,
                "excluded_count": len(context.excluded_models),
                "prediction_entropy": prediction_entropy,
                "h_current": h_current,
                "lambda_weights": list(context.lambda_weights),
                "uses_can_apply_filter": True,
            },
        )


class SearchSelectorAdapter:
    """
    Adapter exposing SearchStrategy through ReasoningEngine's select() protocol.

    ReasoningEngine only requires a select(symbolic_state, abstract_state, ...)
    method that returns (model, selection_info).  This adapter keeps search
    experiments independent from src/reasoning/model_selector.py.
    """

    def __init__(
        self,
        strategy: str | BaseSearchStrategy,
        theorem_library: Any,
        neural_network: Optional[Any] = None,
        state_constructor: Optional[Any] = None,
        device: str = "cpu",
        top_k: int = 10,
        lambda_weights: Tuple[float, float, float] = DEFAULT_LAMBDA_WEIGHTS,
        entropy_estimator: Optional[EntropyEstimator] = None,
        avoid_repeated_models: bool = True,
    ):
        self.strategy = build_search_strategy(strategy)
        self.theorem_library = theorem_library
        self.neural_network = neural_network
        self.state_constructor = state_constructor
        self.device = device
        self.top_k = top_k
        self.lambda_weights = lambda_weights
        self.entropy_estimator = entropy_estimator or EntropyEstimator(mode="heuristic")
        self.avoid_repeated_models = avoid_repeated_models

        if self.strategy.uses_neural and self.neural_network is None:
            raise ValueError(f"{self.strategy.name} requires a neural_network")

    @property
    def strategy_name(self) -> str:
        return self.strategy.name

    def metadata(self) -> Dict[str, Any]:
        return {
            **self.strategy.metadata(),
            "top_k": self.top_k,
            "lambda_weights": list(self.lambda_weights),
            "avoid_repeated_models": self.avoid_repeated_models,
        }

    def select(
        self,
        symbolic_state: Any,
        abstract_state: Any,
        top_k: Optional[int] = None,
        excluded_models: Optional[Set[int]] = None,
    ) -> Tuple[Optional[Any], Dict[str, Any]]:
        excluded = set(excluded_models or set())
        if self.avoid_repeated_models:
            excluded.update(getattr(symbolic_state, "applied_models", []) or [])

        context = SearchContext(
            symbolic_state=symbolic_state,
            abstract_state=abstract_state,
            theorem_library=self.theorem_library,
            neural_network=self.neural_network,
            state_constructor=self.state_constructor,
            entropy_estimator=self.entropy_estimator,
            device=self.device,
            top_k=int(top_k or self.top_k),
            lambda_weights=self.lambda_weights,
            excluded_models=excluded,
        )
        decision = self.strategy.select(context)
        info = decision.to_selection_info()
        info.update(
            {
                "search_strategy_metadata": self.metadata(),
                "excluded_count": len(excluded),
            }
        )
        return decision.selected_model, info


def build_search_strategy(strategy: str | BaseSearchStrategy) -> BaseSearchStrategy:
    if isinstance(strategy, BaseSearchStrategy):
        return strategy

    normalized = normalize_strategy_name(strategy)
    mapping = {
        RuleOnlyStrategy.name: RuleOnlyStrategy,
        NeuralOnlyStrategy.name: NeuralOnlyStrategy,
        NeuralRuleStrategy.name: NeuralRuleStrategy,
        FullEGRStrategy.name: FullEGRStrategy,
    }
    try:
        return mapping[normalized]()
    except KeyError as exc:
        raise ValueError(f"Unknown search strategy: {strategy}") from exc


def normalize_strategy_name(strategy: str) -> str:
    aliases = {
        "rule": "rule_only",
        "rule-only": "rule_only",
        "rule_only": "rule_only",
        "neural": "neural_only",
        "neural-only": "neural_only",
        "neural_only": "neural_only",
        "neural+rule": "neural_rule",
        "neural-rule": "neural_rule",
        "neural_rule": "neural_rule",
        "full": "full_egr",
        "full-egr": "full_egr",
        "full_egr": "full_egr",
        "three_layer_entropy": "full_egr",
    }
    key = str(strategy).strip().lower()
    if key not in aliases:
        raise ValueError(f"Unknown search strategy: {strategy}")
    return aliases[key]


def default_ablation_strategies() -> List[str]:
    return ["rule_only", "neural_only", "neural_rule", "full_egr"]


def _predict_top_k(context: SearchContext) -> Tuple[torch.Tensor, float, List[int], List[float]]:
    if context.neural_network is None:
        raise ValueError("Neural strategy requires a neural_network")

    state_vector = torch.tensor(
        context.abstract_state.to_vector(),
        dtype=torch.float32,
        device=context.device,
    )
    with torch.no_grad():
        probs, _, entropy = context.neural_network.predict(state_vector)
        flat_probs = probs.detach().reshape(-1)
        k = max(1, min(int(context.top_k), int(flat_probs.numel())))
        top_k_probs, top_k_ids = context.neural_network.get_top_k(state_vector, k=k)

    return (
        flat_probs,
        float(entropy),
        [int(model_id) for model_id in top_k_ids.detach().cpu().reshape(-1).tolist()],
        [float(prob) for prob in top_k_probs.detach().cpu().reshape(-1).tolist()],
    )


def _simulate_info_gain(
    model: Any,
    context: SearchContext,
    h_current: float,
) -> Tuple[float, Optional[float]]:
    try:
        simulated_symbolic = copy.deepcopy(context.symbolic_state)
        apply_result = model.apply(simulated_symbolic)
        if apply_result is False:
            return 0.0, h_current
        simulated_abstract = context.state_constructor.update_abstract_state(
            simulated_symbolic,
            context.abstract_state,
        )
        h_next = context.entropy_estimator.estimate(simulated_abstract)
        return h_current - h_next, h_next
    except Exception:
        return 0.0, h_current


def _safe_can_apply(model: Any, symbolic_state: Any) -> bool:
    try:
        return bool(model.can_apply(symbolic_state))
    except Exception:
        return False


def _model_name(model: Optional[Any], model_id: int) -> str:
    if model is None:
        return f"Model_{model_id}"
    return str(getattr(model, "name", f"Model_{model_id}"))
