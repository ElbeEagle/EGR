"""
Model 59: Vector_Dot_Product_Algebraic
向量数量积(代数形式)

公式: a⃗·b⃗ = x₁x₂ + y₁y₂
用于: 已知两个向量的坐标，计算数量积（点积）
"""

import re
from itertools import combinations
from ..base_model import TheoremModel


class VectorDotProductAlgebraic(TheoremModel):
    """
    向量数量积（代数形式）
    
    前置条件:
    - 存在向量信息（geometric_relations 中提到 Vector 或 向量）
    - 或存在至少 2 个点的坐标（可构造向量）
    
    输出:
    - geometric_relations: 数量积公式 a⃗·b⃗ = x₁x₂ + y₁y₂
    - parameters: 具体数量积值
    - 如果有垂直条件，添加 x₁x₂ + y₁y₂ = 0
    
    示例:
    输入: a⃗ = (1, 2), b⃗ = (3, 4)
    输出: a⃗·b⃗ = 1×3 + 2×4 = 11
    """
    
    def __init__(self):
        super().__init__(
            model_id=59,
            name="Vector_Dot_Product_Algebraic",
            chinese_name="向量数量积(代数)"
        )
    
    def can_apply(self, state) -> bool:
        """
        检查是否可应用
        
        条件:
        1. geometric_relations 中提到 Vector / 向量
        2. 或存在至少 2 个点的坐标（可构造向量）
        """
        # 条件1: 有向量相关信息
        for rel in state.geometric_relations:
            if any(kw in rel for kw in ['Vector', 'vector', '向量', 'DotProduct', '数量积', '点积']):
                return True
        
        # 条件1b: entities 中有向量
        for entity_type in state.entities.values():
            if 'Vector' in str(entity_type) or '向量' in str(entity_type):
                return True
        
        # 条件2: 至少有 2 个点的坐标
        if len(state.coordinates) >= 2:
            return True
        
        return False
    
    def apply(self, state) -> bool:
        """
        应用模型，添加向量数量积代数公式
        """
        try:
            # 添加通用公式
            general_formula = "向量数量积(代数形式): a⃗·b⃗ = x₁x₂ + y₁y₂"
            if general_formula not in state.geometric_relations:
                state.geometric_relations.append(general_formula)
            
            # 检查是否有垂直条件
            has_perpendicular = any(
                any(kw in rel for kw in ['Perpendicular', '垂直', '⊥', 'perp'])
                for rel in state.geometric_relations
            )
            
            if has_perpendicular:
                perp_formula = "向量垂直条件: a⃗·b⃗ = 0, 即 x₁x₂ + y₁y₂ = 0"
                if perp_formula not in state.geometric_relations:
                    state.geometric_relations.append(perp_formula)
            
            # 尝试从 geometric_relations 中提取已知向量
            vectors = self._extract_vectors(state)
            
            # 计算已知向量对的数量积
            if len(vectors) >= 2:
                for (v_name1, v1), (v_name2, v2) in combinations(vectors.items(), 2):
                    dot = self._compute_dot_product(v1, v2)
                    if dot is not None:
                        dot_key = f"dot_{v_name1}_{v_name2}"
                        state.parameters[dot_key] = str(dot)
                        
                        rel_str = (
                            f"DotProduct({v_name1}, {v_name2}) = "
                            f"{v1[0]}*{v2[0]} + {v1[1]}*{v2[1]} = {dot}"
                        )
                        if rel_str not in state.geometric_relations:
                            state.geometric_relations.append(rel_str)
            
            # 用坐标点对构造向量并计算数量积
            coord_list = list(state.coordinates.items())
            
            if len(coord_list) >= 3:
                # 以第一个点为公共点，构造向量对
                origin_name, origin_coord = coord_list[0]
                constructed_vectors = {}
                
                for point_name, point_coord in coord_list[1:]:
                    vec_name = f"{origin_name}{point_name}"
                    vec = self._construct_vector(origin_coord, point_coord)
                    if vec is not None:
                        constructed_vectors[vec_name] = vec
                
                # 计算构造向量对的数量积
                for (v_name1, v1), (v_name2, v2) in combinations(
                    constructed_vectors.items(), 2
                ):
                    dot = self._compute_dot_product(v1, v2)
                    if dot is not None:
                        dot_key = f"dot_{v_name1}_{v_name2}"
                        if dot_key not in state.parameters:
                            state.parameters[dot_key] = str(dot)
                            
                            rel_str = (
                                f"DotProduct(vec_{v_name1}, vec_{v_name2}) = "
                                f"{v1[0]}*{v2[0]} + {v1[1]}*{v2[1]} = {dot}"
                            )
                            if rel_str not in state.geometric_relations:
                                state.geometric_relations.append(rel_str)
                            
                            # 如果点积为0，标注垂直
                            if dot == 0:
                                perp_rel = (
                                    f"Perpendicular(vec_{v_name1}, vec_{v_name2}): "
                                    f"数量积为0，向量垂直"
                                )
                                if perp_rel not in state.geometric_relations:
                                    state.geometric_relations.append(perp_rel)
            
            elif len(coord_list) == 2:
                # 只有两个点，构造一个向量
                name1, coord1 = coord_list[0]
                name2, coord2 = coord_list[1]
                vec = self._construct_vector(coord1, coord2)
                if vec is not None:
                    vec_name = f"{name1}{name2}"
                    rel_str = f"Vector({vec_name}) = ({vec[0]}, {vec[1]})"
                    if rel_str not in state.geometric_relations:
                        state.geometric_relations.append(rel_str)
            
            # 记录已应用的模型
            state.applied_models.append(self.model_id)
            return True
        
        except Exception:
            return False
    
    def _extract_vectors(self, state):
        """
        从 geometric_relations 中提取已知向量
        
        支持形式:
        - Vector(AB) = (x, y)
        - 向量AB = (x, y)
        - vec_AB = (x, y)
        
        Returns:
            dict: {name: (x, y)}
        """
        vectors = {}
        
        for rel in state.geometric_relations:
            # 匹配 Vector(XX) = (x, y)
            match = re.search(
                r'Vector\((\w+)\)\s*=\s*\(\s*([^,]+)\s*,\s*([^)]+)\s*\)', rel
            )
            if match:
                name = match.group(1)
                x_str = match.group(2).strip()
                y_str = match.group(3).strip()
                vectors[name] = (x_str, y_str)
                continue
            
            # 匹配 向量XX = (x, y)
            match = re.search(
                r'向量\s*(\w+)\s*=\s*\(\s*([^,]+)\s*,\s*([^)]+)\s*\)', rel
            )
            if match:
                name = match.group(1)
                x_str = match.group(2).strip()
                y_str = match.group(3).strip()
                vectors[name] = (x_str, y_str)
                continue
            
            # 匹配 vec_XX = (x, y)
            match = re.search(
                r'vec[_]?(\w+)\s*=\s*\(\s*([^,]+)\s*,\s*([^)]+)\s*\)', rel
            )
            if match:
                name = match.group(1)
                x_str = match.group(2).strip()
                y_str = match.group(3).strip()
                vectors[name] = (x_str, y_str)
        
        return vectors
    
    def _construct_vector(self, coord1, coord2):
        """
        从两个点坐标构造向量 (x2-x1, y2-y1)
        
        Returns:
            (dx, dy) 数值元组, 或 None
        """
        try:
            x1, y1 = float(coord1[0]), float(coord1[1])
            x2, y2 = float(coord2[0]), float(coord2[1])
            
            dx = x2 - x1
            dy = y2 - y1
            
            # 格式化
            dx = int(dx) if dx == int(dx) else round(dx, 4)
            dy = int(dy) if dy == int(dy) else round(dy, 4)
            
            return (dx, dy)
        except (ValueError, TypeError):
            return None
    
    def _compute_dot_product(self, v1, v2):
        """
        计算两个向量的数量积 x1*x2 + y1*y2
        
        Args:
            v1: (x1, y1)
            v2: (x2, y2)
        
        Returns:
            数值结果, 或 None
        """
        try:
            x1, y1 = float(v1[0]), float(v1[1])
            x2, y2 = float(v2[0]), float(v2[1])
            
            dot = x1 * x2 + y1 * y2
            
            # 格式化
            if dot == int(dot):
                return int(dot)
            else:
                return round(dot, 4)
        except (ValueError, TypeError):
            return None
