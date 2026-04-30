import torch

from src.reasoning.entropy_estimator import EntropyEstimator
from src.reasoning.search import (
    FullEGRStrategy,
    NeuralOnlyStrategy,
    NeuralRuleStrategy,
    RuleOnlyStrategy,
    SearchContext,
    SearchSelectorAdapter,
    default_ablation_strategies,
    normalize_strategy_name,
)
from src.state.abstract_state import AbstractState
from src.state.symbolic_state import SymbolicState


class DummyModel:
    def __init__(self, model_id, can_apply=True, completeness_boost=0.0):
        self.model_id = model_id
        self.name = f"Dummy_{model_id}"
        self._can_apply = can_apply
        self.completeness_boost = completeness_boost

    def can_apply(self, state):
        return self._can_apply

    def apply(self, state):
        state.parameters[f"m{self.model_id}"] = self.completeness_boost
        state.applied_models.append(self.model_id)
        return True


class DummyLibrary:
    def __init__(self, models):
        self.models = {model.model_id: model for model in models}

    def get_available_models(self):
        return sorted(self.models)

    def get_model(self, model_id):
        return self.models.get(model_id)


class DummyNetwork:
    def __init__(self, probs):
        self.probs = torch.tensor(probs, dtype=torch.float32)

    def predict(self, state_vector):
        entropy = -(self.probs * torch.log(self.probs + 1e-10)).sum().item()
        return self.probs, int(self.probs.argmax().item()), entropy

    def get_top_k(self, state_vector, k=5):
        return torch.topk(self.probs, k=k)


class DummyConstructor:
    def update_abstract_state(self, symbolic_state, old_abstract_state):
        state = AbstractState()
        state.completeness_score = old_abstract_state.completeness_score
        if symbolic_state.parameters:
            state.completeness_score += max(float(v) for v in symbolic_state.parameters.values())
        state.completeness_score = min(1.0, state.completeness_score)
        state.reasoning_depth = old_abstract_state.reasoning_depth + 1
        return state


def make_abstract_state(completeness=0.2):
    state = AbstractState()
    state.completeness_score = completeness
    state.reasoning_depth = 0
    return state


def make_context(strategy, models, probs=None, top_k=3):
    return SearchContext(
        symbolic_state=SymbolicState(),
        abstract_state=make_abstract_state(),
        theorem_library=DummyLibrary(models),
        neural_network=DummyNetwork(probs or [0.1, 0.7, 0.2]),
        state_constructor=DummyConstructor(),
        entropy_estimator=EntropyEstimator(mode="heuristic"),
        top_k=top_k,
        lambda_weights=(0.2, 1.0, 0.0),
    )


def test_rule_only_uses_fixed_order_and_can_apply_filter():
    context = make_context(
        RuleOnlyStrategy(),
        [DummyModel(0, can_apply=False), DummyModel(1, can_apply=True)],
        top_k=2,
    )

    decision = RuleOnlyStrategy().select(context)
    info = decision.to_selection_info()

    assert decision.selected_model.model_id == 1
    assert info["strategy"] == "rule_only"
    assert info["candidates"][0]["can_apply"] is False
    assert info["candidates"][1]["can_apply"] is True


def test_neural_only_does_not_filter_by_can_apply():
    context = make_context(
        NeuralOnlyStrategy(),
        [DummyModel(1, can_apply=False), DummyModel(2, can_apply=True)],
        probs=[0.05, 0.9, 0.05],
        top_k=2,
    )

    decision = NeuralOnlyStrategy().select(context)
    info = decision.to_selection_info()

    assert decision.selected_model.model_id == 1
    assert info["uses_can_apply_filter"] is False
    assert info["can_apply"] is False


def test_neural_rule_filters_by_can_apply():
    context = make_context(
        NeuralRuleStrategy(),
        [DummyModel(1, can_apply=False), DummyModel(2, can_apply=True)],
        probs=[0.01, 0.7, 0.29],
        top_k=2,
    )

    decision = NeuralRuleStrategy().select(context)

    assert decision.selected_model.model_id == 2
    assert decision.to_selection_info()["uses_can_apply_filter"] is True


def test_full_egr_records_entropy_and_info_gain_fields():
    context = make_context(
        FullEGRStrategy(),
        [
            DummyModel(1, can_apply=True, completeness_boost=0.05),
            DummyModel(2, can_apply=True, completeness_boost=0.5),
        ],
        probs=[0.01, 0.8, 0.19],
        top_k=2,
    )

    decision = FullEGRStrategy().select(context)
    info = decision.to_selection_info()

    assert decision.selected_model.model_id == 2
    assert info["strategy"] == "full_egr"
    assert info["info_gain"] > 0
    assert info["score"] is not None
    assert info["lambda_weights"] == [0.2, 1.0, 0.0]


def test_selector_adapter_combines_retry_and_applied_exclusions():
    symbolic_state = SymbolicState()
    symbolic_state.applied_models = [1]
    library = DummyLibrary([DummyModel(1, can_apply=True), DummyModel(2, can_apply=True)])
    adapter = SearchSelectorAdapter(
        strategy="neural_rule",
        theorem_library=library,
        neural_network=DummyNetwork([0.01, 0.7, 0.29]),
        state_constructor=DummyConstructor(),
        top_k=2,
    )

    model, info = adapter.select(
        symbolic_state=symbolic_state,
        abstract_state=make_abstract_state(),
        excluded_models=set(),
    )

    assert model.model_id == 2
    assert info["excluded_count"] == 1
    assert info["search_strategy_metadata"]["avoid_repeated_models"] is True


def test_strategy_aliases_and_default_ablation_order():
    assert normalize_strategy_name("Rule-only") == "rule_only"
    assert normalize_strategy_name("neural+rule") == "neural_rule"
    assert normalize_strategy_name("three_layer_entropy") == "full_egr"
    assert default_ablation_strategies() == [
        "rule_only",
        "neural_only",
        "neural_rule",
        "full_egr",
    ]
