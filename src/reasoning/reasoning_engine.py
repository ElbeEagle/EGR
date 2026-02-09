"""
推理引擎 (Reasoning Engine)

实现自动数学推理的主逻辑。
"""

import time
from typing import Any, Optional
from src.reasoning.model_selector import ModelSelector
from src.reasoning.reasoning_result import ReasoningResult
from src.theorems.theorem_library import TheoremLibrary
from src.state.state_constructor import StateConstructor
from src.state.symbolic_state import SymbolicState
from src.state.abstract_state import AbstractState


class ReasoningEngine:
    """
    推理引擎主类
    
    实现自动推理的完整流程：
    1. 构造初始状态
    2. 循环选择并应用模型
    3. 判断是否完成
    4. 提取答案
    """
    
    def __init__(
        self,
        theorem_library: TheoremLibrary,
        model_selector: ModelSelector,
        state_constructor: StateConstructor,
        max_steps: int = 20,
        completeness_threshold: float = 0.95,
        verbose: bool = True
    ):
        """
        初始化推理引擎
        
        Args:
            theorem_library: 定理库
            model_selector: 模型选择器
            state_constructor: 状态构造器
            max_steps: 最大推理步数
            completeness_threshold: 完整度阈值（判断是否完成）
            verbose: 是否打印详细日志
        """
        self.theorem_library = theorem_library
        self.model_selector = model_selector
        self.state_constructor = state_constructor
        self.max_steps = max_steps
        self.completeness_threshold = completeness_threshold
        self.verbose = verbose
    
    def solve(
        self,
        facts: str,
        query: str,
        reasoning_depth: int = 0
    ) -> ReasoningResult:
        """
        求解数学问题
        
        Args:
            facts: 事实表达式（如："G: Ellipse; Expression(G) = (x^2/4 + y^2 = 1)"）
            query: 查询表达式（如："Length(MajorAxis(G))"）
            reasoning_depth: 初始推理深度
        
        Returns:
            ReasoningResult: 推理结果
        """
        start_time = time.time()
        
        # 创建结果对象
        result = ReasoningResult(
            facts=facts,
            query=query
        )
        
        if self.verbose:
            print("=" * 80)
            print("推理引擎启动")
            print("=" * 80)
            print(f"事实: {facts}")
            print(f"查询: {query}")
            print(f"最大步数: {self.max_steps}")
            print("=" * 80)
            print()
        
        try:
            # 1. 构造初始状态
            if self.verbose:
                print("[步骤 0] 构造初始状态...")
            
            abstract_state, symbolic_state = self.state_constructor.construct_from_facts(
                fact_expressions=facts,
                query_expressions=query,
                reasoning_depth=reasoning_depth
            )
            
            # 记录初始状态
            result.states.append(abstract_state)
            result.completeness_scores.append(abstract_state.completeness_score)
            
            if self.verbose:
                print(f"  初始完整度: {abstract_state.completeness_score:.3f}")
                print()
            
            # 2. 推理循环
            step = 0
            while step < self.max_steps:
                step += 1
                
                # 检查是否完成
                if self._is_complete(abstract_state):
                    if self.verbose:
                        print(f"[步骤 {step}] 推理完成！完整度达到阈值")
                    result.success = True
                    break
                
                # 选择模型
                if self.verbose:
                    print(f"[步骤 {step}] 选择模型...")
                
                selected_model, selection_info = self.model_selector.select(
                    symbolic_state=symbolic_state,
                    abstract_state=abstract_state
                )
                
                if selected_model is None:
                    if self.verbose:
                        print(f"  ✗ 无可用模型")
                    result.failure_reason = f"Step {step}: No applicable model found"
                    break
                
                if self.verbose:
                    print(f"  ✓ 选中: Model {selected_model.model_id} - {selected_model.name}")
                    if 'predicted_confidence' in selection_info:
                        print(f"    置信度: {selection_info['predicted_confidence']:.3f}")
                
                # 应用模型
                try:
                    success = selected_model.apply(symbolic_state)
                    
                    if not success:
                        if self.verbose:
                            print(f"  ✗ 模型应用失败")
                        result.failure_reason = f"Step {step}: Model {selected_model.model_id} apply failed"
                        break
                    
                    # 更新抽象状态
                    abstract_state = self.state_constructor.update_abstract_state(
                        symbolic_state,
                        abstract_state
                    )
                    
                    # 记录这一步
                    result.num_steps = step
                    result.model_sequence.append(selected_model.model_id)
                    result.model_names.append(selected_model.name)
                    result.states.append(abstract_state)
                    result.completeness_scores.append(abstract_state.completeness_score)
                    
                    # 详细追踪
                    trace_entry = {
                        'step': step,
                        'model_id': selected_model.model_id,
                        'model_name': selected_model.name,
                        'before_completeness': result.completeness_scores[-2],
                        'after_completeness': abstract_state.completeness_score,
                        **selection_info
                    }
                    result.reasoning_trace.append(trace_entry)
                    
                    if self.verbose:
                        print(f"  ✓ 应用成功")
                        print(f"    完整度: {result.completeness_scores[-2]:.3f} → {abstract_state.completeness_score:.3f}")
                        print()
                
                except Exception as e:
                    if self.verbose:
                        print(f"  ✗ 异常: {str(e)}")
                    result.failure_reason = f"Step {step}: Exception - {str(e)}"
                    break
            
            # 3. 检查是否达到最大步数
            if step >= self.max_steps and not result.success:
                result.max_steps_reached = True
                result.failure_reason = f"Reached max steps ({self.max_steps})"
                if self.verbose:
                    print(f"[步骤 {step}] 达到最大步数限制")
            
            # 4. 提取答案（如果成功）
            if result.success:
                result.answer = self._extract_answer(symbolic_state, query)
                if self.verbose:
                    print()
                    print(f"答案: {result.answer}")
        
        except Exception as e:
            result.success = False
            result.failure_reason = f"Fatal error: {str(e)}"
            if self.verbose:
                print(f"✗ 致命错误: {str(e)}")
        
        # 记录耗时
        result.elapsed_time = time.time() - start_time
        
        if self.verbose:
            print()
            print("=" * 80)
            print(result.get_summary())
        
        return result
    
    def _is_complete(self, abstract_state: AbstractState) -> bool:
        """
        判断状态是否完整
        
        Args:
            abstract_state: 抽象状态
        
        Returns:
            bool: 是否达到完整度阈值
        """
        return abstract_state.completeness_score >= self.completeness_threshold
    
    def _extract_answer(
        self,
        symbolic_state: SymbolicState,
        query: str
    ) -> Any:
        """
        从符号状态中提取查询的答案
        
        Args:
            symbolic_state: 符号状态
            query: 查询表达式
        
        Returns:
            答案（数值、表达式等）
        """
        # TODO: 实现更智能的答案提取逻辑
        # 当前简单实现：尝试从has_parameters中查找
        
        # 简单策略：返回完整度分数作为placeholder
        # 实际应该解析query表达式并从symbolic_state中提取对应值
        
        # 如果有参数，返回参数字典
        if hasattr(symbolic_state, 'has_parameters') and symbolic_state.has_parameters:
            return dict(symbolic_state.has_parameters)
        
        return "Answer extraction not implemented yet"
