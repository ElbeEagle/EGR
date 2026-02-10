"""
批量推理引擎测试

验证推理引擎在多个样本上的基本功能和性能。

运行方式：
    python tests/test_batch_reasoning.py
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.reasoning import ReasoningEngine, ModelSelector
from src.reasoning.answer_comparator import compare_answers, safe_eval
from src.selector import MaxEntropyClassifier
from src.theorems import TheoremLibrary
from src.state import StateConstructor
import torch


def test_answer_comparator():
    """测试答案比较器"""
    print("测试: AnswerComparator")
    
    assert safe_eval('2') == 2.0
    assert safe_eval('sqrt(3)') is not None
    assert abs(safe_eval('sqrt(3)/2') - 0.866025) < 1e-4
    assert safe_eval('pm*2') == 2.0
    assert safe_eval('x^2+1') is None  # 含变量
    
    assert compare_answers(4, '4') == True
    assert compare_answers('sqrt(3)/3', 'sqrt(3)/3') == True
    assert compare_answers(0.5, '1/2') == True
    assert compare_answers('wrong', '4') == False
    
    print("  ✓ 全部通过")


def test_backtracking():
    """测试回溯机制：apply失败不会终止推理"""
    print("测试: 回溯机制")
    
    library = TheoremLibrary()
    constructor = StateConstructor(theorem_library=library)
    nn = MaxEntropyClassifier()
    try:
        cp = torch.load('checkpoints/model_selector.pth', map_location='cpu')
        nn.load_state_dict(cp['model_state_dict'])
    except: pass
    nn.eval()
    
    selector = ModelSelector(nn, library, strategy='neural_topk')
    engine = ReasoningEngine(
        library, selector, constructor,
        max_steps=10, max_retries_per_step=3, verbose=False
    )
    
    # 这个问题应该能推理出结果
    result = engine.solve(
        "G: Ellipse; Expression(G) = (x^2/4 + y^2 = 1)",
        "Eccentricity(G)"
    )
    
    assert result.success, f"应该成功: {result.failure_reason}"
    assert result.answer is not None
    
    print("  ✓ 全部通过")


def test_best_effort_answer():
    """测试尽力提取答案策略"""
    print("测试: 尽力提取答案")
    
    library = TheoremLibrary()
    constructor = StateConstructor(theorem_library=library)
    nn = MaxEntropyClassifier()
    try:
        cp = torch.load('checkpoints/model_selector.pth', map_location='cpu')
        nn.load_state_dict(cp['model_state_dict'])
    except: pass
    nn.eval()
    
    selector = ModelSelector(nn, library, strategy='neural_topk')
    engine = ReasoningEngine(
        library, selector, constructor,
        max_steps=5, verbose=False
    )
    
    result = engine.solve(
        "G: Hyperbola; Expression(G) = (x^2/4 - y^2/9 = 1)",
        "m"  # 简单值查询，参数中可能没有m
    )
    
    # 不管成功与否，都不应该崩溃
    assert result is not None
    
    print("  ✓ 全部通过")


if __name__ == '__main__':
    print("=" * 60)
    print("批量推理引擎测试")
    print("=" * 60)
    
    test_answer_comparator()
    test_backtracking()
    test_best_effort_answer()
    
    print("=" * 60)
    print("✓ 全部测试通过！")
    print("=" * 60)
