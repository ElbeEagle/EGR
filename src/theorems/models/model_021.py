"""
Model 21: Hyperbola_Asymptote
双曲线渐近线

公式: y = ±(b/a)x
前提: 已知 a 和 b
"""

import re
from ..base_model import TheoremModel


class HyperbolaAsymptote(TheoremModel):
    """
    双曲线渐近线
    
    前置条件:
    - 实体包含 Hyperbola 类型
    - 参数中有 a 和 b
    
    输出:
    - equations: 渐近线方程 y = ±(b/a)x
    - geometric_relations: 渐近线关系
    
    示例:
    输入: a=2, b=m
    输出: Expression(Asymptote(G)) = (y = pm*(m/2)*x)
    """
    
    def __init__(self):
        super().__init__(
            model_id=21,
            name="Hyperbola_Asymptote",
            chinese_name="双曲线渐近线"
        )
    
    def propose_bound(self, state, action):
        import sympy as sp
        from src.solver.transition_primitives import (
            TransitionError, finite_real_solutions, hyperbola_parameters, line_slope,
        )
        from src.theorems.bound_application import Proposal, check_binding

        if action.mode != 'constrain_parameters':
            raise TransitionError('inapplicable', 'Bound slice supports inverse RM21 only')
        fact = check_binding(state, action)
        line = state.equations[action.line_equation_id]
        a_key, b_key = (action.curve, 'a_sq'), (action.curve, 'b_sq')
        if a_key not in state.properties or b_key not in state.properties:
            raise TransitionError('inapplicable', 'Missing RM5 parameter facts')
        x, y = state.symbols['x'], state.symbols['y']
        constraints = list(state.constraints.values())
        # Verify that stored properties still match the explicitly bound equation.
        a_sq, b_sq = hyperbola_parameters(fact.expression, x, y, constraints)
        for key, expected in ((a_key, a_sq), (b_key, b_sq)):
            if sp.simplify((state.properties[key]-expected).subs(state.values)) != 0:
                raise TransitionError('conflict', 'Parameters do not match bound equation')
        slope = line_slope(line.expression, x, y, constraints)
        relation = sp.cancel(slope**2 - b_sq/a_sq)
        reads = (fact.fact_id, line.fact_id, *state.constraints.keys(),
                 f'property:{action.curve}:a_sq', f'property:{action.curve}:b_sq')
        operations = [{'operation': 'line_slope', 'equation': line.fact_id, 'result': slope},
                      {'operation': 'asymptote_constraint', 'expression': relation}]
        if state.query in state.values:
            if sp.simplify(relation.subs(state.values)) != 0:
                raise TransitionError('conflict', 'Known answer violates asymptote relation')
            return Proposal(read_facts=reads, operations=operations)
        candidates = finite_real_solutions(relation.subs(state.values), state.query,
                                          [c.subs(state.values) for c in constraints], trace=operations)
        operations.append({'operation': 'solve_and_filter', 'target': state.query,
                           'candidates': candidates})
        if not candidates:
            raise TransitionError('conflict', 'No real solution satisfies the constraints')
        if len(candidates) != 1:
            # Expose all candidates without committing one arbitrary branch.
            return Proposal(read_facts=reads, operations=operations, candidates=candidates)
        return Proposal(values={state.query: candidates[0]}, read_facts=reads,
                        operations=operations, candidates=candidates)

    def can_apply(self, state) -> bool:
        """
        检查是否可应用
        
        条件:
        1. 存在 Hyperbola 实体
        2. 参数中有 a 和 b
        """
        # 条件1: 检查是否有双曲线实体
        has_hyperbola = any(
            entity_type.lower() == 'hyperbola'
            for entity_type in state.entities.values()
        )
        if not has_hyperbola:
            return False
        
        # 条件2: 检查是否有 a 和 b 参数
        if 'a' not in state.parameters or 'b' not in state.parameters:
            return False
        
        return True
    
    def apply(self, state) -> bool:
        """
        应用模型，添加渐近线方程
        """
        try:
            a_val = state.parameters['a']
            b_val = state.parameters['b']
        
            # 查找双曲线实体名称
            hyperbola_name = None
            for name, type_ in state.entities.items():
                if type_.lower() == 'hyperbola':
                    hyperbola_name = name
                    break
        
            if hyperbola_name is None:
                hyperbola_name = 'G'  # 默认名称
        
            # 构建渐近线方程
            # 格式: y = pm*(b/a)*x  其中pm表示±
            asymptote_eq = f"y = pm*({b_val}/{a_val})*x"
        
            # 添加到方程列表
            equation_str = f"Expression(Asymptote({hyperbola_name})) = ({asymptote_eq})"
            state.equations.append(equation_str)
        
            # 添加几何关系（便于人类阅读）
            state.geometric_relations.append(f"渐近线: y = ±({b_val}/{a_val})x")
        
            # 尝试简化渐近线斜率
            slope = self._simplify_fraction(b_val, a_val)
            if slope:
                state.geometric_relations.append(f"渐近线斜率: ±{slope}")
        
            # 记录已应用的模型
            state.applied_models.append(self.model_id)
    
            return True

        except Exception:
            return False
    def _simplify_fraction(self, numerator: str, denominator: str) -> str:
        """
        简化分数
        
        例如:
        - "m", "2" -> "m/2"
        - "4", "2" -> "2"
        """
        # 尝试数值简化
        try:
            num_val = float(numerator)
            den_val = float(denominator)
            result = num_val / den_val
            if result == int(result):
                return str(int(result))
            else:
                return f"{numerator}/{denominator}"
        except:
            # 符号形式
            if denominator == "1":
                return numerator
            else:
                return f"{numerator}/{denominator}"
