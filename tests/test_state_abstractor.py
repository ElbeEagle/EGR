"""
状态抽象器测试
"""

import sys
sys.path.insert(0, '/Users/ebeleagel/Documents/GitHub/EGR')

from src.state_abstractor import (
    StateAbstractor,
    CurveType,
    QueryType,
    create_state_abstractor
)


def test_basic_ellipse():
    """测试基础椭圆案例"""
    abstractor = create_state_abstractor()
    
    print("="*80)
    print("测试 1: 基础椭圆案例")
    print("="*80)
    
    # 样本：椭圆，有方程，求离心率
    facts = "G: Ellipse;Expression(G) = (x^2/2 + y^2/3 = 1)"
    query = "Eccentricity(G)"
    
    state = abstractor.abstract(facts, query)
    
    print(f"\n输入:")
    print(f"  Facts: {facts}")
    print(f"  Query: {query}")
    
    print(f"\n输出:")
    print(f"  曲线类型: {state.curve_type.value}")
    print(f"  查询类型: {state.query_type.value}")
    print(f"  有方程: {state.has_equation}")
    print(f"  已知参数: {state.known_params}")
    print(f"  信息完整度: {state.completeness:.2f}")
    print(f"  状态哈希: {state.state_hash}")
    
    # 验证
    assert state.curve_type == CurveType.ELLIPSE
    assert state.query_type == QueryType.ECCENTRICITY
    assert state.has_equation == True
    assert 'a' in state.known_params
    assert 'b' in state.known_params
    print(f"\n✅ 测试通过!")


def test_hyperbola_with_asymptote():
    """测试双曲线+渐近线案例"""
    abstractor = create_state_abstractor()
    
    print("\n" + "="*80)
    print("测试 2: 双曲线+渐近线案例")
    print("="*80)
    
    facts = "G: Hyperbola;m: Number;m>0;Expression(G) = (x^2/4 - y^2/m^2 = 1);Expression(OneOf(Asymptote(G))) = (5*x - 2*y = 0)"
    query = "m"
    
    state = abstractor.abstract(facts, query)
    
    print(f"\n输入:")
    print(f"  Facts: {facts[:100]}...")
    print(f"  Query: {query}")
    
    print(f"\n输出:")
    print(f"  曲线类型: {state.curve_type.value}")
    print(f"  查询类型: {state.query_type.value}")
    print(f"  有方程: {state.has_equation}")
    print(f"  有渐近线: {state.has_asymptote}")
    print(f"  已知参数: {state.known_params}")
    print(f"  约束条件: {state.constraints}")
    print(f"  信息完整度: {state.completeness:.2f}")
    print(f"  状态哈希: {state.state_hash}")
    
    # 验证
    assert state.curve_type == CurveType.HYPERBOLA
    assert state.query_type == QueryType.VALUE
    assert state.has_equation == True
    assert state.has_asymptote == True
    assert 'm' in state.known_params or 'a' in state.known_params
    print(f"\n✅ 测试通过!")


def test_parabola_with_point():
    """测试抛物线+点案例"""
    abstractor = create_state_abstractor()
    
    print("\n" + "="*80)
    print("测试 3: 抛物线+点案例")
    print("="*80)
    
    facts = "G: Parabola;Expression(G) = (x^2 = a*y);a: Number;A: Point;Coordinate(A) = (1, 1/4);PointOnCurve(A, G)"
    query = "Distance(A, Focus(G))"
    
    state = abstractor.abstract(facts, query)
    
    print(f"\n输入:")
    print(f"  Facts: {facts[:80]}...")
    print(f"  Query: {query}")
    
    print(f"\n输出:")
    print(f"  曲线类型: {state.curve_type.value}")
    print(f"  查询类型: {state.query_type.value}")
    print(f"  有方程: {state.has_equation}")
    print(f"  有焦点: {state.has_focus}")
    print(f"  点在曲线上: {state.has_point_on_curve}")
    print(f"  已知参数: {state.known_params}")
    print(f"  信息完整度: {state.completeness:.2f}")
    print(f"  状态哈希: {state.state_hash}")
    
    # 验证
    assert state.curve_type == CurveType.PARABOLA
    assert state.query_type == QueryType.DISTANCE
    assert state.has_equation == True
    # 注意：Focus在query中，不在facts中，所以has_focus=False是正确的
    assert state.has_point_on_curve == True
    print(f"\n✅ 测试通过!")


