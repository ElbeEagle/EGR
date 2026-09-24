"""
Model 12: Hyperbola_Parameter_Relation
双曲线参数关系

公式: c^2 = a^2 + b^2
已知两个参数，求第三个
"""

import re
from ..base_model import TheoremModel


class HyperbolaParameterRelation(TheoremModel):
    """
    双曲线参数关系
    
    前置条件:
    - 实体包含 Hyperbola 类型
    - a, b, c 中至少有两个已知
    
    输出:
    - parameters: 缺失的参数 (a, b, 或 c)
    - geometric_relations: c^2 = a^2 + b^2
    
    示例:
    输入: a=2, b=3
    输出: c=sqrt(13)
    """
    
    def __init__(self):
        super().__init__(
            model_id=12,
            name="Hyperbola_Parameter_Relation",
            chinese_name="双曲线参数关系"
        )
    
    def propose_bound(self, state, action):
        import sympy as sp
        from src.solver.transition_primitives import (
            TransitionError, instantiate_shared_focus, finite_real_solutions,
        )
        from src.theorems.bound_application import Proposal, check_binding, bound_parameters

        from src.theorems.parameter_proposals import PARAMETER_MODES, parameter_proposal
        if action.mode in PARAMETER_MODES:
            return parameter_proposal(state, action)
        if action.mode != 'constrain_shared_focus':
            raise TransitionError('inapplicable', 'Unsupported RM12 mode')
        if not isinstance(state.query, sp.Symbol):
            raise TransitionError('inapplicable', 'Shared-focus parameter solving requires a scalar query')
        fact = check_binding(state, action)
        a_sq, b_sq = bound_parameters(state, action.curve, fact.fact_id)
        bound_parameters(state, action.peer_curve, action.peer_equation_id)
        peer_key = (action.peer_curve, 'c_sq')
        if peer_key not in state.properties:
            raise TransitionError('inapplicable', 'Missing peer focal parameter; apply RM11 first')
        c_sq, relation_operation = instantiate_shared_focus(
            state.relations[action.relation_id], action.curve, action.peer_curve,
            state.frames[action.curve], state.frames[action.peer_curve], state.properties[peer_key],
        )
        equation = sp.cancel(c_sq - a_sq - b_sq)
        operations = [relation_operation, {'operation': 'hyperbola_parameter_relation',
                                           'curve': action.curve, 'expression': equation}]
        reads = (fact.fact_id, action.peer_equation_id, action.relation_id,
                 f'frame:{action.curve}', f'frame:{action.peer_curve}',
                 f'property:{action.curve}:a_sq', f'property:{action.curve}:b_sq',
                 f'property:{action.peer_curve}:a_sq', f'property:{action.peer_curve}:b_sq',
                 f'property:{action.peer_curve}:c_sq', *state.constraints.keys())
        values, candidates = {}, ()
        if state.query in state.values:
            if sp.simplify(equation.subs(state.values)) != 0:
                raise TransitionError('conflict', 'Known value violates shared-focus relation')
        else:
            candidates = finite_real_solutions(
                equation.subs(state.values), state.query,
                [c.subs(state.values) for c in state.constraints.values()], trace=operations)
            operations.append({'operation': 'solve_and_filter', 'target': state.query,
                               'candidates': candidates})
            if not candidates:
                raise TransitionError('conflict', 'No shared-focus solution satisfies conditions')
            if len(candidates) == 1:
                values[state.query] = candidates[0]
        return Proposal(properties={(action.curve, 'c_sq'): c_sq}, values=values,
                        read_facts=reads, operations=operations, candidates=candidates)

    def can_apply(self, state) -> bool:
        """
        检查是否可应用
        
        条件:
        1. 存在 Hyperbola 实体
        2. a, b, c 中至少有两个已知
        """
        # 条件1: 检查是否有双曲线实体
        has_hyperbola = any(
            entity_type.lower() == 'hyperbola'
            for entity_type in state.entities.values()
        )
        if not has_hyperbola:
            return False
        
        # 条件2: 检查参数
        params = state.parameters
        known_count = 0
        if 'a' in params or 'a^2' in params:
            known_count += 1
        if 'b' in params or 'b^2' in params:
            known_count += 1
        if 'c' in params or 'c^2' in params:
            known_count += 1
        
        return known_count >= 2
    
    def apply(self, state) -> bool:
        """
        应用模型，计算缺失的参数
        
        Returns:
            bool: 应用是否成功
        """
        try:
            params = state.parameters
            
            # 获取已知参数
            a_val = params.get('a')
            b_val = params.get('b')
            c_val = params.get('c')
            
            # 情况1: 已知a和b，求c
            # c^2 = a^2 + b^2
            if a_val and b_val and not c_val:
                c_expr = f"sqrt({a_val}^2 + {b_val}^2)"
                
                try:
                    a_num = self._eval_expr(a_val)
                    b_num = self._eval_expr(b_val)
                    c_num_sq = a_num**2 + b_num**2
                    c_num = c_num_sq ** 0.5
                    if c_num == int(c_num):
                        params['c'] = str(int(c_num))
                    else:
                        params['c'] = f"sqrt({int(c_num_sq)})"
                except Exception:
                    params['c'] = c_expr
                
                state.geometric_relations.append(f"c^2 = {a_val}^2 + {b_val}^2")
            
            # 情况2: 已知a和c，求b
            # b^2 = c^2 - a^2
            elif a_val and c_val and not b_val:
                b_expr = f"sqrt({c_val}^2 - {a_val}^2)"
                
                try:
                    a_num = self._eval_expr(a_val)
                    c_num = self._eval_expr(c_val)
                    b_num_sq = c_num**2 - a_num**2
                    if b_num_sq >= 0:
                        b_num = b_num_sq ** 0.5
                        if b_num == int(b_num):
                            params['b'] = str(int(b_num))
                        else:
                            params['b'] = f"sqrt({int(b_num_sq)})"
                    else:
                        params['b'] = b_expr
                except Exception:
                    params['b'] = b_expr
                
                state.geometric_relations.append(f"b^2 = {c_val}^2 - {a_val}^2")
            
            # 情况3: 已知b和c，求a
            # a^2 = c^2 - b^2
            elif b_val and c_val and not a_val:
                a_expr = f"sqrt({c_val}^2 - {b_val}^2)"
                
                try:
                    b_num = self._eval_expr(b_val)
                    c_num = self._eval_expr(c_val)
                    a_num_sq = c_num**2 - b_num**2
                    if a_num_sq >= 0:
                        a_num = a_num_sq ** 0.5
                        if a_num == int(a_num):
                            params['a'] = str(int(a_num))
                        else:
                            params['a'] = f"sqrt({int(a_num_sq)})"
                    else:
                        params['a'] = a_expr
                except Exception:
                    params['a'] = a_expr
                
                state.geometric_relations.append(f"a^2 = {c_val}^2 - {b_val}^2")
            
            # 记录已应用的模型
            state.applied_models.append(self.model_id)
            return True
            
        except Exception:
            return False
    
    def _eval_expr(self, expr: str) -> float:
        """
        计算表达式的数值
        
        支持：
        - 数字: "2", "3.5"
        - 平方根: "sqrt(5)"
        """
        expr = str(expr).strip()
        
        # 纯数字
        try:
            return float(expr)
        except:
            pass
        
        # sqrt形式
        match = re.match(r'sqrt\((\d+(?:\.\d+)?)\)', expr)
        if match:
            num = float(match.group(1))
            return num ** 0.5
        
        raise ValueError(f"Cannot evaluate: {expr}")
