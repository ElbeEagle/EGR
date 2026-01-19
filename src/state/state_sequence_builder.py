"""
状态序列构建器

功能：从初始状态s0开始，应用模型序列，构建完整的状态转换序列
"""

from typing import List, Tuple, Dict, Any, Optional
from dataclasses import dataclass
from .symbolic_state import SymbolicState
from .abstract_state import AbstractState
from .state_constructor import StateConstructor


@dataclass
class StateTransition:
    """
    状态转换记录
    """
    step: int  # 推理步数
    model_id: Optional[int]  # 应用的模型ID（None表示初始状态）
    model_name: Optional[str]  # 模型名称
    symbolic_state: SymbolicState  # 符号状态
    abstract_state: AbstractState  # 抽象状态
    status: str  # 状态：'success', 'skipped', 'failed'
    error_message: Optional[str] = None  # 错误信息


class StateSequenceBuilder:
    """
    状态序列构建器
    
    功能：
    1. 构建从s0到sN的完整状态序列
    2. 处理未实现模型（跳过）
    3. 记录详细的转换信息
    """
    
    def __init__(self, theorem_library, state_constructor: StateConstructor):
        """
        初始化
        
        Args:
            theorem_library: 定理库实例
            state_constructor: 状态构造器实例
        """
        self.theorem_library = theorem_library
        self.state_constructor = state_constructor
    
    def build_sequence(
        self,
        fact_expressions: str,
        query_expressions: str,
        model_ids: List[int]
    ) -> List[StateTransition]:
        """
        构建完整的状态序列
        
        Args:
            fact_expressions: 事实表达式
            query_expressions: 查询表达式
            model_ids: 要应用的模型ID序列
        
        Returns:
            状态转换列表，包含每一步的详细信息
        """
        transitions = []
        
        # ===== 步骤0: 构建初始状态 =====
        try:
            symbolic_s0 = self.state_constructor._parse_fact_expressions(fact_expressions)
            abstract_s0 = self.state_constructor._construct_abstract_features(
                symbolic_s0,
                query_expressions,
                reasoning_depth=0
            )
            
            # 记录初始状态
            transitions.append(StateTransition(
                step=0,
                model_id=None,
                model_name="Initial State",
                symbolic_state=symbolic_s0.copy(),
                abstract_state=abstract_s0,
                status='success'
            ))
        except Exception as e:
            # 初始状态构建失败
            transitions.append(StateTransition(
                step=0,
                model_id=None,
                model_name="Initial State",
                symbolic_state=SymbolicState(),
                abstract_state=AbstractState(),
                status='failed',
                error_message=str(e)
            ))
            return transitions
        
        # ===== 步骤1-N: 逐步应用模型 =====
        current_symbolic = symbolic_s0
        
        for i, model_id in enumerate(model_ids):
            step = i + 1
            
            # 获取模型
            model = self.theorem_library.get_model(model_id)
            
            if model is None:
                # 模型未实现
                transitions.append(StateTransition(
                    step=step,
                    model_id=model_id,
                    model_name=f"Model_{model_id} (Not Implemented)",
                    symbolic_state=current_symbolic.copy(),
                    abstract_state=self.state_constructor._construct_abstract_features(
                        current_symbolic,
                        query_expressions,
                        reasoning_depth=step
                    ),
                    status='skipped',
                    error_message=f'Model {model_id} not implemented'
                ))
                continue
            
            # 应用模型
            try:
                # 检查前置条件
                if not model.can_apply(current_symbolic):
                    # 前置条件不满足
                    transitions.append(StateTransition(
                        step=step,
                        model_id=model_id,
                        model_name=model.name,
                        symbolic_state=current_symbolic.copy(),
                        abstract_state=self.state_constructor._construct_abstract_features(
                            current_symbolic,
                            query_expressions,
                            reasoning_depth=step
                        ),
                        status='failed',
                        error_message='Precondition not satisfied'
                    ))
                    continue
                
                # 应用模型（会修改current_symbolic）
                model.apply(current_symbolic)
                
                # 构建新的抽象状态
                new_abstract = self.state_constructor._construct_abstract_features(
                    current_symbolic,
                    query_expressions,
                    reasoning_depth=step
                )
                
                # 记录成功转换
                transitions.append(StateTransition(
                    step=step,
                    model_id=model_id,
                    model_name=model.name,
                    symbolic_state=current_symbolic.copy(),
                    abstract_state=new_abstract,
                    status='success'
                ))
                
            except Exception as e:
                # 模型应用出错
                transitions.append(StateTransition(
                    step=step,
                    model_id=model_id,
                    model_name=model.name if model else f"Model_{model_id}",
                    symbolic_state=current_symbolic.copy(),
                    abstract_state=self.state_constructor._construct_abstract_features(
                        current_symbolic,
                        query_expressions,
                        reasoning_depth=step
                    ),
                    status='failed',
                    error_message=str(e)
                ))
        
        return transitions
    
    def analyze_sequence(self, transitions: List[StateTransition]) -> Dict[str, Any]:
        """
        分析状态序列
        
        Args:
            transitions: 状态转换列表
        
        Returns:
            分析结果字典
        """
        total_steps = len(transitions) - 1  # 减去初始状态
        success_steps = sum(1 for t in transitions[1:] if t.status == 'success')
        skipped_steps = sum(1 for t in transitions[1:] if t.status == 'skipped')
        failed_steps = sum(1 for t in transitions[1:] if t.status == 'failed')
        
        # 检查completeness单调性
        completeness_values = [t.abstract_state.completeness_score for t in transitions]
        is_monotonic = all(
            completeness_values[i] <= completeness_values[i+1]
            for i in range(len(completeness_values) - 1)
        )
        
        # 计算参数增长
        param_counts = [len(t.symbolic_state.parameters) for t in transitions]
        
        return {
            'total_steps': total_steps,
            'success_steps': success_steps,
            'skipped_steps': skipped_steps,
            'failed_steps': failed_steps,
            'success_rate': success_steps / total_steps if total_steps > 0 else 0.0,
            'completeness_monotonic': is_monotonic,
            'initial_completeness': completeness_values[0] if completeness_values else 0.0,
            'final_completeness': completeness_values[-1] if completeness_values else 0.0,
            'completeness_gain': completeness_values[-1] - completeness_values[0] if completeness_values else 0.0,
            'initial_param_count': param_counts[0] if param_counts else 0,
            'final_param_count': param_counts[-1] if param_counts else 0,
            'param_gain': param_counts[-1] - param_counts[0] if param_counts else 0
        }
