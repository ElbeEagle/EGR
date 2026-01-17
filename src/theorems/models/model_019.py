"""
Model 19: Hyperbola_Latus_Rectum
双曲线通径（过焦点垂直于实轴的弦长）

公式: 通径 = 2b²/a
"""

from ..base_model import TheoremModel


class HyperbolaLatusRectum(TheoremModel):
    """
    双曲线通径
    
    前置条件:
    - 实体包含 Hyperbola 类型
    - 已知参数 a 和 b
    
    输出:
    - parameters: 通径长度
    - geometric_relations: 通径公式
    
    示例:
    输入: a=2, b=3
    输出: 通径 = 2*9/2 = 9
    """
    
    def __init__(self):
        super().__init__(
            model_id=19,
            name="Hyperbola_Latus_Rectum",
            chinese_name="双曲线通径"
        )
    
    def can_apply(self, state) -> bool:
        """
        检查是否可应用
        
        条件:
        1. 存在 Hyperbola 实体
        2. 已知参数 a 和 b
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
    
    def apply(self, state) -> None:
        """
        应用模型，计算通径
        """
        a_val = state.parameters['a']
        b_val = state.parameters['b']
        
        # 计算通径 = 2b²/a
        try:
            a_num = float(a_val)
            b_num = float(b_val)
            
            latus_rectum = 2 * b_num ** 2 / a_num
            
            if latus_rectum == int(latus_rectum):
                state.parameters['latus_rectum'] = str(int(latus_rectum))
            else:
                state.parameters['latus_rectum'] = str(latus_rectum)
            
            state.geometric_relations.append(f"通径 = 2*{b_val}²/{a_val} = {latus_rectum}")
            
        except:
            # 符号形式
            latus_expr = f"2*{b_val}^2/{a_val}"
            state.parameters['latus_rectum'] = latus_expr
            state.geometric_relations.append(f"通径 = {latus_expr}")
        
        # 记录已应用的模型
        state.applied_models.append(self.model_id)
