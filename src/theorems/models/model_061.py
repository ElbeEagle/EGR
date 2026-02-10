"""
Model 61: Vector_Perpendicular_Condition
向量垂直条件

公式: a⊥b <=> a·b = 0
用于: 判断或建立两向量垂直的条件
"""

import re
from ..base_model import TheoremModel


class VectorPerpendicularCondition(TheoremModel):
    """
    向量垂直条件
    
    前置条件:
    - 存在向量
    - 存在垂直关系
    
    输出:
    - 向量数量积为0: a·b = 0
    
    示例:
    输入: 向量AB ⊥ 向量CD
    输出: AB·CD = 0
    """
    
    def __init__(self):
        super().__init__(
            model_id=61,
            name="Vector_Perpendicular_Condition",
            chinese_name="向量垂直条件"
        )
    
    def can_apply(self, state) -> bool:
        """
        检查是否可应用（放宽条件）
        
        条件:
        1. 存在向量或垂直关系
        2. 或存在线段和垂直符号
        """
        # 检查是否有垂直关系
        for rel in state.geometric_relations:
            if any(kw in rel for kw in ['Perpendicular', 'IsPerpendicular', '垂直', 'Vector', '⊥']):
                return True
        
        # 检查是否有向量相关实体
        has_vector = any('Vector' in str(v) for v in state.entities.values())
        if has_vector:
            return True
        
        # 检查是否有线段和垂直信息（放宽）
        has_line = any('Line' in str(v) for v in state.entities.values())
        has_perp_info = any('⊥' in rel or 'perpendicular' in rel.lower() 
                           for rel in state.geometric_relations)
        
        return has_line and has_perp_info
    
    def apply(self, state) -> bool:
        """
        应用模型，建立垂直条件
        """
        try:
            # 查找垂直关系
            for rel in state.geometric_relations:
                # IsPerpendicular(AB, CD) 或 Perpendicular
                if 'IsPerpendicular' in rel or 'Perpendicular' in rel:
                    # 提取向量或线段
                    match = re.search(r'IsPerpendicular\((\w+),\s*(\w+)\)', rel)
                    if not match:
                        match = re.search(r'Perpendicular\((\w+),\s*(\w+)\)', rel)
                
                    if match:
                        vec1 = match.group(1)
                        vec2 = match.group(2)
                    
                        # 添加向量数量积为0的关系
                        dot_product_rel = f"DotProduct({vec1}, {vec2}) = 0"
                        if dot_product_rel not in state.geometric_relations:
                            state.geometric_relations.append(dot_product_rel)
                    
                        # 如果是坐标形式，添加坐标乘积关系
                        state.geometric_relations.append(f"VectorPerpendicular({vec1}, {vec2})")
        
            # 记录已应用的模型
            state.applied_models.append(self.model_id)
            return True

        except Exception:
            return False
