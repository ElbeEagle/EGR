"""
答案比较器 (Answer Comparator)

将预测答案和标准答案都尝试数值化，进行模糊比较。
"""

import re
import math
from typing import Any, Union


def compare_answers(predicted: Any, expected: str, tolerance: float = 1e-4) -> bool:
    """
    比较预测答案与标准答案
    
    策略（按优先级）：
    1. 字符串完全匹配
    2. 数值化后比较（误差<tolerance）
    3. 简化后字符串匹配
    
    Args:
        predicted: 预测答案（任意类型）
        expected: 标准答案（字符串）
        tolerance: 数值误差容忍度
    
    Returns:
        bool: 是否匹配
    """
    if predicted is None or expected is None:
        return False
    
    pred_str = str(predicted).strip()
    exp_str = str(expected).strip()
    
    # 策略1: 字符串完全匹配
    if pred_str == exp_str:
        return True
    
    # 策略2: 数值化比较
    pred_num = safe_eval(pred_str)
    exp_num = safe_eval(exp_str)
    
    if pred_num is not None and exp_num is not None:
        if abs(pred_num - exp_num) < tolerance:
            return True
        # 相对误差
        if abs(exp_num) > tolerance and abs(pred_num - exp_num) / abs(exp_num) < tolerance:
            return True
    
    # 策略3: 标准化后比较
    pred_norm = normalize_expr(pred_str)
    exp_norm = normalize_expr(exp_str)
    if pred_norm and exp_norm and pred_norm == exp_norm:
        return True
    
    return False


def safe_eval(expr: str) -> float:
    """
    安全地将表达式计算为数值
    
    支持：
    - 整数/小数: "2", "3.5"
    - 分数: "1/2", "sqrt(3)/2"
    - sqrt: "sqrt(5)", "2*sqrt(3)"
    - 基本运算: "2+3", "4-1", "2*3"
    - pm: "pm*2" → 2 (取正值)
    - 负数: "-3"
    
    Returns:
        float 或 None（无法计算时）
    """
    if expr is None:
        return None
    
    expr = str(expr).strip()
    
    # 空字符串
    if not expr:
        return None
    
    # 跳过明显的非数值（方程、坐标、区间等）
    if any(c in expr for c in ['=', '{', '}', '&', '+oo', '-oo', '[', ']']):
        # 但允许坐标形式 (a, b) 中的逗号
        if '=' in expr or '{' in expr:
            return None
    
    # 预处理
    s = expr
    
    # pm → 取正值
    s = s.replace('pm*', '').replace('pm', '')
    
    # 替换 sqrt
    s = re.sub(r'sqrt\(([^)]+)\)', r'math.sqrt(\1)', s)
    
    # 替换 ^ 为 **
    s = s.replace('^', '**')
    
    # 处理隐式乘法: 2sqrt → 2*sqrt, 数字后接(
    s = re.sub(r'(\d)\s*\*?\s*math\.sqrt', r'\1*math.sqrt', s)
    s = re.sub(r'(\d)\s*\(', r'\1*(', s)
    
    try:
        result = eval(s, {"__builtins__": {}, "math": math}, {})
        return float(result)
    except Exception:
        pass
    
    # 直接尝试float转换
    try:
        return float(expr)
    except Exception:
        pass
    
    return None


def normalize_expr(expr: str) -> str:
    """
    标准化表达式用于字符串比较
    
    - 去除空格
    - 统一 pm 为 ±
    - 去除多余括号
    """
    if not expr:
        return ""
    
    s = str(expr).strip()
    s = s.replace(' ', '')
    s = s.replace('pm*', '±')
    s = s.replace('pm', '±')
    s = s.replace('**', '^')
    
    return s
