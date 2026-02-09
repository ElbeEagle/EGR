"""
推理结果数据结构

定义推理引擎的输出格式。
"""

from dataclasses import dataclass, field
from typing import Any, List, Dict, Optional
from src.state.abstract_state import AbstractState


@dataclass
class ReasoningResult:
    """
    推理结果数据结构
    
    包含推理过程的完整信息：成功状态、答案、推理路径等。
    """
    
    # 基本信息
    success: bool = False
    """是否成功求解"""
    
    answer: Optional[Any] = None
    """最终答案（如果成功）"""
    
    # 推理过程
    num_steps: int = 0
    """实际推理步数"""
    
    model_sequence: List[int] = field(default_factory=list)
    """应用的模型ID序列"""
    
    model_names: List[str] = field(default_factory=list)
    """应用的模型名称序列"""
    
    # 状态序列
    states: List[AbstractState] = field(default_factory=list)
    """推理过程中的抽象状态序列"""
    
    completeness_scores: List[float] = field(default_factory=list)
    """每步的完整度分数"""
    
    # 详细推理追踪
    reasoning_trace: List[Dict] = field(default_factory=list)
    """
    详细推理过程，每步包含：
    - step: 步骤编号
    - model_id: 应用的模型ID
    - model_name: 模型名称
    - before_completeness: 应用前完整度
    - after_completeness: 应用后完整度
    - neural_confidence: 神经网络预测概率
    - neural_entropy: 预测熵
    - top_k_candidates: Top-K候选模型
    """
    
    # 性能指标
    elapsed_time: float = 0.0
    """总耗时（秒）"""
    
    # 失败信息
    failure_reason: Optional[str] = None
    """失败原因（如果失败）"""
    
    max_steps_reached: bool = False
    """是否达到最大步数限制"""
    
    # 问题信息
    facts: str = ""
    """输入的事实表达式"""
    
    query: str = ""
    """输入的查询表达式"""
    
    def __str__(self) -> str:
        """字符串表示"""
        if self.success:
            return (f"ReasoningResult(success=True, answer={self.answer}, "
                   f"steps={self.num_steps}, time={self.elapsed_time:.2f}s)")
        else:
            return (f"ReasoningResult(success=False, reason={self.failure_reason}, "
                   f"steps={self.num_steps})")
    
    def to_dict(self) -> Dict:
        """转换为字典格式（便于序列化）"""
        return {
            'success': self.success,
            'answer': str(self.answer) if self.answer is not None else None,
            'num_steps': self.num_steps,
            'model_sequence': self.model_sequence,
            'model_names': self.model_names,
            'completeness_scores': self.completeness_scores,
            'reasoning_trace': self.reasoning_trace,
            'elapsed_time': self.elapsed_time,
            'failure_reason': self.failure_reason,
            'max_steps_reached': self.max_steps_reached,
            'facts': self.facts,
            'query': self.query
        }
    
    def get_summary(self) -> str:
        """获取简要总结"""
        lines = []
        lines.append("=" * 60)
        lines.append("推理结果总结")
        lines.append("=" * 60)
        lines.append(f"状态: {'✓ 成功' if self.success else '✗ 失败'}")
        
        if self.success:
            lines.append(f"答案: {self.answer}")
        else:
            lines.append(f"失败原因: {self.failure_reason}")
        
        lines.append(f"步数: {self.num_steps}")
        lines.append(f"耗时: {self.elapsed_time:.2f}秒")
        
        if self.model_names:
            lines.append(f"模型序列: {' → '.join(self.model_names[:5])}")
            if len(self.model_names) > 5:
                lines.append(f"  ... (共{len(self.model_names)}个模型)")
        
        if self.completeness_scores:
            initial = self.completeness_scores[0]
            final = self.completeness_scores[-1]
            lines.append(f"完整度: {initial:.2f} → {final:.2f}")
        
        lines.append("=" * 60)
        return "\n".join(lines)
