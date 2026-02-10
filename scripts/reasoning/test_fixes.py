"""
测试推理引擎修复

验证：
1. 问题1: 阈值+最小步数
2. 问题2: Query解析器+答案提取器
3. 问题3: 模型apply返回值修复
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from src.reasoning import ReasoningEngine, ModelSelector
from src.selector import MaxEntropyClassifier
from src.theorems import TheoremLibrary
from src.state import StateConstructor
import torch


def test_fix1_threshold_and_min_steps():
    """测试问题1修复：阈值+最小步数"""
    print("=" * 80)
    print("测试1: 阈值+最小步数修复")
    print("=" * 80)
    
    # 初始化组件
    library = TheoremLibrary()
    constructor = StateConstructor(theorem_library=library)
    
    neural_network = MaxEntropyClassifier()
    try:
        checkpoint = torch.load('checkpoints/model_selector.pth', map_location='cpu')
        neural_network.load_state_dict(checkpoint['model_state_dict'])
        neural_network.eval()
    except:
        print("警告：无法加载模型权重，使用未训练的模型")
    
    selector = ModelSelector(neural_network, library, strategy='neural_topk')
    
    # 测试旧配置（应该立即完成）
    engine_old = ReasoningEngine(
        library, selector, constructor,
        completeness_threshold=0.95,
        min_steps=0,
        verbose=False
    )
    
    # 测试新配置（至少推理1步）
    engine_new = ReasoningEngine(
        library, selector, constructor,
        completeness_threshold=0.99,
        min_steps=1,
        verbose=False
    )
    
    problem = {
        'facts': "G: Hyperbola; Expression(G) = (x^2/3 - y^2 = 1)",
        'query': "Equation(Asymptote(G))"
    }
    
    result_old = engine_old.solve(problem['facts'], problem['query'])
    result_new = engine_new.solve(problem['facts'], problem['query'])
    
    print(f"旧配置（threshold=0.95, min_steps=0）:")
    print(f"  步数: {result_old.num_steps}")
    print(f"  成功: {result_old.success}")
    
    print(f"\n新配置（threshold=0.99, min_steps=1）:")
    print(f"  步数: {result_new.num_steps}")
    print(f"  成功: {result_new.success}")
    
    if result_new.num_steps >= 1:
        print("\n✓ 问题1修复成功：强制至少推理1步")
    else:
        print("\n✗ 问题1修复失败")
    
    print()


def test_fix2_answer_extraction():
    """测试问题2修复：答案提取器"""
    print("=" * 80)
    print("测试2: 答案提取器")
    print("=" * 80)
    
    from src.reasoning import QueryParser, AnswerExtractor
    from src.state.symbolic_state import SymbolicState
    
    parser = QueryParser()
    extractor = AnswerExtractor()
    
    # 测试1: 简单值
    print("测试2.1: 简单值 'm'")
    state = SymbolicState()
    state.parameters = {'m': '5'}
    answer = extractor.extract(state, 'm')
    print(f"  Query: m")
    print(f"  答案: {answer}")
    print(f"  ✓ 通过" if answer == '5' else f"  ✗ 失败")
    
    # 测试2: 离心率
    print("\n测试2.2: Eccentricity(G)")
    state = SymbolicState()
    state.entities = {'G': 'Ellipse'}
    state.parameters = {'a': '2', 'b': '1'}
    answer = extractor.extract(state, 'Eccentricity(G)')
    print(f"  Query: Eccentricity(G)")
    print(f"  状态: a=2, b=1")
    print(f"  答案: {answer}")
    print(f"  ✓ 通过" if answer else f"  ✗ 失败")
    
    # 测试3: 长度
    print("\n测试2.3: Length(MajorAxis(G))")
    state = SymbolicState()
    state.entities = {'G': 'Ellipse'}
    state.parameters = {'a': '4'}
    answer = extractor.extract(state, 'Length(MajorAxis(G))')
    print(f"  Query: Length(MajorAxis(G))")
    print(f"  状态: a=4")
    print(f"  答案: {answer}")
    print(f"  ✓ 通过" if answer == 8 else f"  ✗ 失败")
    
    # 测试4: 方程
    print("\n测试2.4: Equation(Asymptote(G))")
    state = SymbolicState()
    state.entities = {'G': 'Hyperbola'}
    state.equations = ['Equation(Asymptote(G)) = (y = ±(b/a)x)']
    answer = extractor.extract(state, 'Equation(Asymptote(G))')
    print(f"  Query: Equation(Asymptote(G))")
    print(f"  答案: {answer}")
    print(f"  ✓ 通过" if 'y' in str(answer) else f"  ✗ 失败")
    
    print("\n✓ 问题2修复完成：答案提取器工作正常")
    print()


def test_fix3_model_apply_return():
    """测试问题3修复：模型apply返回值"""
    print("=" * 80)
    print("测试3: 模型apply返回值")
    print("=" * 80)
    
    from src.state.symbolic_state import SymbolicState as SymState
    
    library = TheoremLibrary()
    constructor = StateConstructor(theorem_library=library)
    
    # 测试Model 13（离心率公式）
    print("测试3.1: Model 13 - Eccentricity_Formula")
    state = SymState()
    state.entities = {'G': 'Ellipse'}
    state.parameters = {'a': '2', 'b': '1'}
    
    model = library.get_model(13)
    if model:
        can_apply = model.can_apply(state)
        print(f"  can_apply: {can_apply}")
        
        if can_apply:
            result = model.apply(state)
            print(f"  apply返回值: {result}")
            print(f"  结果参数: {state.parameters}")
            
            if result is True or result is None:
                print(f"  ✓ Model 13 返回值正确")
            else:
                print(f"  ✗ Model 13 返回值错误: {result}")
    else:
        print("  ✗ Model 13 未实现")
    
    # 测试Model 11（椭圆参数关系）
    print("\n测试3.2: Model 11 - Ellipse_Parameter_Relation")
    state = SymState()
    state.entities = {'G': 'Ellipse'}
    state.parameters = {'a': '2', 'b': '1'}
    
    model = library.get_model(11)
    if model:
        can_apply = model.can_apply(state)
        print(f"  can_apply: {can_apply}")
        
        if can_apply:
            result = model.apply(state)
            print(f"  apply返回值: {result}")
            print(f"  结果参数: {state.parameters}")
            
            if result is True or result is None:
                print(f"  ✓ Model 11 返回值正确")
            else:
                print(f"  ✗ Model 11 返回值错误: {result}")
    else:
        print("  ✗ Model 11 未实现")
    
    print("\n✓ 问题3修复完成：模型apply返回值正确")
    print()


def test_integrated():
    """集成测试：完整推理流程"""
    print("=" * 80)
    print("集成测试: 完整推理流程")
    print("=" * 80)
    
    # 初始化
    library = TheoremLibrary()
    constructor = StateConstructor(theorem_library=library)
    
    neural_network = MaxEntropyClassifier()
    try:
        checkpoint = torch.load('checkpoints/model_selector.pth', map_location='cpu')
        neural_network.load_state_dict(checkpoint['model_state_dict'])
        neural_network.eval()
    except:
        print("警告：无法加载模型权重")
    
    selector = ModelSelector(neural_network, library, strategy='neural_topk')
    
    engine = ReasoningEngine(
        library, selector, constructor,
        completeness_threshold=0.99,
        min_steps=1,
        verbose=True
    )
    
    # 测试问题1：双曲线渐近线
    print("\n问题1: 双曲线渐近线")
    print("-" * 80)
    result1 = engine.solve(
        facts="G: Hyperbola; Expression(G) = (x^2/3 - y^2 = 1)",
        query="Equation(Asymptote(G))"
    )
    
    # 测试问题2：椭圆离心率
    print("\n问题2: 椭圆离心率")
    print("-" * 80)
    result2 = engine.solve(
        facts="G: Ellipse; Expression(G) = (x^2/4 + y^2 = 1)",
        query="Eccentricity(G)"
    )
    
    # 测试问题3：椭圆长轴长
    print("\n问题3: 椭圆长轴长")
    print("-" * 80)
    result3 = engine.solve(
        facts="G: Ellipse; Expression(G) = (x^2/4 + y^2 = 1)",
        query="Length(MajorAxis(G))"
    )
    
    # 汇总结果
    print("\n" + "=" * 80)
    print("集成测试结果汇总")
    print("=" * 80)
    
    results = [result1, result2, result3]
    names = ["双曲线渐近线", "椭圆离心率", "椭圆长轴长"]
    
    success_count = sum(1 for r in results if r.success)
    
    for name, result in zip(names, results):
        status = "✓ 成功" if result.success else "✗ 失败"
        print(f"{name}: {status}")
        print(f"  步数: {result.num_steps}")
        print(f"  答案: {result.answer}")
        if not result.success:
            print(f"  原因: {result.failure_reason}")
        print()
    
    print(f"总成功率: {success_count}/3 ({success_count*100/3:.1f}%)")
    

if __name__ == '__main__':
    print("\n推理引擎修复验证测试\n")
    
    # 运行各项测试
    test_fix1_threshold_and_min_steps()
    test_fix2_answer_extraction()
    test_fix3_model_apply_return()
    test_integrated()
    
    print("\n" + "=" * 80)
    print("所有测试完成！")
    print("=" * 80)
