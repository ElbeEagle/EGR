"""
Model 22: Hyperbola_Focus_To_Asymptote_Distance
双曲线焦点到渐近线的距离

公式: 距离 = b
"""

from ..base_model import TheoremModel


class HyperbolaFocusToAsymptoteDistance(TheoremModel):
    """
    双曲线焦点到渐近线的距离
    
    前置条件:
    - 实体包含 Hyperbola 类型
    - 已知参数 b
    
    输出:
    - geometric_relations: 焦点到渐近线距离 = b
    
    示例:
    输入: b=3
    输出: 焦点到渐近线距离 = 3
    """
    
    def __init__(self):
        super().__init__(
            model_id=22,
            name="Hyperbola_Focus_To_Asymptote_Distance",
            chinese_name="双曲线焦点到渐近线距离"
        )
    
    def can_apply(self, state) -> bool:
        """
        检查是否可应用
        
        条件:
        1. 存在 Hyperbola 实体
        2. 已知参数 b
        """
        # 条件1: 检查是否有双曲线实体
        has_hyperbola = any(
            entity_type.lower() == 'hyperbola'
            for entity_type in state.entities.values()
        )
        if not has_hyperbola:
            return False
        
        # 条件2: 检查是否有 b 参数
        if 'b' not in state.parameters:
            return False
        
        return True
    
    def apply(self, state) -> bool:
        """
        应用模型，添加焦点到渐近线距离
        """
        try:
            b_val = state.parameters['b']
        
            # 添加关系：焦点到渐近线距离 = b
            state.geometric_relations.append(f"焦点到渐近线距离 = {b_val}")
        
            # 如果有焦点坐标，可以添加更具体的信息
            if 'Focus' in state.coordinates or 'c' in state.parameters:
                state.geometric_relations.append("对于双曲线，焦点到其渐近线的距离恒等于b")
        
            # 记录已应用的模型
            state.applied_models.append(self.model_id)
            return True

        except Exception:
            return False
