"""
定理库 - 定义每个模型的输入输出和状态转换规则

关键设计：
1. 每个模型定义为状态转换函数
2. 输入：当前状态 + 模型参数
3. 输出：新状态（增量）
"""

from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from src.state_abstractor import SymbolicState, AbstractState
import re
import json


@dataclass
class TheoremModel:
    """
    定理模型定义
    
    每个模型包含：
    - 前置条件：应用该模型需要满足的条件
    - 输出：应用模型后会新增什么信息
    - 状态转换函数：如何更新状态
    """
    id: int
    name: str
    description: str
    category: str
    
    # 前置条件（需要哪些信息才能应用该模型）
    preconditions: List[str]
    
    # 输出信息（应用该模型后会得到什么新信息）
    outputs: List[str]
    
    # 状态转换函数
    transform_func: callable
    
    def can_apply(self, symbolic_state: SymbolicState) -> bool:
        """
        检查是否可以应用该模型
        
        Args:
            symbolic_state: 当前符号状态
        
        Returns:
            bool: 是否满足前置条件
        """
        # 这里应该检查symbolic_state是否包含所有preconditions
        # 简化实现：总是返回True（实际应该根据preconditions检查）
        return True
    
    def apply(self, symbolic_state: SymbolicState) -> SymbolicState:
        """
        应用模型，返回新的符号状态
        
        Args:
            symbolic_state: 当前符号状态
        
        Returns:
            新的符号状态（包含模型输出的信息）
        """
        # 深拷贝当前状态
        new_state = symbolic_state.copy()
        
        # 调用转换函数，更新状态
        self.transform_func(new_state)
        
        return new_state