def test_complex_hyperbola():
    """测试复杂双曲线案例"""
    abstractor = create_state_abstractor()
    
    print("\n" + "="*80)
    print("测试 4: 复杂双曲线案例")
    print("="*80)
    
    facts = "C: Hyperbola;b: Number;a: Number;G: Circle;A: Point;B: Point;F: Point;a>0;b>0;Expression(C) = (-y^2/b^2 + x^2/a^2 = 1);OneOf(Focus(C)) = F;Center(G) = F;IsTangent(Asymptote(C), G);Intersection(G, C) = {A, B}"
    query = "Eccentricity(C)"
    
    state = abstractor.abstract(facts, query)
    
    print(f"\n输入:")
    print(f"  Facts: {facts[:100]}...")
    print(f"  Query: {query}")
    
    print(f"\n输出:")
    print(f"  曲线类型: {state.curve_type.value}")
    print(f"  查询类型: {state.query_type.value}")
    print(f"  有方程: {state.has_equation}")
    print(f"  有焦点: {state.has_focus}")
    print(f"  有渐近线: {state.has_asymptote}")
    print(f"  有切线: {state.has_tangent}")
    print(f"  有交点: {state.has_intersection}")
    print(f"  已知参数: {state.known_params}")
    print(f"  约束条件: {state.constraints}")
    print(f"  信息完整度: {state.completeness:.2f}")
    print(f"  状态哈希: {state.state_hash}")
    
    # 验证
    assert state.curve_type == CurveType.HYPERBOLA
    assert state.query_type == QueryType.ECCENTRICITY
    assert state.has_equation == True
    assert state.has_focus == True
    print(f"\n✅ 测试通过!")


def test_batch_abstraction():
    """测试批量抽象（覆盖率测试）"""
    import json
    
    abstractor = create_state_abstractor()
    
    print("\n" + "="*80)
    print("测试 5: 批量抽象（覆盖率测试）")
    print("="*80)
    
    # 加载前100个样本
    with open('/Users/ebeleagel/Documents/GitHub/EGR/Conic10K/conic10k/train.json', 'r') as f:
        data = json.load(f)
    
    sample_size = 100
    success_count = 0
    curve_type_counts = {}
    query_type_counts = {}
    
    print(f"\n处理 {sample_size} 个样本...")
    
    for item in data[:sample_size]:
        state = abstractor.abstract(
            item['fact_expressions'],
            item['query_expressions']
        )
        
        if state.curve_type != CurveType.UNKNOWN:
            success_count += 1
        
        # 统计
        curve_type_counts[state.curve_type.value] = \
            curve_type_counts.get(state.curve_type.value, 0) + 1
        query_type_counts[state.query_type.value] = \
            query_type_counts.get(state.query_type.value, 0) + 1
    
    coverage = success_count / sample_size * 100
    
    print(f"\n结果:")
    print(f"  成功抽象: {success_count}/{sample_size} ({coverage:.1f}%)")
    
    print(f"\n曲线类型分布:")
    for ctype, count in sorted(curve_type_counts.items()):
        print(f"    {ctype:<15} {count:>3} ({count/sample_size*100:.1f}%)")
    
    print(f"\n查询类型分布:")
    for qtype, count in sorted(query_type_counts.items()):
        print(f"    {qtype:<15} {count:>3} ({count/sample_size*100:.1f}%)")
    
    # 统计信息
    stats = abstractor.get_statistics()
    print(f"\n抽象器统计:")
    print(f"  总处理数: {stats['total_abstracted']}")
    print(f"  失败数: {stats['failed_count']}")
    print(f"  成功率: {stats['success_rate']*100:.1f}%")
    
    # 验证覆盖率
    assert coverage >= 95.0, f"覆盖率 {coverage:.1f}% 低于目标 95%"
    print(f"\n✅ 覆盖率测试通过! ({coverage:.1f}% >= 95%)")


def test_completeness_estimation():
    """测试完整度估计"""
    abstractor = create_state_abstractor()
    
    print("\n" + "="*80)
    print("测试 6: 完整度估计")
    print("="*80)
    
    test_cases = [
        {
            'name': '仅有曲线类型',
            'facts': 'G: Ellipse',
            'query': 'Eccentricity(G)',
            'expected_range': (0.0, 0.2)
        },
        {
            'name': '有方程',
            'facts': 'G: Ellipse;Expression(G) = (x^2/4 + y^2/3 = 1)',
            'query': 'Eccentricity(G)',
            'expected_range': (0.5, 0.8)
        },
        {
            'name': '有方程+焦点',
            'facts': 'G: Ellipse;Expression(G) = (x^2/4 + y^2/3 = 1);Focus(G) = {F1, F2}',
            'query': 'Eccentricity(G)',
            'expected_range': (0.7, 1.0)
        },
    ]
    
    for tc in test_cases:
        state = abstractor.abstract(tc['facts'], tc['query'])
        completeness = state.completeness
        
        print(f"\n【{tc['name']}】")
        print(f"  完整度: {completeness:.2f}")
        print(f"  预期范围: {tc['expected_range']}")
        
        assert tc['expected_range'][0] <= completeness <= tc['expected_range'][1], \
            f"完整度 {completeness} 不在预期范围 {tc['expected_range']}"
        print(f"  ✅ 通过")
    
    print(f"\n✅ 完整度估计测试通过!")


def run_all_tests():
    """运行所有测试"""
    test_basic_ellipse()
    test_hyperbola_with_asymptote()
    test_parabola_with_point()
    test_complex_hyperbola()
    test_completeness_estimation()
    test_batch_abstraction()
    
    print("\n" + "="*80)
    print("🎉 所有测试完成!")
    print("="*80)


if __name__ == '__main__':
    run_all_tests()

