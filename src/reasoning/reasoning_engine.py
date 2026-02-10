"""
推理引擎 (Reasoning Engine)

实现自动数学推理的主逻辑。
"""

import time
from typing import Any, Optional
from src.reasoning.model_selector import ModelSelector
from src.reasoning.reasoning_result import ReasoningResult
from src.reasoning.answer_extractor import AnswerExtractor
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
        completeness_threshold: float = 0.99,
        min_steps: int = 1,
        max_retries_per_step: int = 3,
        verbose: bool = True
    ):
        """
        初始化推理引擎
        
        Args:
            theorem_library: 定理库
            model_selector: 模型选择器
            state_constructor: 状态构造器
            max_steps: 最大推理步数
            completeness_threshold: 完整度阈值（判断是否完成），默认0.99
            min_steps: 最小推理步数（强制至少推理N步），默认1
            max_retries_per_step: 每步最大重试次数（apply失败时尝试其他模型），默认3
            verbose: 是否打印详细日志
        """
        self.theorem_library = theorem_library
        self.model_selector = model_selector
        self.state_constructor = state_constructor
        self.max_steps = max_steps
        self.completeness_threshold = completeness_threshold
        self.min_steps = min_steps
        self.max_retries_per_step = max_retries_per_step
        self.verbose = verbose
        
        # 初始化答案提取器
        self.answer_extractor = AnswerExtractor()
    
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
            
            # 2. 推理循环（含回溯重试）
            applied_count = 0  # 实际已应用模型的计数
            step = 0
            consecutive_failures = 0  # 连续无法选到可用模型的次数
            
            while step < self.max_steps:
                step += 1
                
                # 检查是否完成
                if self._is_complete(abstract_state, applied_count):
                    if self.verbose:
                        print(f"[步骤 {step}] 推理完成！(已推理{applied_count}步)")
                    result.success = True
                    break
                
                # 选择并应用模型（带重试）
                step_success = False
                step_excluded = set()  # 本步额外排除的模型（apply失败的）
                
                for retry in range(self.max_retries_per_step):
                    # 选择模型
                    selected_model, selection_info = self.model_selector.select(
                        symbolic_state=symbolic_state,
                        abstract_state=abstract_state,
                        excluded_models=step_excluded
                    )
                    
                    if selected_model is None:
                        if self.verbose and retry == 0:
                            print(f"[步骤 {step}] ✗ 无可用模型")
                        break  # 没有候选了，退出重试
                    
                    if self.verbose:
                        retry_tag = f" (重试{retry})" if retry > 0 else ""
                        print(f"[步骤 {step}]{retry_tag} 选中: Model {selected_model.model_id} - {selected_model.name}", end="")
                        if 'predicted_confidence' in selection_info:
                            print(f" (置信度:{selection_info['predicted_confidence']:.3f})")
                        else:
                            print()
                    
                    # 应用模型
                    try:
                        apply_result = selected_model.apply(symbolic_state)
                        if apply_result is None:
                            apply_result = True
                        
                        if apply_result:
                            # 应用成功
                            abstract_state = self.state_constructor.update_abstract_state(
                                symbolic_state, abstract_state
                            )
                            
                            applied_count += 1
                            result.num_steps = step
                            result.model_sequence.append(selected_model.model_id)
                            result.model_names.append(selected_model.name)
                            result.states.append(abstract_state)
                            result.completeness_scores.append(abstract_state.completeness_score)
                            
                            result.reasoning_trace.append({
                                'step': step,
                                'model_id': selected_model.model_id,
                                'model_name': selected_model.name,
                                'before_completeness': result.completeness_scores[-2],
                                'after_completeness': abstract_state.completeness_score,
                                'retry': retry,
                                **selection_info
                            })
                            
                            if self.verbose:
                                print(f"  ✓ 完整度: {result.completeness_scores[-2]:.3f} → {abstract_state.completeness_score:.3f}")
                            
                            step_success = True
                            consecutive_failures = 0
                            break  # 成功，退出重试
                        else:
                            # apply返回False，将该模型加入本步排除列表，重试
                            step_excluded.add(selected_model.model_id)
                            if self.verbose:
                                print(f"  ✗ apply失败，重试...")
                    
                    except Exception as e:
                        step_excluded.add(selected_model.model_id)
                        if self.verbose:
                            print(f"  ✗ 异常: {str(e)}，重试...")
                
                if not step_success:
                    consecutive_failures += 1
                    # 连续2步都无法推进 → 终止
                    if consecutive_failures >= 2:
                        result.failure_reason = f"Step {step}: No applicable model (consecutive failures)"
                        if self.verbose:
                            print(f"  连续{consecutive_failures}步无法推进，终止")
                        break
            
            # 3. 检查是否达到最大步数
            if step >= self.max_steps and not result.success:
                result.max_steps_reached = True
                result.failure_reason = f"Reached max steps ({self.max_steps})"
                if self.verbose:
                    print(f"[步骤 {step}] 达到最大步数限制")
            
            # 4. 提取答案
            # 即使推理未"完成"，只要应用了模型就尝试提取答案（尽力而为）
            if result.success or applied_count > 0:
                result.answer = self._extract_answer(symbolic_state, query)
                # 如果推理未完成但拿到了有效答案，也视为成功
                if not result.success and result.answer is not None:
                    answer_str = str(result.answer)
                    is_valid = (answer_str and
                                'not found' not in answer_str and
                                'not specified' not in answer_str and
                                answer_str != 'None')
                    if is_valid:
                        result.success = True
                        result.failure_reason = None
                        if self.verbose:
                            print(f"  尽力提取答案成功")
                
                if self.verbose and result.answer is not None:
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
    
    def _is_complete(self, abstract_state: AbstractState, applied_count: int) -> bool:
        """
        判断状态是否完整
        
        必须同时满足：
        1. 完整度达到阈值
        2. 至少已应用了min_steps个模型
        
        Args:
            abstract_state: 抽象状态
            applied_count: 已成功应用的模型数量
        
        Returns:
            bool: 是否完成
        """
        completeness_ok = abstract_state.completeness_score >= self.completeness_threshold
        min_steps_ok = applied_count >= self.min_steps
        return completeness_ok and min_steps_ok
    
    def _extract_answer(
        self,
        symbolic_state: SymbolicState,
        query: str
    ) -> Any:
        """
        从符号状态中提取查询的答案
        
        使用AnswerExtractor智能解析query并提取对应值
        
        Args:
            symbolic_state: 符号状态
            query: 查询表达式
        
        Returns:
            答案（数值、表达式、坐标等）
        """
        return self.answer_extractor.extract(symbolic_state, query)
