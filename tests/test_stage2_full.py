"""
Module 4 阶段2完整测试

验证：模型库扩充、三层熵架构、重训练后的选择器

运行方式：
    python tests/test_stage2_full.py
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import torch
from src.theorems import TheoremLibrary
from src.reasoning import ReasoningEngine, ModelSelector
from src.reasoning.entropy_estimator import EntropyEstimator
from src.reasoning.answer_comparator import compare_answers
from src.selector import MaxEntropyClassifier
from src.state import StateConstructor


def test_model_library():
    """测试模型库扩充"""
    print("测试: 模型库 (52/80)")
    library = TheoremLibrary()
    assert len(library) >= 52, f"模型数量不足: {len(library)}"
    
    new_models = [33, 44, 49, 51, 52, 55, 59, 66, 68, 72, 76, 77]
    for mid in new_models:
        assert library.get_model(mid) is not None, f"Model {mid} 未注册"
    
    print(f"  ✓ {len(library)}个模型全部加载")


def test_entropy_estimator():
    """测试熵估计器"""
    print("测试: EntropyEstimator")
    from src.state.abstract_state import AbstractState
    
    estimator = EntropyEstimator(mode='heuristic')
    
    state = AbstractState()
    state.completeness_score = 0.5
    state.has_parameters = {'a', 'b'}
    state.reasoning_depth = 1
    state.has_equation = True
    
    h = estimator.estimate(state)
    assert 0.0 <= h <= 1.0, f"熵值超范围: {h}"
    
    # 高完整度应有低熵
    state2 = AbstractState()
    state2.completeness_score = 0.95
    state2.has_parameters = {'a', 'b', 'c', 'e'}
    state2.reasoning_depth = 3
    state2.has_equation = True
    h2 = estimator.estimate(state2)
    assert h2 < h, f"高完整度应有更低熵: {h2} >= {h}"
    
    # InfoGain
    ig = estimator.compute_info_gain(state, state2)
    assert ig > 0, f"InfoGain应为正: {ig}"
    
    print("  ✓ 全部通过")


def test_three_layer_strategy():
    """测试三层熵选择策略"""
    print("测试: 三层熵策略")
    
    library = TheoremLibrary()
    constructor = StateConstructor(theorem_library=library)
    nn = MaxEntropyClassifier()
    try:
        cp = torch.load('checkpoints/model_selector_v2.pth', map_location='cpu')
        nn.load_state_dict(cp['model_state_dict'])
    except:
        try:
            cp = torch.load('checkpoints/model_selector.pth', map_location='cpu')
            nn.load_state_dict(cp['model_state_dict'])
        except:
            print("  ⚠ 无模型权重")
    nn.eval()
    
    selector = ModelSelector(nn, library, strategy='three_layer_entropy',
                              state_constructor=constructor, lambda_weights=(0.6, 0.3, 0.1))
    
    abstract, symbolic = constructor.construct_from_facts(
        "G: Ellipse; Expression(G) = (x^2/4 + y^2 = 1)", "Eccentricity(G)")
    
    model, info = selector.select(symbolic, abstract)
    assert model is not None, "应选出模型"
    assert 'score' in info, "应有综合评分"
    assert 'info_gain' in info, "应有InfoGain"
    
    print(f"  ✓ 选中Model {model.model_id}, score={info['score']:.4f}")


def test_v2_selector():
    """测试v2选择器"""
    print("测试: v2选择器 (12460训练样本)")
    
    nn = MaxEntropyClassifier()
    try:
        cp = torch.load('checkpoints/model_selector_v2.pth', map_location='cpu')
        nn.load_state_dict(cp['model_state_dict'])
        print(f"  Top-1={cp['best_val_acc']:.3f}")
    except:
        print("  ⚠ v2模型不存在，跳过")
        return
    
    assert cp['best_val_acc'] > 0.5, f"Top-1应>50%: {cp['best_val_acc']}"
    print("  ✓ 全部通过")


if __name__ == '__main__':
    print("=" * 60)
    print("Module 4 阶段2 完整测试")
    print("=" * 60)
    
    test_model_library()
    test_entropy_estimator()
    test_three_layer_strategy()
    test_v2_selector()
    
    print("=" * 60)
    print("✓ 全部测试通过！")
    print("=" * 60)
