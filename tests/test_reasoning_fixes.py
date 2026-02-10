"""
推理引擎修复验证测试

测试内容：
1. 问题1修复：阈值+最小步数（不再立即完成）
2. 问题2修复：答案提取器（8种查询类型）
3. 问题3修复：模型apply返回值+排除重复
4. 集成测试：完整推理流程

运行方式：
    python tests/test_reasoning_fixes.py
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.state.symbolic_state import SymbolicState
from src.reasoning import QueryParser, AnswerExtractor


def test_query_parser():
    """测试Query解析器"""
    print("测试: QueryParser")
    parser = QueryParser()
    
    # 简单值
    p = parser.parse("m")
    assert p.operation == 'Value' and p.target == 'm', f"Failed: {p}"
    
    # 单层函数
    p = parser.parse("Eccentricity(G)")
    assert p.operation == 'Eccentricity' and p.target == 'G', f"Failed: {p}"
    
    # 嵌套函数
    p = parser.parse("Length(MajorAxis(G))")
    assert p.operation == 'Length' and p.nested_operation == 'MajorAxis', f"Failed: {p}"
    
    p = parser.parse("Equation(Asymptote(G))")
    assert p.operation == 'Equation' and p.nested_operation == 'Asymptote', f"Failed: {p}"
    
    print("  ✓ QueryParser 全部通过")


def test_answer_extractor():
    """测试答案提取器"""
    print("测试: AnswerExtractor")
    extractor = AnswerExtractor()
    
    # 1. 简单值
    state = SymbolicState()
    state.parameters = {'m': '5'}
    assert extractor.extract(state, 'm') == '5', "简单值提取失败"
    
    # 2. 长度（长轴长 = 2a）
    state = SymbolicState()
    state.entities = {'G': 'Ellipse'}
    state.parameters = {'a': '4'}
    assert extractor.extract(state, 'Length(MajorAxis(G))') == 8, "长轴长提取失败"
    
    # 3. 长度（虚轴长 = 2b）
    state = SymbolicState()
    state.entities = {'G': 'Hyperbola'}
    state.parameters = {'b': '3'}
    result = extractor.extract(state, 'Length(ImageinaryAxis(G))')
    assert result == 6, f"虚轴长提取失败: {result}"
    
    # 4. 离心率
    state = SymbolicState()
    state.entities = {'G': 'Ellipse'}
    state.parameters = {'a': '2', 'b': '1'}
    result = extractor.extract(state, 'Eccentricity(G)')
    assert isinstance(result, (int, float)), f"离心率类型错误: {type(result)}"
    
    # 5. 方程提取
    state = SymbolicState()
    state.equations = ['Equation(Asymptote(G)) = (y = ±x)']
    result = extractor.extract(state, 'Equation(Asymptote(G))')
    assert 'y' in str(result), f"方程提取失败: {result}"
    
    # 6. 坐标提取
    state = SymbolicState()
    state.coordinates = {'A': ('1', '2')}
    result = extractor.extract(state, 'Coordinate(A)')
    assert result == ('1', '2'), f"坐标提取失败: {result}"
    
    print("  ✓ AnswerExtractor 全部通过")


def test_model_apply_returns():
    """测试模型apply返回bool"""
    print("测试: Model apply返回值")
    from src.theorems import TheoremLibrary
    
    library = TheoremLibrary()
    
    # 测试Model 13
    state = SymbolicState()
    state.entities = {'G': 'Ellipse'}
    state.parameters = {'a': '2', 'b': '1'}
    
    model = library.get_model(13)
    assert model is not None, "Model 13 不存在"
    result = model.apply(state)
    assert result is True, f"Model 13 返回 {result}，期望 True"
    assert 'e' in state.parameters, "Model 13 未设置 e 参数"
    
    # 测试Model 11
    state = SymbolicState()
    state.entities = {'G': 'Ellipse'}
    state.parameters = {'a': '2', 'b': '1'}
    
    model = library.get_model(11)
    assert model is not None, "Model 11 不存在"
    result = model.apply(state)
    assert result is True, f"Model 11 返回 {result}，期望 True"
    assert 'c' in state.parameters, "Model 11 未计算 c 参数"
    
    print("  ✓ Model apply返回值 全部通过")


def test_reasoning_engine_integration():
    """集成测试：推理引擎"""
    print("测试: ReasoningEngine 集成")
    from src.reasoning import ReasoningEngine, ModelSelector
    from src.selector import MaxEntropyClassifier
    from src.theorems import TheoremLibrary
    from src.state import StateConstructor
    import torch
    
    library = TheoremLibrary()
    constructor = StateConstructor(theorem_library=library)
    
    neural_network = MaxEntropyClassifier()
    try:
        checkpoint = torch.load('checkpoints/model_selector.pth', map_location='cpu')
        neural_network.load_state_dict(checkpoint['model_state_dict'])
    except Exception:
        print("  ⚠ 无法加载模型权重，使用未训练模型")
    neural_network.eval()
    
    selector = ModelSelector(neural_network, library, strategy='neural_topk')
    engine = ReasoningEngine(
        library, selector, constructor,
        completeness_threshold=0.99,
        min_steps=1,
        verbose=False
    )
    
    # 测试3个问题
    problems = [
        ("G: Hyperbola; Expression(G) = (x^2/3 - y^2 = 1)", "Equation(Asymptote(G))"),
        ("G: Ellipse; Expression(G) = (x^2/4 + y^2 = 1)", "Eccentricity(G)"),
        ("G: Ellipse; Expression(G) = (x^2/4 + y^2 = 1)", "Length(MajorAxis(G))"),
    ]
    
    success_count = 0
    for facts, query in problems:
        result = engine.solve(facts, query)
        if result.success:
            success_count += 1
        # 确保至少推理了1步
        assert result.num_steps >= 1 or not result.success, \
            f"min_steps未生效: {query}, steps={result.num_steps}"
    
    print(f"  成功率: {success_count}/{len(problems)}")
    assert success_count >= 2, f"成功率太低: {success_count}/3"
    print("  ✓ ReasoningEngine 集成测试通过")


if __name__ == '__main__':
    print("=" * 60)
    print("推理引擎修复验证测试")
    print("=" * 60)
    
    test_query_parser()
    test_answer_extractor()
    test_model_apply_returns()
    test_reasoning_engine_integration()
    
    print("=" * 60)
    print("✓ 全部测试通过！")
    print("=" * 60)
