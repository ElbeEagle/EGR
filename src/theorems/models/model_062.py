"""
Model 62: Vector_Collinear_Condition
向量共线条件

公式: 
  向量a与向量b共线 ⟺ a⃗ = λb⃗
  坐标形式: x₁y₂ - x₂y₁ = 0
"""

from ..base_model import TheoremModel


class VectorCollinearCondition(TheoremModel):
    """
    向量共线条件
    
    前置条件:
    - 存在向量相关信息
    - 或有共线/平行判断需求
    
    输出:
    - geometric_relations: 向量共线条件
    
    示例:
    向量a⃗(x₁, y₁)与向量b⃗(x₂, y₂)共线
    ⟺ x₁y₂ - x₂y₁ = 0
    ⟺ x₁/x₂ = y₁/y₂
    """
    
    def __init__(self):
        super().__init__(
            model_id=62,
            name="Vector_Collinear_Condition",
            chinese_name="向量共线条件"
        )
    
    def can_apply(self, state) -> bool:
        """
        检查是否可应用（放宽条件）
        
        条件:
        1. 存在向量相关信息
        2. 或有共线判断需求  
        3. 或存在多个点和线段
        4. 或存在λ系数（向量表示）
        """
        # 检查向量相关关键词
        for rel in state.geometric_relations:
            if any(keyword in rel.lower() for keyword in [
                'vector', '向量', 'collinear', '共线', 'parallel', '平行',
                'lambda', 'λ', 'line', 'segment', '线段'
            ]):
                return True
        
        # 检查是否有三点共线的需求
        for rel in state.geometric_relations:
            if '三点共线' in rel or 'three points collinear' in rel.lower():
                return True
        
        # 检查参数中是否有向量表示或λ
        for param_name in state.parameters.keys():
            if any(kw in param_name.lower() for kw in ['vector', 'vec_', 'lambda', 'λ']):
                return True
        
        # 检查是否有多个点（至少3个）- 可能涉及共线
        if len(state.coordinates) >= 3:
            return True
        
        # 检查实体中是否有线或点
        has_line = any('Line' in str(v) for v in state.entities.values())
        has_multiple_points = sum(1 for v in state.entities.values() if 'Point' in str(v)) >= 2
        
        if has_line or has_multiple_points:
            return True
        
        return False
    
    def apply(self, state) -> bool:
        """
        应用模型，添加向量共线条件
        """
        try:
            # 添加向量共线条件公式
            formulas = [
                "向量共线条件:",
                "  方法1: a⃗ = λb⃗ (λ为实数)",
                "  方法2: x₁y₂ - x₂y₁ = 0 (坐标表示)",
                "  方法3: x₁/x₂ = y₁/y₂ (比例关系)",
            ]
        
            for formula in formulas:
                if formula not in state.geometric_relations:
                    state.geometric_relations.append(formula)
        
            # 添加三点共线的特殊情况
            state.geometric_relations.append(
                "三点共线: A, B, C共线 ⟺ AB⃗与AC⃗共线"
            )
        
            # 记录已应用的模型
            state.applied_models.append(self.model_id)
            return True

        except Exception:
            return False
