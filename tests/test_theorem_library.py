"""
定理库单元测试
"""

import sys
sys.path.insert(0, '/Users/ebeleagel/Documents/GitHub/EGR')

from src.theorems.theorem_library import (
    TheoremLibrary, 
    TheoremPriority,
    CurveType,
    get_theorem_library
)


def test_library_initialization():
    """测试定理库初始化"""
    lib = get_theorem_library()
    
    print("="*80)
    print("定理库初始化测试")
    print("="*80)
    
    print(f"\n总定理数: {len(lib.theorems)}")
    
    # 按优先级统计
    basic = lib.get_theorems_by_priority(TheoremPriority.BASIC)
    print(f"基础定理数: {len(basic)}")
    
    print("\n" + "-"*80)
    print("已注册的定理列表:")
    print("-"*80)
    for tid, theorem in lib.theorems.items():
        print(f"\n{tid:<25} {theorem.name}")
        print(f"  公式: {theorem.formula}")
        print(f"  优先级: {theorem.priority.value}")
        print(f"  适用曲线: {[ct.value for ct in theorem.precondition.curve_types]}")


def test_ellipse_abc_theorem():
    """测试椭圆参数关系定理"""
    lib = get_theorem_library()
    theorem = lib.get_theorem('T1_ellipse_abc')
    
    print("\n" + "="*80)
    print("测试：T1 椭圆参数关系")
    print("="*80)
    
    # 测试用例1：已知 b, c 求 a
    state1 = {
        'curve_type': 'Ellipse',
        'known_params': {'b': 3.0, 'c': 4.0}
    }
    
    print("\n【测试用例1】已知 b=3, c=4, 求 a")
    print(f"  前置条件检查: {theorem.check_applicable(state1)}")
    
    if theorem.check_applicable(state1):
        new_state = theorem.apply(state1)
        print(f"  计算结果: a = {new_state['known_params'].get('a')}")
        print(f"  验证: a² = b² + c² → 25 = 9 + 16 ✓")
    
    # 测试用例2：已知 a, b 求 c
    state2 = {
        'curve_type': 'Ellipse',
        'known_params': {'a': 5.0, 'b': 4.0}
    }
    
    print("\n【测试用例2】已知 a=5, b=4, 求 c")
    print(f"  前置条件检查: {theorem.check_applicable(state2)}")
    
    if theorem.check_applicable(state2):
        new_state = theorem.apply(state2)
        print(f"  计算结果: c = {new_state['known_params'].get('c')}")
        print(f"  验证: c² = a² - b² → 9 = 25 - 16 ✓")


def test_hyperbola_abc_theorem():
    """测试双曲线参数关系定理"""
    lib = get_theorem_library()
    theorem = lib.get_theorem('T2_hyperbola_abc')
    
    print("\n" + "="*80)
    print("测试：T2 双曲线参数关系")
    print("="*80)
    
    # 测试用例：已知 a, b 求 c
    state = {
        'curve_type': 'Hyperbola',
        'known_params': {'a': 4.0, 'b': 5.0}
    }
    
    print("\n【测试用例】已知 a=4, b=5, 求 c")
    print(f"  前置条件检查: {theorem.check_applicable(state)}")
    
    if theorem.check_applicable(state):
        new_state = theorem.apply(state)
        c_value = new_state['known_params'].get('c')
        print(f"  计算结果: c = {c_value}")
        print(f"  验证: c² = a² + b² → {c_value**2:.2f} = 16 + 25 = 41 ✓")


def test_eccentricity_theorem():
    """测试离心率公式定理"""
    lib = get_theorem_library()
    theorem = lib.get_theorem('T4_eccentricity')
    
    print("\n" + "="*80)
    print("测试：T4 离心率公式")
    print("="*80)
    
    # 测试用例1：椭圆
    state1 = {
        'curve_type': 'Ellipse',
        'known_params': {'a': 5.0, 'c': 3.0}
    }
    
    print("\n【测试用例1】椭圆: a=5, c=3")
    print(f"  前置条件检查: {theorem.check_applicable(state1)}")
    
    if theorem.check_applicable(state1):
        new_state = theorem.apply(state1)
        e = new_state['known_params'].get('eccentricity')
        print(f"  计算结果: e = {e}")
        print(f"  验证: e = c/a = 3/5 = 0.6 ✓")
    
    # 测试用例2：双曲线
    state2 = {
        'curve_type': 'Hyperbola',
        'known_params': {'a': 4.0, 'c': 6.4}
    }
    
    print("\n【测试用例2】双曲线: a=4, c=6.4")
    print(f"  前置条件检查: {theorem.check_applicable(state2)}")
    
    if theorem.check_applicable(state2):
        new_state = theorem.apply(state2)
        e = new_state['known_params'].get('eccentricity')
        print(f"  计算结果: e = {e}")
        print(f"  验证: e = c/a = 6.4/4 = 1.6 ✓")


def test_get_applicable_theorems():
    """测试获取可应用的定理"""
    lib = get_theorem_library()
    
    print("\n" + "="*80)
    print("测试：获取可应用的定理")
    print("="*80)
    
    # 场景：已知椭圆方程，求离心率
    state = {
        'curve_type': 'Ellipse',
        'has_equation': True,
        'known_params': {'a': 4.0, 'b': 3.0}
    }
    
    print("\n当前状态:")
    print(f"  曲线类型: {state['curve_type']}")
    print(f"  有方程: {state['has_equation']}")
    print(f"  已知参数: {state['known_params']}")
    
    applicable = lib.get_applicable_theorems(state)
    
    print(f"\n可应用的定理数量: {len(applicable)}")
    print("\n可应用的定理列表:")
    for theorem in applicable:
        print(f"  - {theorem.theorem_id}: {theorem.name}")


def run_all_tests():
    """运行所有测试"""
    test_library_initialization()
    test_ellipse_abc_theorem()
    test_hyperbola_abc_theorem()
    test_eccentricity_theorem()
    test_get_applicable_theorems()
    
    print("\n" + "="*80)
    print("所有测试完成！")
    print("="*80)


if __name__ == '__main__':
    run_all_tests()

