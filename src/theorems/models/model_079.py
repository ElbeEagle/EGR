"""
Model 79: Quadratic_Function_Maximum
二次函数最值

公式: f(x) = ax² + bx + c
- 当 a > 0 时，最小值 f(-b/2a) = (4ac - b²)/4a
- 当 a < 0 时，最大值 f(-b/2a) = (4ac - b²)/4a
"""

import re
from ..base_model import TheoremModel


class QuadraticFunctionMaximum(TheoremModel):
    """
    二次函数最值
    
    前置条件:
    - 存在二次函数
    - 或求最值问题
    
    输出:
    - 最值公式
    - 最值点 x = -b/2a
    - 最值 y = (4ac - b²)/4a
    
    示例:
    输入: f(x) = x² + 2x + 1
    输出: 最小值在 x = -1，最小值 = 0
    """
    
    def __init__(self):
        super().__init__(
            model_id=79,
            name="Quadratic_Function_Maximum",
            chinese_name="二次函数最值"
        )
    
    def can_apply(self, state) -> bool:
        """
        检查是否可应用
        
        条件:
        1. 存在二次函数或二次方程
        2. 或讨论最值、极值
        """
        # 条件1: 存在二次项
        has_quadratic = any(
            '^2' in eq for eq in state.equations
        )
        
        # 条件2: 讨论最值
        has_extremum = any(
            kw in rel for rel in state.geometric_relations
            for kw in ['Maximum', 'Minimum', 'Max', 'Min', 'Extremum', '最大', '最小', '最值', '极值']
        )
        
        # 条件3: 查询中涉及最值
        return has_quadratic or has_extremum
    
    def apply(self, state) -> None:
        """
        应用模型，求最值
        """
        # 添加二次函数最值公式
        state.geometric_relations.append("QuadraticFunction: f(x) = ax² + bx + c")
        state.geometric_relations.append("Vertex: x = -b/(2a)")
        state.geometric_relations.append("Extremum: f(-b/2a) = (4ac - b²)/(4a)")
        
        # 添加最值判断条件
        state.geometric_relations.append("If a > 0: Minimum at x = -b/(2a)")
        state.geometric_relations.append("If a < 0: Maximum at x = -b/(2a)")
        
        # 添加参数
        state.parameters['vertex_x'] = "-b/(2*a)"
        state.parameters['extremum_value'] = "(4*a*c - b^2)/(4*a)"
        
        # 记录已应用的模型
        state.applied_models.append(self.model_id)
