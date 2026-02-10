"""
Model 33: Parabola_Focal_Chord_Length
抛物线焦点弦长

公式: |AB| = x1 + x2 + p (对于 y² = 2px)
性质: x1*x2 = p²/4, y1*y2 = -p²
"""

import re
from ..base_model import TheoremModel


class ParabolaFocalChordLength(TheoremModel):
    """
    抛物线焦点弦长
    
    前置条件:
    - 存在 Parabola 实体
    - 已知参数 p
    - 存在焦点弦相关信息 (两个点或 x 坐标)
    
    输出:
    - 焦点弦长 |AB| = x1 + x2 + p
    - 性质: x1*x2 = p²/4
    - 性质: y1*y2 = -p²
    
    示例:
    输入: y² = 2px, 焦点弦 AB, x1 = 1, x2 = 4, p = 2
    输出: |AB| = 1 + 4 + 2 = 7
    """
    
    def __init__(self):
        super().__init__(
            model_id=33,
            name="Parabola_Focal_Chord_Length",
            chinese_name="抛物线焦点弦长"
        )
    
    def can_apply(self, state) -> bool:
        """
        检查是否可应用
        
        条件:
        1. 存在 Parabola 实体
        2. 已知参数 p (或 2p)
        3. 存在焦点弦相关信息
        """
        # 条件1: 存在抛物线
        has_parabola = any(
            entity_type.lower() == 'parabola'
            for entity_type in state.entities.values()
        )
        if not has_parabola:
            return False
        
        # 条件2: 已知 p 或 2p
        has_p = ('p' in state.parameters or '2p' in state.parameters
                 or 'p/2' in state.parameters)
        if not has_p:
            # 也可从方程中推断 p
            for eq in state.equations:
                if re.search(r'y\^2\s*=\s*\d+', eq):
                    has_p = True
                    break
        
        if not has_p:
            return False
        
        # 条件3: 存在焦点弦相关信息
        has_focal_chord = False
        
        # 检查是否有两个点的坐标
        point_count = sum(
            1 for entity_type in state.entities.values()
            if entity_type.lower() == 'point'
        )
        if point_count >= 2:
            has_focal_chord = True
        
        # 检查是否有 x1, x2 或焦点弦关键词
        if not has_focal_chord:
            has_x_coords = ('x1' in state.parameters or 'x_1' in state.parameters
                            or 'x2' in state.parameters or 'x_2' in state.parameters)
            if has_x_coords:
                has_focal_chord = True
        
        # 检查几何关系中是否提到焦点弦
        if not has_focal_chord:
            focal_keywords = ['FocalChord', 'Focal_Chord', '焦点弦',
                              'Chord', '弦', 'AB']
            has_focal_chord = any(
                kw in rel for rel in state.geometric_relations
                for kw in focal_keywords
            )
        
        return has_focal_chord
    
    def apply(self, state) -> bool:
        """
        应用模型，计算焦点弦长并添加性质
        
        步骤:
        1. 获取 p 的值
        2. 获取 x1, x2 (如果已知)
        3. 计算 |AB| = x1 + x2 + p
        4. 添加性质 x1*x2 = p²/4, y1*y2 = -p²
        """
        try:
            # 获取 p 的值
            p = state.parameters.get('p')
            two_p = state.parameters.get('2p')
            
            if p is None and two_p is not None:
                p = f"({two_p})/2"
                try:
                    p = str(float(two_p) / 2)
                except (ValueError, TypeError):
                    pass
            
            # 如果仍没有 p，尝试从方程 y^2 = 2px 中提取
            if p is None:
                for eq in state.equations:
                    match = re.search(r'y\^2\s*=\s*(\d+)\s*\*?\s*x', eq)
                    if match:
                        coeff = int(match.group(1))
                        p = str(coeff // 2)
                        state.parameters['p'] = p
                        break
            
            if p is None:
                p = 'p'
            
            # 添加焦点弦长公式 (通用)
            state.geometric_relations.append(
                f"FocalChordLength: |AB| = x1 + x2 + {p}"
            )
            
            # 获取 x1, x2 并尝试计算具体值
            x1 = state.parameters.get('x1') or state.parameters.get('x_1')
            x2 = state.parameters.get('x2') or state.parameters.get('x_2')
            
            if x1 is not None and x2 is not None:
                # 尝试计算具体弦长
                try:
                    x1_val = float(x1)
                    x2_val = float(x2)
                    p_val = float(p)
                    chord_length = x1_val + x2_val + p_val
                    state.parameters['focal_chord_length'] = str(chord_length)
                    state.geometric_relations.append(
                        f"|AB| = {x1} + {x2} + {p} = {chord_length}"
                    )
                except (ValueError, TypeError):
                    # 保持符号形式
                    state.parameters['focal_chord_length'] = f"{x1} + {x2} + {p}"
                    state.geometric_relations.append(
                        f"|AB| = {x1} + {x2} + {p}"
                    )
            else:
                state.parameters['focal_chord_length'] = f"x1 + x2 + {p}"
            
            # 添加焦点弦性质: x1*x2 = p²/4
            try:
                p_val = float(p)
                x1x2_val = str(p_val ** 2 / 4)
                y1y2_val = str(-(p_val ** 2))
            except (ValueError, TypeError):
                x1x2_val = f"{p}^2/4"
                y1y2_val = f"-{p}^2"
            
            state.geometric_relations.append(
                f"FocalChordProperty: x1*x2 = {x1x2_val}"
            )
            state.parameters['x1*x2'] = x1x2_val
            
            # 添加焦点弦性质: y1*y2 = -p²
            state.geometric_relations.append(
                f"FocalChordProperty: y1*y2 = {y1y2_val}"
            )
            state.parameters['y1*y2'] = y1y2_val
            
            # 记录已应用的模型
            state.applied_models.append(self.model_id)
            return True
        
        except Exception:
            return False