class TheoremLibrary:
    """
    定理库：包含所有80个模型的定义
    """
    
    def __init__(self):
        self.models: Dict[int, TheoremModel] = {}
        self._build_library()
    
    def _build_library(self):
        """构建定理库"""
        
        # ===== 模型0: 椭圆定义 =====
        self.models[0] = TheoremModel(
            id=0,
            name="Ellipse_Definition",
            description="椭圆定义: |PF₁| + |PF₂| = 2a",
            category="曲线定义",
            preconditions=[
                "有椭圆",
                "有两个焦点F₁和F₂",
                "有椭圆上的点P"
            ],
            outputs=[
                "Distance(P, F1) + Distance(P, F2) = 2*a"
            ],
            transform_func=self._transform_ellipse_definition
        )
        
        # ===== 模型1: 双曲线定义 =====
        self.models[1] = TheoremModel(
            id=1,
            name="Hyperbola_Definition",
            description="双曲线定义: ||PF₁| - |PF₂|| = 2a",
            category="曲线定义",
            preconditions=[
                "有双曲线",
                "有两个焦点F₁和F₂",
                "有双曲线上的点P"
            ],
            outputs=[
                "Abs(Distance(P, F1) - Distance(P, F2)) = 2*a"
            ],
            transform_func=self._transform_hyperbola_definition
        )
        
        # ===== 模型5: 双曲线标准方程（焦点在x轴）=====
        self.models[5] = TheoremModel(
            id=5,
            name="Hyperbola_Equation_Standard_X",
            description="双曲线标准方程: x²/a² - y²/b² = 1",
            category="标准方程",
            preconditions=[
                "有双曲线",
                "有标准方程 x²/a² - y²/b² = 1"
            ],
            outputs=[
                "参数a和b的值",
                "焦点在x轴"
            ],
            transform_func=self._transform_hyperbola_standard_x
        )
        
        # ===== 模型11: 椭圆参数关系 =====
        self.models[11] = TheoremModel(
            id=11,
            name="Ellipse_Parameter_Relation",
            description="椭圆参数关系: a² = b² + c²",
            category="参数关系",
            preconditions=[
                "有椭圆",
                "已知a, b, c中的任意两个"
            ],
            outputs=[
                "第三个参数的值"
            ],
            transform_func=self._transform_ellipse_parameter_relation
        )
        
        # ===== 模型12: 双曲线参数关系 =====
        self.models[12] = TheoremModel(
            id=12,
            name="Hyperbola_Parameter_Relation",
            description="双曲线参数关系: c² = a² + b²",
            category="参数关系",
            preconditions=[
                "有双曲线",
                "已知a, b, c中的任意两个"
            ],
            outputs=[
                "第三个参数的值"
            ],
            transform_func=self._transform_hyperbola_parameter_relation
        )
        
        # ===== 模型13: 离心率公式 =====
        self.models[13] = TheoremModel(
            id=13,
            name="Eccentricity_Formula",
            description="离心率公式: e = c/a",
            category="参数关系",
            preconditions=[
                "已知c和a"
            ],
            outputs=[
                "离心率e的值"
            ],
            transform_func=self._transform_eccentricity_formula
        )
        
        # ===== 模型21: 双曲线渐近线 =====
        self.models[21] = TheoremModel(
            id=21,
            name="Hyperbola_Asymptote",
            description="双曲线渐近线: y = ±(b/a)x",
            category="渐近线",
            preconditions=[
                "有双曲线",
                "已知a和b"
            ],
            outputs=[
                "渐近线方程: y = ±(b/a)x"
            ],
            transform_func=self._transform_hyperbola_asymptote
        )
        
        # ===== 模型22: 焦点到渐近线距离 =====
        self.models[22] = TheoremModel(
            id=22,
            name="Hyperbola_Focus_To_Asymptote_Distance",
            description="焦点到渐近线距离 = b",
            category="渐近线",
            preconditions=[
                "有双曲线",
                "有焦点",
                "有渐近线"
            ],
            outputs=[
                "Distance(Focus, Asymptote) = b"
            ],
            transform_func=self._transform_hyperbola_focus_to_asymptote
        )
        
        # ... 继续添加其他模型 ...
        
        # 简化起见，我们先实现前面几个关键模型
        # 完整的80个模型会在后续补充
    
    # ========== 状态转换函数 ==========
    
    def _transform_ellipse_definition(self, state: SymbolicState):
        """应用椭圆定义"""
        # 添加新的几何关系
        state.geometric_relations.append(
            "Distance(P, F1) + Distance(P, F2) = 2*a"
        )
    
    def _transform_hyperbola_definition(self, state: SymbolicState):
        """应用双曲线定义"""
        state.geometric_relations.append(
            "Abs(Distance(P, F1) - Distance(P, F2)) = 2*a"
        )
    
    def _transform_hyperbola_standard_x(self, state: SymbolicState):
        """
        应用双曲线标准方程（焦点在x轴）
        
        输入：Expression(G) = (x^2/A - y^2/B = 1)
        输出：a² = A, b² = B
        
        例如：x²/4 - y²/m² = 1
        → a² = 4, b² = m²
        → a = 2, b = m
        """
        # 从方程中提取参数
        for eq in state.equations:
            if 'x^2' in eq and '- y^2' in eq:
                # 解析形如 x^2/4 - y^2/m^2 = 1 的方程
                # 提取分母
                match = re.search(r'x\^2/([^\s\-]+).*y\^2/([^\s=]+)', eq)
                if match:
                    a_squared_str = match.group(1)
                    b_squared_str = match.group(2)
                    
                    # 添加参数信息
                    state.parameters['a^2'] = a_squared_str
                    state.parameters['b^2'] = b_squared_str
                    
                    # 如果是具体数值，计算出a和b
                    try:
                        a_squared = float(eval(a_squared_str))
                        state.parameters['a'] = f"sqrt({a_squared})"
                    except:
                        pass
                    
                    # 添加新的fact
                    state.geometric_relations.append(
                        f"a^2 = {a_squared_str}"
                    )
                    state.geometric_relations.append(
                        f"b^2 = {b_squared_str}"
                    )
                    
                    break
    
    def _transform_ellipse_parameter_relation(self, state: SymbolicState):
        """
        应用椭圆参数关系: a² = b² + c²
        
        如果已知a, b中的两个，可以求第三个
        """
        params = state.parameters
        
        # 情况1: 已知a和b，求c
        if 'a' in params and 'b' in params:
            a_val = params['a']
            b_val = params['b']
            params['c'] = f"sqrt({a_val}^2 - {b_val}^2)"
            state.geometric_relations.append(
                f"c = sqrt({a_val}^2 - {b_val}^2)"
            )
        
        # 情况2: 已知a和c，求b
        elif 'a' in params and 'c' in params:
            a_val = params['a']
            c_val = params['c']
            params['b'] = f"sqrt({a_val}^2 - {c_val}^2)"
            state.geometric_relations.append(
                f"b = sqrt({a_val}^2 - {c_val}^2)"
            )
        
        # 情况3: 已知b和c，求a
        elif 'b' in params and 'c' in params:
            b_val = params['b']
            c_val = params['c']
            params['a'] = f"sqrt({b_val}^2 + {c_val}^2)"
            state.geometric_relations.append(
                f"a = sqrt({b_val}^2 + {c_val}^2)"
            )
    
    def _transform_hyperbola_parameter_relation(self, state: SymbolicState):
        """
        应用双曲线参数关系: c² = a² + b²
        
        注意：与椭圆不同！
        """
        params = state.parameters
        
        # 情况1: 已知a和b，求c
        if 'a' in params and 'b' in params:
            a_val = params['a']
            b_val = params['b']
            params['c'] = f"sqrt({a_val}^2 + {b_val}^2)"
            state.geometric_relations.append(
                f"c = sqrt({a_val}^2 + {b_val}^2)"
            )
        
        # 情况2: 已知a和c，求b
        elif 'a' in params and 'c' in params:
            a_val = params['a']
            c_val = params['c']
            params['b'] = f"sqrt({c_val}^2 - {a_val}^2)"
            state.geometric_relations.append(
                f"b = sqrt({c_val}^2 - {a_val}^2)"
            )
        
        # 情况3: 已知b和c，求a
        elif 'b' in params and 'c' in params:
            b_val = params['b']
            c_val = params['c']
            params['a'] = f"sqrt({c_val}^2 - {b_val}^2)"
            state.geometric_relations.append(
                f"a = sqrt({c_val}^2 - {b_val}^2)"
            )
    
    def _transform_eccentricity_formula(self, state: SymbolicState):
        """应用离心率公式: e = c/a"""
        params = state.parameters
        
        if 'c' in params and 'a' in params:
            c_val = params['c']
            a_val = params['a']
            params['e'] = f"{c_val}/{a_val}"
            state.geometric_relations.append(
                f"e = {c_val}/{a_val}"
            )
    
    def _transform_hyperbola_asymptote(self, state: SymbolicState):
        """应用双曲线渐近线公式: y = ±(b/a)x"""
        params = state.parameters
        
        if 'a' in params and 'b' in params:
            a_val = params['a']
            b_val = params['b']
            
            # 添加渐近线方程
            asymptote_eq = f"y = pm*({b_val}/{a_val})*x"
            state.equations.append(
                f"Expression(Asymptote(G)) = ({asymptote_eq})"
            )
            state.geometric_relations.append(
                f"渐近线方程: y = ±({b_val}/{a_val})x"
            )
    
    def _transform_hyperbola_focus_to_asymptote(self, state: SymbolicState):
        """应用焦点到渐近线距离公式: d = b"""
        # 如果已知焦点到渐近线的距离，可以得到b
        # 或者，如果已知b，可以验证距离
        
        state.geometric_relations.append(
            "Distance(Focus, Asymptote) = b"
        )
    
    def get_model(self, model_id: int) -> Optional[TheoremModel]:
        """获取指定ID的模型"""
        return self.models.get(model_id)
    
    def apply_model_sequence(
        self, 
        initial_state: SymbolicState, 
        model_ids: List[int]
    ) -> List[SymbolicState]:
        """
        应用一系列模型，返回每一步的状态
        
        Args:
            initial_state: 初始状态
            model_ids: 模型ID列表
        
        Returns:
            状态列表 [S0, S1, S2, ..., Sn]
        """
        states = [initial_state]
        current_state = initial_state
        
        for model_id in model_ids:
            model = self.get_model(model_id)
            if model is None:
                print(f"Warning: Model {model_id} not found")
                continue
            
            # 应用模型
            new_state = model.apply(current_state)
            states.append(new_state)
            current_state = new_state
        
        return states


