"""
Model 1: Hyperbola_Definition
双曲线定义

定义: ||PF₁| - |PF₂|| = 2a
双曲线上任一点到两焦点距离之差的绝对值为定值
"""

from ..base_model import TheoremModel


class HyperbolaDefinition(TheoremModel):
    """
    双曲线定义
    
    前置条件:
    - 实体包含 Hyperbola 类型
    - 有焦点信息或参数a
    
    输出:
    - geometric_relations: ||PF₁| - |PF₂|| = 2a
    
    示例:
    对于双曲线上的点P，添加关系 Abs(Distance(P, F1) - Distance(P, F2)) = 2*a
    """
    
    def __init__(self):
        super().__init__(
            model_id=1,
            name="Hyperbola_Definition",
            chinese_name="双曲线定义"
        )
    
    def can_apply(self, state) -> bool:
        """
        检查是否可应用
        
        条件:
        1. 存在 Hyperbola 实体
        2. 有焦点或参数a相关信息
        """
        # 条件1: 检查是否有双曲线实体
        has_hyperbola = any(
            entity_type.lower() == 'hyperbola'
            for entity_type in state.entities.values()
        )
        if not has_hyperbola:
            return False
        
        # 条件2: 检查是否有焦点或参数a
        if 'a' in state.parameters or 'a^2' in state.parameters:
            return True
        
        # 或者从几何关系中查找焦点
        for rel in state.geometric_relations:
            if 'Focus' in rel or 'F1' in rel or 'F2' in rel or '焦点' in rel:
                return True
        
        # 或者从坐标中查找焦点
        if 'Focus' in state.coordinates or 'F1' in state.coordinates or 'F2' in state.coordinates:
            return True
        
        return False
    
    def apply(self, state) -> None:
        """
        应用模型，添加双曲线定义关系
        """
        # 获取参数a（如果有）
        a_val = state.parameters.get('a')
        if not a_val and 'a^2' in state.parameters:
            try:
                a_sq = float(state.parameters['a^2'])
                a_val = str(a_sq ** 0.5)
            except:
                a_val = f"sqrt({state.parameters['a^2']})"
        
        # 添加定义关系
        if a_val:
            relation = f"双曲线定义: ||PF₁| - |PF₂|| = 2*{a_val}"
        else:
            relation = "双曲线定义: ||PF₁| - |PF₂|| = 2a"
        
        # 避免重复添加
        if relation not in state.geometric_relations:
            state.geometric_relations.append(relation)
        
        # 如果有具体的焦点坐标，添加更具体的关系
        if 'F1' in state.coordinates and 'F2' in state.coordinates:
            f1_coord = state.coordinates['F1']
            f2_coord = state.coordinates['F2']
            state.geometric_relations.append(
                f"对于双曲线上任意点P: Abs(Distance(P, F1{f1_coord}) - Distance(P, F2{f2_coord})) = 2*{a_val if a_val else 'a'}"
            )
        
        # 记录已应用的模型
        state.applied_models.append(self.model_id)
