"""
Model 68: Triangle_Midline_Theorem
三角形中位线定理

定理: 三角形中位线平行于第三边，且等于第三边的一半
公式: 中位线 = 底边 / 2
"""

import math
from ..base_model import TheoremModel


class TriangleMidlineTheorem(TheoremModel):
    """
    三角形中位线定理
    
    前置条件:
    - 存在中点信息 (MidPoint)
    - 或存在三角形相关几何关系
    
    输出:
    - geometric_relations: 中位线 = 底边/2，中位线平行于底边
    - parameters: 如果已知中点坐标，添加相关中位线长度
    
    示例:
    三角形ABC中，D、E分别为AB、AC的中点
    输出: DE = BC/2，DE ∥ BC
    """
    
    def __init__(self):
        super().__init__(
            model_id=68,
            name="Triangle_Midline_Theorem",
            chinese_name="三角形中位线定理"
        )
    
    def can_apply(self, state) -> bool:
        """
        检查是否可应用
        
        条件:
        1. 存在中点信息 (MidPoint 在 geometric_relations 或 coordinates 中)
        2. 或存在三角形相关的几何关系
        """
        # 条件1: 检查是否有中点信息
        for rel in state.geometric_relations:
            if 'MidPoint' in rel or 'Midpoint' in rel or '中点' in rel:
                return True
        
        # 条件2: 检查坐标中是否暗含中点（例如名称含 M 且有对应端点）
        if self._has_midpoint_in_coordinates(state):
            return True
        
        # 条件3: 检查是否有三角形相关关系
        for rel in state.geometric_relations:
            if 'Triangle' in rel or '三角形' in rel:
                return True
        
        # 条件4: 检查实体中是否有 Triangle 类型
        for entity_type in state.entities.values():
            if entity_type.lower() == 'triangle':
                return True
        
        return False
    
    def apply(self, state) -> bool:
        """
        应用模型，添加中位线定理关系
        """
        try:
            # 添加通用中位线定理公式
            relation = "三角形中位线定理: 中位线平行于第三边，且等于第三边的一半"
            if relation not in state.geometric_relations:
                state.geometric_relations.append(relation)
            
            # 从几何关系中提取中点信息并建立中位线关系
            self._apply_midline_from_relations(state)
            
            # 从坐标中计算中位线（如果有具体坐标）
            self._apply_midline_from_coordinates(state)
            
            # 记录已应用的模型
            state.applied_models.append(self.model_id)
            return True

        except Exception:
            return False
    
    def _has_midpoint_in_coordinates(self, state) -> bool:
        """检查坐标中是否有中点信息"""
        # 如果有名为 M、D、E 等常见中点名的坐标，且有对应的三角形顶点
        midpoint_names = {'M', 'D', 'E', 'N', 'P'}
        vertex_names = {'A', 'B', 'C'}
        
        has_midpoint_candidate = any(
            name in midpoint_names for name in state.coordinates
        )
        has_vertices = sum(
            1 for name in state.coordinates if name in vertex_names
        ) >= 2
        
        return has_midpoint_candidate and has_vertices
    
    def _apply_midline_from_relations(self, state):
        """从几何关系中提取中点信息，建立中位线关系"""
        midpoints = []
        
        for rel in state.geometric_relations:
            # 匹配 "MidPoint(D, A, B)" 格式：D 是 AB 的中点
            if 'MidPoint' in rel or 'Midpoint' in rel:
                midpoints.append(rel)
            elif '中点' in rel:
                midpoints.append(rel)
        
        if len(midpoints) >= 2:
            # 有两个中点，可以构成中位线
            state.geometric_relations.append(
                "中位线定理应用: 两中点连线 = 对边/2"
            )
            state.geometric_relations.append(
                "中位线定理应用: 两中点连线 ∥ 对边"
            )
        elif len(midpoints) == 1:
            # 有一个中点，添加一般性中位线关系
            state.geometric_relations.append(
                f"中位线关系: {midpoints[0]} → 中位线 = 底边/2"
            )
    
    def _apply_midline_from_coordinates(self, state):
        """从坐标计算中位线长度"""
        # 查找可能的三角形顶点
        vertex_candidates = {}
        for name, coord in state.coordinates.items():
            vertex_candidates[name] = coord
        
        # 如果有中点关系，尝试计算中位线长度
        for rel in state.geometric_relations:
            if 'MidPoint' not in rel and 'Midpoint' not in rel and '中点' not in rel:
                continue
            
            # 尝试提取中点对应的底边端点
            # 常见格式: MidPoint(M, A, B) 表示 M 是 AB 中点
            for p1_name, p1_coord in state.coordinates.items():
                for p2_name, p2_coord in state.coordinates.items():
                    if p1_name >= p2_name:
                        continue
                    # 检查 rel 中是否包含这两个端点
                    if p1_name in rel and p2_name in rel:
                        base_len = self._calculate_distance(p1_coord, p2_coord)
                        if base_len is not None:
                            midline_len = base_len / 2
                            midline_str = str(int(midline_len)) if midline_len == int(midline_len) else str(round(midline_len, 4))
                            param_key = f"midline_{p1_name}{p2_name}"
                            if param_key not in state.parameters:
                                state.parameters[param_key] = midline_str
                                state.geometric_relations.append(
                                    f"中位线长度: 平行于{p1_name}{p2_name}的中位线 = |{p1_name}{p2_name}|/2 = {midline_str}"
                                )
    
    def _calculate_distance(self, coord1, coord2):
        """
        计算两点间距离
        
        Returns:
            distance: 距离值，失败返回 None
        """
        try:
            x1, y1 = float(coord1[0]), float(coord1[1])
            x2, y2 = float(coord2[0]), float(coord2[1])
            
            distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
            
            if distance == int(distance):
                return int(distance)
            else:
                return round(distance, 4)
        except (ValueError, TypeError):
            return None
