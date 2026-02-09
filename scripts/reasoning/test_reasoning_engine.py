#!/usr/bin/env python3
"""
推理引擎测试脚本

测试基础推理引擎在简单问题上的表现。
"""

import sys
from pathlib import Path
import torch

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.reasoning import ReasoningEngine, ModelSelector
from src.theorems import TheoremLibrary
from src.state import StateConstructor
from src.selector import MaxEntropyClassifier


def load_neural_network(model_path: str, device: str = 'cpu') -> MaxEntropyClassifier:
    """加载训练好的神经网络"""
    model = MaxEntropyClassifier()
    checkpoint = torch.load(model_path, map_location=device)
    model.load_state_dict(checkpoint['model_state_dict'])
    model.eval()
    return model


def test_simple_problem():
    """测试简单问题"""
    print("=" * 80)
    print("测试1: 简单双曲线问题")
    print("=" * 80)
    print()
    
    # 初始化组件
    print("初始化组件...")
    library = TheoremLibrary()
    constructor = StateConstructor(theorem_library=library)
    
    # 加载神经网络
    model_path = project_root / 'checkpoints' / 'model_selector.pth'
    neural_network = load_neural_network(str(model_path))
    print(f"✓ 神经网络已加载: {model_path}")
    
    # 创建模型选择器
    selector = ModelSelector(
        neural_network=neural_network,
        theorem_library=library,
        strategy='neural_top1'  # 使用Top-1策略
    )
    print("✓ 模型选择器已创建")
    
    # 创建推理引擎
    engine = ReasoningEngine(
        theorem_library=library,
        model_selector=selector,
        state_constructor=constructor,
        max_steps=10,
        completeness_threshold=0.90,
        verbose=True
    )
    print("✓ 推理引擎已创建")
    print()
    
    # 测试问题
    facts = "G: Hyperbola; Expression(G) = (x^2/3 - y^2 = 1)"
    query = "Equation(Asymptote(G))"
    
    # 求解
    result = engine.solve(facts=facts, query=query)
    
    # 分析结果
    print()
    print("=" * 80)
    print("结果分析")
    print("=" * 80)
    print(f"成功: {result.success}")
    print(f"步数: {result.num_steps}")
    print(f"耗时: {result.elapsed_time:.2f}秒")
    
    if result.model_names:
        print(f"模型序列: {' → '.join(result.model_names)}")
    
    if result.completeness_scores:
        print(f"完整度变化: {result.completeness_scores[0]:.3f} → {result.completeness_scores[-1]:.3f}")
    
    if not result.success:
        print(f"失败原因: {result.failure_reason}")
    
    return result


def test_topk_strategy():
    """测试Top-K策略"""
    print()
    print("=" * 80)
    print("测试2: Top-K策略")
    print("=" * 80)
    print()
    
    # 初始化
    library = TheoremLibrary()
    constructor = StateConstructor(theorem_library=library)
    model_path = project_root / 'checkpoints' / 'model_selector.pth'
    neural_network = load_neural_network(str(model_path))
    
    # 使用Top-K策略
    selector = ModelSelector(
        neural_network=neural_network,
        theorem_library=library,
        strategy='neural_topk'  # Top-K策略
    )
    
    engine = ReasoningEngine(
        theorem_library=library,
        model_selector=selector,
        state_constructor=constructor,
        max_steps=10,
        verbose=True
    )
    
    # 测试问题
    facts = "G: Ellipse; Expression(G) = (x^2/4 + y^2 = 1)"
    query = "Length(MajorAxis(G))"
    
    result = engine.solve(facts=facts, query=query)
    
    print()
    print(f"Top-K策略结果: {'成功' if result.success else '失败'}")
    if result.success:
        print(f"步数: {result.num_steps}")
        print(f"模型序列: {' → '.join(result.model_names)}")
    
    return result


def test_multiple_problems():
    """测试多个问题"""
    print()
    print("=" * 80)
    print("测试3: 批量测试")
    print("=" * 80)
    print()
    
    # 初始化
    library = TheoremLibrary()
    constructor = StateConstructor(theorem_library=library)
    model_path = project_root / 'checkpoints' / 'model_selector.pth'
    neural_network = load_neural_network(str(model_path))
    
    selector = ModelSelector(
        neural_network=neural_network,
        theorem_library=library,
        strategy='neural_topk'
    )
    
    engine = ReasoningEngine(
        theorem_library=library,
        model_selector=selector,
        state_constructor=constructor,
        max_steps=15,
        verbose=False  # 关闭详细输出
    )
    
    # 测试问题集
    test_cases = [
        {
            'name': '双曲线1',
            'facts': 'G: Hyperbola; Expression(G) = (x^2/3 - y^2 = 1)',
            'query': 'Equation(Asymptote(G))'
        },
        {
            'name': '椭圆1',
            'facts': 'G: Ellipse; Expression(G) = (x^2/4 + y^2 = 1)',
            'query': 'Length(MajorAxis(G))'
        },
        {
            'name': '抛物线1',
            'facts': 'G: Parabola; Expression(G) = (y^2 = 4*x)',
            'query': 'Coordinate(Focus(G))'
        },
    ]
    
    results = []
    for i, case in enumerate(test_cases, 1):
        print(f"问题 {i}/{len(test_cases)}: {case['name']}")
        result = engine.solve(facts=case['facts'], query=case['query'])
        results.append((case['name'], result))
        
        status = '✓ 成功' if result.success else '✗ 失败'
        print(f"  {status} (步数={result.num_steps}, 耗时={result.elapsed_time:.2f}s)")
    
    # 总结
    print()
    print("-" * 80)
    success_count = sum(1 for _, r in results if r.success)
    print(f"总计: {success_count}/{len(results)} 成功 ({success_count/len(results)*100:.1f}%)")
    
    return results


def main():
    """主函数"""
    print("推理引擎功能测试")
    print()
    
    try:
        # 测试1: 简单问题
        result1 = test_simple_problem()
        
        # 测试2: Top-K策略
        result2 = test_topk_strategy()
        
        # 测试3: 批量测试
        results3 = test_multiple_problems()
        
        print()
        print("=" * 80)
        print("✅ 所有测试完成!")
        print("=" * 80)
        
    except Exception as e:
        print()
        print("=" * 80)
        print(f"❌ 测试失败: {str(e)}")
        print("=" * 80)
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
