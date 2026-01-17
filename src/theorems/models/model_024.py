"""
Model 24: Hyperbola_Equal_Axis
等轴双曲线

定义: a = b
等轴双曲线的实轴和虚轴长度相等，离心率为√2
"""

from ..base_model import TheoremModel


class HyperbolaEqualAxis(TheoremModel):
    """
    等轴双曲线
    
    前置条件:
    - 实体包含 Hyperbola 类型
    - 满足以下条件之一:
      1. 渐近线方程为 y = ±x
      2. 离心率 e = √2
      3. 已知 a = b
    
    输出:
    - parameters: a = b
    - geometric_relations: 等轴双曲线性质
    
    示例:
    输入: 渐近线 y = ±x
    输出: a = b, e = √2
    """
    
    def __init__(self):
        super().__init__(
            model_id=24,
            name="Hyperbola_Equal_Axis",
            chinese_name="等轴双曲线"
        )
    
    def can_apply(self, state) -> bool:
        """
        检查是否可应用
        
        条件:
        1. 存在 Hyperbola 实体
        2. 满足等轴双曲线的特征
        """
        # 条件1: 检查是否有双曲线实体
        has_hyperbola = any(
            entity_type.lower() == 'hyperbola'
            for entity_type in state.entities.values()
        )
        if not has_hyperbola:
            return False
        
        # 条件2: 检查是否满足等轴双曲线特征
        
        # 特征1: 渐近线为 y = ±x
        for rel in state.geometric_relations:
            if 'y = ±x' in rel or 'y = pm*x' in rel or 'y = ±(1)*x' in rel:
                return True
            if '渐近线' in rel and ('y = x' in rel or 'y = -x' in rel):
                # 检查是否同时有 y=x 和 y=-x
                has_pos = 'y = x' in rel or 'y = +x' in rel
                has_neg = 'y = -x' in rel
                if has_pos and has_neg:
                    return True
        
        # 特征2: 离心率为 √2
        e_val = state.parameters.get('e')
        if e_val:
            try:
                e_num = float(e_val)
                if abs(e_num - 1.414213562) < 0.001:  # √2 ≈ 1.414
                    return True
            except:
                if 'sqrt(2)' in str(e_val) or '√2' in str(e_val):
                    return True
        
        # 特征3: 已知 a = b
        if 'a' in state.parameters and 'b' in state.parameters:
            try:
                a_num = float(state.parameters['a'])
                b_num = float(state.parameters['b'])
                if abs(a_num - b_num) < 0.001:
                    return True
            except:
                pass
        
        # 特征4: 从方程推断（x² - y² = λ 形式）
        for eq in state.equations:
            # x^2 - y^2 = ... 或 x^2/k - y^2/k = 1
            if 'x^2' in eq and 'y^2' in eq:
                # 检查系数是否相等
                import re
                # 匹配 x^2/a^2 - y^2/b^2 = 1 形式
                match = re.search(r'x\^2/(\S+)\s*-\s*y\^2/(\S+)\s*=', eq)
                if match:
                    coef1, coef2 = match.groups()
                    if coef1 == coef2:
                        return True
        
        return False
    
    def apply(self, state) -> None:
        """
        应用模型，推导等轴双曲线性质
        """
        # 添加 a = b 关系
        state.geometric_relations.append("等轴双曲线: a = b")
        
        # 如果已知 a 或 b，补充另一个
        if 'a' in state.parameters and 'b' not in state.parameters:
            state.parameters['b'] = state.parameters['a']
        elif 'b' in state.parameters and 'a' not in state.parameters:
            state.parameters['a'] = state.parameters['b']
        
        # 添加离心率
        if 'e' not in state.parameters:
            state.parameters['e'] = 'sqrt(2)'
            state.geometric_relations.append("等轴双曲线离心率: e = √2")
        
        # 添加渐近线（如果还没有）
        has_asymptote = any('渐近线' in rel for rel in state.geometric_relations)
        if not has_asymptote:
            state.geometric_relations.append("渐近线: y = ±x")
        
        # 如果有 a 和 b，计算 c
        if 'a' in state.parameters and 'b' in state.parameters and 'c' not in state.parameters:
            try:
                a_num = float(state.parameters['a'])
                # 对于等轴双曲线，c² = a² + b² = 2a²
                c_num = (2 * a_num ** 2) ** 0.5
                if c_num == int(c_num):
                    state.parameters['c'] = str(int(c_num))
                else:
                    state.parameters['c'] = str(c_num)
            except:
                state.parameters['c'] = f"sqrt(2)*{state.parameters['a']}"
        
        # 记录已应用的模型
        state.applied_models.append(self.model_id)
