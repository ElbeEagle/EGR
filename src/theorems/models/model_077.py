"""
Model 77: Homogenization_Eccentricity
齐次化求离心率

方法: 将方程除以 a²，用 e = c/a 代换
椭圆: b²/a² = 1 - e²
双曲线: b²/a² = e² - 1
"""

import re
from ..base_model import TheoremModel


class HomogenizationEccentricity(TheoremModel):
    """
    齐次化求离心率
    
    前置条件:
    - 存在圆锥曲线 (Ellipse 或 Hyperbola)
    - 已知参数 a, b 或 a², b²
    - 存在涉及 a, b, c 的方程或关系
    
    输出:
    - 齐次化代换关系 (b²/a² 用 e 表示)
    - 尝试求解离心率 e
    - 添加约束 (椭圆 0 < e < 1, 双曲线 e > 1)
    
    示例:
    输入: 椭圆 x²/a² + y²/b² = 1, 关系 b² = 2ac
    输出: 1 - e² = 2e => e² + 2e - 1 = 0 => e = √2 - 1
    """
    
    def __init__(self):
        super().__init__(
            model_id=77,
            name="Homogenization_Eccentricity",
            chinese_name="齐次化求离心率"
        )
    
    def can_apply(self, state) -> bool:
        """
        检查是否可应用
        
        条件:
        1. 存在圆锥曲线 (Ellipse 或 Hyperbola)
        2. 已知参数 a, b 或 a², b²
        3. 存在涉及 a, b, c 的方程或关系
        """
        # 条件1: 存在椭圆或双曲线
        has_conic = any(
            entity_type.lower() in ('ellipse', 'hyperbola')
            for entity_type in state.entities.values()
        )
        if not has_conic:
            return False
        
        # 条件2: 已知 a, b 相关参数
        has_a = 'a' in state.parameters or 'a^2' in state.parameters
        has_b = 'b' in state.parameters or 'b^2' in state.parameters
        if not (has_a or has_b):
            return False
        
        # 条件3: 存在涉及 a, b, c 的方程或关系
        abc_keywords = ['a', 'b', 'c', 'a^2', 'b^2', 'c^2',
                        'a²', 'b²', 'c²', 'eccentricity', '离心率']
        
        has_abc_relation = False
        
        # 检查方程中是否涉及 a, b, c 的关系
        for eq in state.equations:
            matches = sum(1 for kw in ['a', 'b', 'c'] if kw in eq)
            if matches >= 2:
                has_abc_relation = True
                break
        
        # 检查几何关系中是否涉及
        if not has_abc_relation:
            for rel in state.geometric_relations:
                matches = sum(1 for kw in ['a', 'b', 'c'] if kw in rel)
                if matches >= 2:
                    has_abc_relation = True
                    break
        
        # 也检查是否明确要求离心率
        if not has_abc_relation:
            for rel in state.geometric_relations:
                if any(kw in rel for kw in ['eccentricity', '离心率', 'Eccentricity']):
                    has_abc_relation = True
                    break
        
        return has_abc_relation
    
    def apply(self, state) -> bool:
        """
        应用齐次化方法求离心率
        
        步骤:
        1. 确定曲线类型 (椭圆/双曲线)
        2. 建立 b²/a² 与 e 的关系
        3. 对涉及 a, b, c 的方程除以 a²
        4. 用 e = c/a 代换
        5. 尝试求解 e
        """
        try:
            # 确定曲线类型
            is_ellipse = any(
                entity_type.lower() == 'ellipse'
                for entity_type in state.entities.values()
            )
            is_hyperbola = any(
                entity_type.lower() == 'hyperbola'
                for entity_type in state.entities.values()
            )
            
            # 添加齐次化核心代换
            state.geometric_relations.append(
                "Homogenization: let e = c/a"
            )
            
            if is_ellipse:
                # 椭圆: b² = a² - c², 所以 b²/a² = 1 - e²
                state.geometric_relations.append(
                    "Ellipse: b²/a² = 1 - e²"
                )
                state.parameters['b^2/a^2'] = '1 - e^2'
                state.constraints.append("0 < e < 1")
                
            elif is_hyperbola:
                # 双曲线: b² = c² - a², 所以 b²/a² = e² - 1
                state.geometric_relations.append(
                    "Hyperbola: b²/a² = e² - 1"
                )
                state.parameters['b^2/a^2'] = 'e^2 - 1'
                state.constraints.append("e > 1")
            
            # 扫描方程和关系，进行齐次化代换
            substituted = False
            all_sources = state.equations + state.geometric_relations
            
            for source in all_sources:
                # 查找包含 b^2 和 a 或 c 的关系，例如 b^2 = 2ac
                if self._has_abc_relation(source):
                    homogenized = self._homogenize(source, is_ellipse)
                    if homogenized:
                        state.geometric_relations.append(
                            f"Homogenized: {homogenized}"
                        )
                        state.equations.append(homogenized)
                        substituted = True
            
            # 尝试解出 e
            if substituted or is_ellipse or is_hyperbola:
                state.geometric_relations.append(
                    "Solve for eccentricity e from homogenized equation"
                )
            
            # 如果参数中已有 e 的值，记录
            if 'e' in state.parameters:
                state.geometric_relations.append(
                    f"Eccentricity e = {state.parameters['e']}"
                )
            
            # 记录已应用的模型
            state.applied_models.append(self.model_id)
            return True
        
        except Exception:
            return False
    
    def _has_abc_relation(self, expr: str) -> bool:
        """检查表达式是否涉及 a, b, c 中至少两个"""
        count = 0
        # 用简单的启发式检查
        if re.search(r'\ba\b|a\^2|a²', expr):
            count += 1
        if re.search(r'\bb\b|b\^2|b²', expr):
            count += 1
        if re.search(r'\bc\b|c\^2|c²', expr):
            count += 1
        return count >= 2
    
    def _homogenize(self, expr: str, is_ellipse: bool) -> str:
        """
        对表达式进行齐次化处理
        
        将 b² 替换为 a²(1-e²) (椭圆) 或 a²(e²-1) (双曲线)
        将 c 替换为 a*e
        然后除以 a² 消去 a
        
        Returns:
            齐次化后的表达式字符串，失败返回空字符串
        """
        try:
            result = expr
            
            if is_ellipse:
                # b^2 -> a^2*(1-e^2)
                result = re.sub(r'b\^2|b²', 'a^2*(1-e^2)', result)
            else:
                # b^2 -> a^2*(e^2-1)
                result = re.sub(r'b\^2|b²', 'a^2*(e^2-1)', result)
            
            # c^2 -> a^2*e^2
            result = re.sub(r'c\^2|c²', 'a^2*e^2', result)
            
            # c -> a*e (单独的 c，不在其他变量中)
            result = re.sub(r'\bc\b', 'a*e', result)
            
            # 标记：除以 a² 后简化
            if result != expr:
                result = f"(After dividing by a²): {result}"
                return result
            
            return ""
        except Exception:
            return ""
