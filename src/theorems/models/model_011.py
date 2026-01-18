"""
Model 11: Ellipse_Parameter_Relation
椭圆参数关系

公式: a^2 = b^2 + c^2
已知两个参数，求第三个
"""

import re
from ..base_model import TheoremModel


class EllipseParameterRelation(TheoremModel):
    """
    椭圆参数关系
    
    前置条件:
    - 实体包含 Ellipse 类型
    - a, b, c 中至少有两个已知
    
    输出:
    - parameters: 缺失的参数 (a, b, 或 c)
    - geometric_relations: a^2 = b^2 + c^2
    
    示例:
    输入: a=2, b=sqrt(3)
    输出: c=1
    """
    
    def __init__(self):
        super().__init__(
            model_id=11,
            name="Ellipse_Parameter_Relation",
            chinese_name="椭圆参数关系"
        )
    
    def can_apply(self, state) -> bool:
        """
        检查是否可应用（放宽条件）
        
        条件:
        1. 存在 Ellipse 实体
        2. a, b, c 中至少有一个已知（放宽）
        """
        # 条件1: 检查是否有椭圆实体
        has_ellipse = any(
            entity_type.lower() == 'ellipse'
            for entity_type in state.entities.values()
        )
        if not has_ellipse:
            return False
        
        # 条件2: 检查参数（放宽至至少一个）
        params = state.parameters
        known_count = 0
        if 'a' in params or 'a^2' in params:
            known_count += 1
        if 'b' in params or 'b^2' in params:
            known_count += 1
        if 'c' in params or 'c^2' in params:
            known_count += 1
        
        # 至少有一个参数就可以尝试
        return known_count >= 1
    
    def apply(self, state) -> None:
        """
        应用模型，计算缺失的参数
        """
        params = state.parameters
        
        # 获取已知参数
        a_val = params.get('a')
        b_val = params.get('b')
        c_val = params.get('c')
        
        # 情况1: 已知a和b，求c
        # c^2 = a^2 - b^2
        if a_val and b_val and not c_val:
            c_expr = f"sqrt({a_val}^2 - {b_val}^2)"
            
            # 尝试数值计算
            try:
                a_num = self._eval_expr(a_val)
                b_num = self._eval_expr(b_val)
                c_num_sq = a_num**2 - b_num**2
                if c_num_sq >= 0:
                    c_num = c_num_sq ** 0.5
                    if c_num == int(c_num):
                        params['c'] = str(int(c_num))
                    else:
                        params['c'] = f"sqrt({int(c_num_sq)})"
                else:
                    params['c'] = c_expr
            except:
                params['c'] = c_expr
            
            state.geometric_relations.append(f"c^2 = {a_val}^2 - {b_val}^2")
        
        # 情况2: 已知a和c，求b
        # b^2 = a^2 - c^2
        elif a_val and c_val and not b_val:
            b_expr = f"sqrt({a_val}^2 - {c_val}^2)"
            
            try:
                a_num = self._eval_expr(a_val)
                c_num = self._eval_expr(c_val)
                b_num_sq = a_num**2 - c_num**2
                if b_num_sq >= 0:
                    b_num = b_num_sq ** 0.5
                    if b_num == int(b_num):
                        params['b'] = str(int(b_num))
                    else:
                        params['b'] = f"sqrt({int(b_num_sq)})"
                else:
                    params['b'] = b_expr
            except:
                params['b'] = b_expr
            
            state.geometric_relations.append(f"b^2 = {a_val}^2 - {c_val}^2")
        
        # 情况3: 已知b和c，求a
        # a^2 = b^2 + c^2
        elif b_val and c_val and not a_val:
            a_expr = f"sqrt({b_val}^2 + {c_val}^2)"
            
            try:
                b_num = self._eval_expr(b_val)
                c_num = self._eval_expr(c_val)
                a_num_sq = b_num**2 + c_num**2
                a_num = a_num_sq ** 0.5
                if a_num == int(a_num):
                    params['a'] = str(int(a_num))
                else:
                    params['a'] = f"sqrt({int(a_num_sq)})"
            except:
                params['a'] = a_expr
            
            state.geometric_relations.append(f"a^2 = {b_val}^2 + {c_val}^2")
        
        # 记录已应用的模型
        state.applied_models.append(self.model_id)
    
    def _eval_expr(self, expr: str) -> float:
        """
        计算表达式的数值
        
        支持：
        - 数字: "2", "3.5"
        - 平方根: "sqrt(5)"
        """
        expr = str(expr).strip()
        
        # 纯数字
        try:
            return float(expr)
        except:
            pass
        
        # sqrt形式
        match = re.match(r'sqrt\((\d+(?:\.\d+)?)\)', expr)
        if match:
            num = float(match.group(1))
            return num ** 0.5
        
        raise ValueError(f"Cannot evaluate: {expr}")
