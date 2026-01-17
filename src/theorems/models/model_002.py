"""
Model 2: Parabola_Definition
抛物线定义

定义: 点到焦点的距离 = 点到准线的距离
|PF| = d(P, directrix)
"""

from ..base_model import TheoremModel


class ParabolaDefinition(TheoremModel):
    """
    抛物线定义
    
    前置条件:
    - 实体包含 Parabola 类型
    - 有焦点信息或准线信息
    
    输出:
    - geometric_relations: |PF| = d(P, directrix)
    
    示例:
    对于抛物线上的点P，添加关系 Distance(P, Focus) = Distance(P, Directrix)
    """
    
    def __init__(self):
        super().__init__(
            model_id=2,
            name="Parabola_Definition",
            chinese_name="抛物线定义"
        )
    
    def can_apply(self, state) -> bool:
        """
        检查是否可应用
        
        条件:
        1. 存在 Parabola 实体
        2. 有焦点或准线相关信息
        """
        # 条件1: 检查是否有抛物线实体
        has_parabola = any(
            entity_type.lower() == 'parabola'
            for entity_type in state.entities.values()
        )
        if not has_parabola:
            return False
        
        # 条件2: 检查是否有焦点或准线信息
        # 如果有p参数，说明已经有焦点/准线信息
        if 'p' in state.parameters or '2p' in state.parameters:
            return True
        
        # 或者从几何关系中查找
        for rel in state.geometric_relations:
            if 'Focus' in rel or 'Directrix' in rel or '焦点' in rel or '准线' in rel:
                return True
        
        return False
    
    def apply(self, state) -> None:
        """
        应用模型，添加抛物线定义关系
        """
        # 添加定义关系（通用形式）
        relation = "抛物线定义: |PF| = d(P, directrix)"
        
        # 避免重复添加
        if relation not in state.geometric_relations:
            state.geometric_relations.append(relation)
        
        # 如果有具体的焦点坐标，添加更具体的关系
        if 'Focus' in state.coordinates:
            focus_coord = state.coordinates['Focus']
            state.geometric_relations.append(
                f"对于抛物线上任意点P: Distance(P, Focus{focus_coord}) = Distance(P, Directrix)"
            )
        
        # 记录已应用的模型
        state.applied_models.append(self.model_id)
