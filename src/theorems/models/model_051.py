"""
Model 51: Chord_Length_Formula_With_K
弦长公式（含斜率）

公式: |AB| = |x₁ - x₂| · √(1 + k²)
利用韦达定理: |x₁ - x₂| = √((x₁+x₂)² - 4·x₁·x₂)

用于: 已知直线斜率 k 和韦达定理结果，求弦长
"""

import math
from ..base_model import TheoremModel


class ChordLengthFormulaWithK(TheoremModel):
    """
    弦长公式（含斜率）
    
    前置条件:
    - 已知斜率 k
    - 已知韦达定理结果 (x₁+x₂, x₁·x₂) 或判别式 Δ
    
    输出:
    - parameters: chord_length（弦长）
    - geometric_relations: 弦长公式
    
    示例:
    输入: k=1, x1+x2=4, x1*x2=3
    输出: |AB| = √((4)² - 4·3) · √(1+1²) = 2√2
    """
    
    def __init__(self):
        super().__init__(
            model_id=51,
            name="Chord_Length_Formula_With_K",
            chinese_name="弦长公式(含斜率)"
        )
    
    def can_apply(self, state) -> bool:
        """
        检查是否可应用
        
        条件:
        1. 存在斜率 k
        2. 存在韦达定理结果 (x1_plus_x2 和 x1_times_x2) 或 判别式 delta
        """
        # 条件1: 必须有斜率 k
        has_slope = 'k' in state.parameters or 'slope' in state.parameters
        if not has_slope:
            # 也检查几何关系中是否有斜率信息
            has_slope = any(
                'k=' in rel or 'slope' in rel.lower() or '斜率' in rel
                for rel in state.geometric_relations
            )
        if not has_slope:
            return False
        
        # 条件2: 必须有韦达定理结果或判别式
        has_vieta_x = ('x1_plus_x2' in state.parameters and
                       'x1_times_x2' in state.parameters)
        has_vieta_y = ('y1_plus_y2' in state.parameters and
                       'y1_times_y2' in state.parameters)
        has_delta = 'delta' in state.parameters or 'discriminant' in state.parameters
        
        return has_vieta_x or has_vieta_y or has_delta
    
    def apply(self, state) -> bool:
        """
        应用模型，计算弦长
        
        公式: |AB| = √(1 + k²) · |x₁ - x₂|
        其中: |x₁ - x₂| = √((x₁+x₂)² - 4·x₁·x₂)
        """
        try:
            # 获取斜率 k
            k_val = self._get_slope(state)
            
            # 添加通用弦长公式
            formula = "弦长公式: |AB| = √(1+k²) · √((x₁+x₂)² - 4·x₁·x₂)"
            if formula not in state.geometric_relations:
                state.geometric_relations.append(formula)
            
            # 尝试用 x 的韦达定理结果计算
            if 'x1_plus_x2' in state.parameters and 'x1_times_x2' in state.parameters:
                self._compute_chord_length(state, k_val, 'x')
            
            # 尝试用 y 的韦达定理结果计算
            elif 'y1_plus_y2' in state.parameters and 'y1_times_y2' in state.parameters:
                self._compute_chord_length(state, k_val, 'y')
            
            # 尝试用判别式计算
            elif 'delta' in state.parameters or 'discriminant' in state.parameters:
                self._compute_chord_from_delta(state, k_val)
            
            # 记录已应用的模型
            state.applied_models.append(self.model_id)
            return True

        except Exception:
            return False
    
    def _get_slope(self, state):
        """获取斜率值"""
        k_str = state.parameters.get('k') or state.parameters.get('slope')
        if k_str is not None:
            try:
                return float(k_str)
            except (ValueError, TypeError):
                return k_str
        return None
    
    def _compute_chord_length(self, state, k_val, var='x'):
        """
        利用韦达定理结果计算弦长
        
        |AB| = √(1+k²) · √((x₁+x₂)² - 4·x₁·x₂)
        """
        sum_key = f'{var}1_plus_{var}2'
        prod_key = f'{var}1_times_{var}2'
        
        sum_str = state.parameters.get(sum_key)
        prod_str = state.parameters.get(prod_key)
        
        try:
            sum_val = float(sum_str)
            prod_val = float(prod_str)
            
            # |x₁ - x₂|² = (x₁+x₂)² - 4·x₁·x₂
            diff_squared = sum_val ** 2 - 4 * prod_val
            
            if diff_squared < 0:
                # 判别式为负，无实数交点
                state.geometric_relations.append(
                    f"弦长计算: ({var}₁+{var}₂)²-4·{var}₁·{var}₂ = {diff_squared} < 0，无实数交点"
                )
                return
            
            diff_abs = math.sqrt(diff_squared)
            
            if isinstance(k_val, (int, float)):
                # 数值计算
                chord_length = math.sqrt(1 + k_val ** 2) * diff_abs
                
                chord_str = str(int(chord_length)) if chord_length == int(chord_length) else str(round(chord_length, 4))
                
                state.parameters['chord_length'] = chord_str
                state.parameters['|AB|'] = chord_str
                state.geometric_relations.append(
                    f"弦长: |AB| = √(1+{k_val}²) · √(({sum_str})²-4·({prod_str})) = {chord_str}"
                )
            else:
                # 符号计算
                diff_str = str(int(diff_abs)) if diff_abs == int(diff_abs) else str(round(diff_abs, 4))
                chord_expr = f"√(1+({k_val})²) · {diff_str}"
                
                state.parameters['chord_length'] = chord_expr
                state.parameters['|AB|'] = chord_expr
                state.geometric_relations.append(
                    f"弦长: |AB| = √(1+({k_val})²) · √(({sum_str})²-4·({prod_str})) = {chord_expr}"
                )
        
        except (ValueError, TypeError):
            # 符号形式
            chord_expr = f"√(1+k²) · √(({sum_str})²-4·({prod_str}))"
            state.parameters['chord_length'] = chord_expr
            state.parameters['|AB|'] = chord_expr
            state.geometric_relations.append(f"弦长: |AB| = {chord_expr}")
    
    def _compute_chord_from_delta(self, state, k_val):
        """
        利用判别式计算弦长
        
        |AB| = √(1+k²) · √Δ / |A|
        其中 A 是二次方程的二次项系数
        """
        delta_str = state.parameters.get('delta') or state.parameters.get('discriminant')
        coeff_a = state.parameters.get('equation_A', '1')
        
        try:
            delta_val = float(delta_str)
            a_val = float(coeff_a)
            
            if delta_val < 0:
                state.geometric_relations.append("弦长计算: Δ < 0，无实数交点")
                return
            
            if isinstance(k_val, (int, float)):
                chord_length = math.sqrt(1 + k_val ** 2) * math.sqrt(delta_val) / abs(a_val)
                chord_str = str(int(chord_length)) if chord_length == int(chord_length) else str(round(chord_length, 4))
                
                state.parameters['chord_length'] = chord_str
                state.parameters['|AB|'] = chord_str
                state.geometric_relations.append(
                    f"弦长: |AB| = √(1+k²)·√Δ/|A| = {chord_str}"
                )
            else:
                chord_expr = f"√(1+({k_val})²) · √({delta_str}) / {coeff_a}"
                state.parameters['chord_length'] = chord_expr
                state.parameters['|AB|'] = chord_expr
                state.geometric_relations.append(f"弦长: |AB| = {chord_expr}")
        
        except (ValueError, TypeError):
            # 符号形式
            chord_expr = f"√(1+k²) · √({delta_str}) / |{coeff_a}|"
            state.parameters['chord_length'] = chord_expr
            state.parameters['|AB|'] = chord_expr
            state.geometric_relations.append(f"弦长: |AB| = {chord_expr}")