# ========== 使用示例 ==========

def test_theorem_library():
    """测试定理库"""
    from src.state_abstractor import StateAbstractor
    
    library = TheoremLibrary()
    abstractor = StateAbstractor()
    
    # 示例：id=2的题目
    fact_expressions = (
        "G: Hyperbola;m: Number;m>0;"
        "Expression(G) = (x^2/4 - y^2/m^2 = 1);"
        "Expression(OneOf(Asymptote(G))) = (5*x - 2*y = 0)"
    )
    query_expressions = "m"
    model_ids = [5, 21]  # 应用模型5和21
    
    # 解析初始状态
    _, initial_state = abstractor.abstract_from_facts(fact_expressions, query_expressions)
    
    print("=" * 60)
    print("测试：模型序列应用")
    print("=" * 60)
    print(f"初始状态S0:")
    print(f"  实体: {initial_state.entities}")
    print(f"  方程: {initial_state.equations}")
    print(f"  参数: {initial_state.parameters}")
    print()
    
    # 应用模型序列
    states = library.apply_model_sequence(initial_state, model_ids)
    
    for i, state in enumerate(states[1:], 1):
        print(f"状态S{i} (应用模型{model_ids[i-1]}后):")
        print(f"  参数: {state.parameters}")
        print(f"  新增关系: {state.geometric_relations[-2:]}")  # 显示最新的2个关系
        print()


if __name__ == "__main__":
    test_theorem_library()
