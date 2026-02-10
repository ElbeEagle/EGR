"""
答案提取器 (Answer Extractor)

从SymbolicState中提取查询对应的答案
"""

import re
import math
from typing import Any, Optional, Union, Dict
from src.state.symbolic_state import SymbolicState
from .query_parser import QueryParser, ParsedQuery


class AnswerExtractor:
    """
    答案提取器
    
    根据解析后的query，从symbolic_state中提取对应的答案
    """
    
    def __init__(self):
        self.query_parser = QueryParser()
    
    def extract(
        self,
        symbolic_state: SymbolicState,
        query_expr: str
    ) -> Any:
        """
        提取答案
        
        Args:
            symbolic_state: 符号状态
            query_expr: 查询表达式
        
        Returns:
            答案（数值、字符串、字典等）
        """
        # 解析query
        parsed = self.query_parser.parse(query_expr)
        
        # 根据操作类型提取答案
        if parsed.operation == 'Value':
            return self._extract_value(symbolic_state, parsed)
        elif parsed.operation == 'Eccentricity':
            return self._extract_eccentricity(symbolic_state, parsed)
        elif parsed.operation == 'Length':
            return self._extract_length(symbolic_state, parsed)
        elif parsed.operation == 'Equation':
            return self._extract_equation(symbolic_state, parsed)
        elif parsed.operation == 'Coordinate':
            return self._extract_coordinate(symbolic_state, parsed)
        elif parsed.operation == 'Distance':
            return self._extract_distance(symbolic_state, parsed)
        elif parsed.operation == 'Area':
            return self._extract_area(symbolic_state, parsed)
        elif parsed.operation == 'Angle':
            return self._extract_angle(symbolic_state, parsed)
        else:
            # 未知类型，返回所有可用信息
            return self._extract_all_info(symbolic_state)
    
    def _extract_value(
        self,
        state: SymbolicState,
        parsed: ParsedQuery
    ) -> Any:
        """
        提取简单值 (如 "m", "e")
        
        查找顺序：
        1. parameters中的值
        2. entities中的对象
        """
        target = parsed.target
        
        # 在parameters中查找
        if target in state.parameters:
            return state.parameters[target]
        
        # 在entities中查找
        if target in state.entities:
            return f"{target}: {state.entities[target]}"
        
        # 未找到
        return f"Variable '{target}' not found"
    
    def _extract_eccentricity(
        self,
        state: SymbolicState,
        parsed: ParsedQuery
    ) -> Union[float, str]:
        """
        提取离心率
        
        计算公式：
        - 椭圆/双曲线: e = c/a
        - 抛物线: e = 1
        """
        # 策略1: 直接从参数中查找，尝试数值化
        if 'e' in state.parameters:
            e_val = state.parameters['e']
            try:
                return self._format_number(float(self._evaluate_expression(e_val)))
            except Exception:
                return e_val
        
        # 策略2: 计算 e = c/a
        if 'c' in state.parameters and 'a' in state.parameters:
            try:
                c = float(self._evaluate_expression(state.parameters['c']))
                a = float(self._evaluate_expression(state.parameters['a']))
                e = c / a
                return self._format_number(e)
            except:
                pass
        
        # 策略3: 根据 a, b 计算 c，再算 e
        if 'a' in state.parameters and 'b' in state.parameters:
            try:
                a = float(self._evaluate_expression(state.parameters['a']))
                b = float(self._evaluate_expression(state.parameters['b']))
                
                # 判断曲线类型
                curve_type = self._get_curve_type(state)
                
                if curve_type == 'Ellipse':
                    c = math.sqrt(a**2 - b**2) if a > b else math.sqrt(b**2 - a**2)
                    e = c / max(a, b)
                    return self._format_number(e)
                elif curve_type == 'Hyperbola':
                    c = math.sqrt(a**2 + b**2)
                    e = c / a
                    return self._format_number(e)
            except:
                pass
        
        # 未找到
        return "Eccentricity not found"
    
    def _extract_length(
        self,
        state: SymbolicState,
        parsed: ParsedQuery
    ) -> Union[float, str]:
        """
        提取长度
        
        支持：
        - Length(MajorAxis(G)) → 2a
        - Length(MinorAxis(G)) → 2b
        - Length(ImageinaryAxis(G)) → 2b (双曲线虚轴)
        - Length(RealAxis(G)) → 2a (双曲线实轴)
        - Length(LatusRectum(G)) → 通径长度
        """
        nested_op = parsed.nested_operation
        
        if not nested_op:
            # 无嵌套操作，返回未知
            return "Length target not specified"
        
        # MajorAxis → 2a
        if nested_op in ['MajorAxis', 'RealAxis']:
            if 'a' in state.parameters:
                try:
                    a = float(self._evaluate_expression(state.parameters['a']))
                    return self._format_number(2 * a)
                except:
                    pass
        
        # MinorAxis / ImageinaryAxis → 2b
        elif nested_op in ['MinorAxis', 'ImageinaryAxis', 'ImaginaryAxis']:
            if 'b' in state.parameters:
                try:
                    b = float(self._evaluate_expression(state.parameters['b']))
                    return self._format_number(2 * b)
                except:
                    pass
        
        # LatusRectum (通径) → 椭圆: 2b²/a, 抛物线: 2p
        elif nested_op == 'LatusRectum':
            curve_type = self._get_curve_type(state)
            if curve_type == 'Parabola' and 'p' in state.parameters:
                try:
                    p = float(self._evaluate_expression(state.parameters['p']))
                    return self._format_number(2 * p)
                except:
                    pass
            elif 'a' in state.parameters and 'b' in state.parameters:
                try:
                    a = float(self._evaluate_expression(state.parameters['a']))
                    b = float(self._evaluate_expression(state.parameters['b']))
                    return self._format_number(2 * b**2 / a)
                except:
                    pass
        
        return f"Length({nested_op}) not found"
    
    def _extract_equation(
        self,
        state: SymbolicState,
        parsed: ParsedQuery
    ) -> str:
        """
        提取方程
        
        支持：
        - Equation(Asymptote(G)) → 渐近线方程
        - Equation(Directrix(G)) → 准线方程
        - Equation(Tangent(...)) → 切线方程
        """
        nested_op = parsed.nested_operation
        
        if not nested_op:
            # 返回主方程
            if state.equations:
                return state.equations[0]
            return "No equation found"
        
        # 在方程列表中查找匹配
        for eq in state.equations:
            if nested_op in eq:
                # 提取方程的右侧
                if '=' in eq:
                    parts = eq.split('=', 1)
                    if len(parts) == 2:
                        return parts[1].strip()
                return eq
        
        # 在几何关系中查找
        for rel in state.geometric_relations:
            if nested_op in rel and '=' in rel:
                parts = rel.split('=', 1)
                if len(parts) == 2:
                    return parts[1].strip()
        
        return f"Equation({nested_op}) not found"
    
    def _extract_coordinate(
        self,
        state: SymbolicState,
        parsed: ParsedQuery
    ) -> Union[tuple, str]:
        """
        提取坐标
        
        支持：
        - Coordinate(A) → (x, y)
        - Coordinate(Focus(...)) → 焦点坐标
        """
        target = parsed.target or parsed.nested_target
        
        if not target:
            return "Coordinate target not specified"
        
        # 直接从coordinates字典查找
        if target in state.coordinates:
            return state.coordinates[target]
        
        # 在几何关系中查找
        for rel in state.geometric_relations:
            if f"Coordinate({target})" in rel and '=' in rel:
                match = re.search(r'=\s*\(([^)]+)\)', rel)
                if match:
                    coords_str = match.group(1)
                    coords = tuple(c.strip() for c in coords_str.split(','))
                    return coords
        
        return f"Coordinate({target}) not found"
    
    def _extract_distance(
        self,
        state: SymbolicState,
        parsed: ParsedQuery
    ) -> Union[float, str]:
        """
        提取距离
        """
        # 在几何关系中查找Distance
        for rel in state.geometric_relations:
            if 'Distance' in rel and '=' in rel:
                match = re.search(r'=\s*([^\s;]+)', rel)
                if match:
                    return match.group(1)
        
        return "Distance not found"
    
    def _extract_area(
        self,
        state: SymbolicState,
        parsed: ParsedQuery
    ) -> Union[float, str]:
        """
        提取面积
        """
        # 在几何关系中查找Area
        for rel in state.geometric_relations:
            if 'Area' in rel and '=' in rel:
                match = re.search(r'=\s*([^\s;]+)', rel)
                if match:
                    return match.group(1)
        
        # 如果有参数，尝试计算椭圆面积
        if 'a' in state.parameters and 'b' in state.parameters:
            curve_type = self._get_curve_type(state)
            if curve_type == 'Ellipse':
                try:
                    a = float(self._evaluate_expression(state.parameters['a']))
                    b = float(self._evaluate_expression(state.parameters['b']))
                    area = math.pi * a * b
                    return self._format_number(area)
                except:
                    pass
        
        return "Area not found"
    
    def _extract_angle(
        self,
        state: SymbolicState,
        parsed: ParsedQuery
    ) -> str:
        """
        提取角度
        """
        # 在几何关系中查找Angle
        for rel in state.geometric_relations:
            if 'Angle' in rel and '=' in rel:
                match = re.search(r'=\s*([^\s;]+)', rel)
                if match:
                    return match.group(1)
        
        return "Angle not found"
    
    def _extract_all_info(self, state: SymbolicState) -> Any:
        """
        提取所有可用信息（兜底策略）
        
        尝试返回最可能的单一值，而非整个dict
        """
        params = state.parameters
        
        # 如果只有少量参数，返回最后添加的（通常是推理结果）
        if params:
            # 优先返回常见结果参数
            for key in ['e', 'c', 'k', 'm', 'n', 't', 'p', 'S', 'area', 'result']:
                if key in params:
                    try:
                        return self._format_number(float(self._evaluate_expression(params[key])))
                    except Exception:
                        return params[key]
            
            # 返回最后一个参数值
            last_key = list(params.keys())[-1]
            try:
                return self._format_number(float(self._evaluate_expression(params[last_key])))
            except Exception:
                return params[last_key]
        
        return None
    
    # ===== 辅助方法 =====
    
    def _get_curve_type(self, state: SymbolicState) -> str:
        """获取曲线类型"""
        for entity_type in state.entities.values():
            if entity_type in ['Ellipse', 'Hyperbola', 'Parabola', 'Circle']:
                return entity_type
        return 'Unknown'
    
    def _evaluate_expression(self, expr: str) -> float:
        """
        安全地计算表达式
        
        支持：
        - 数字: "2", "3.5"
        - sqrt: "sqrt(3)", "sqrt(2)"
        - 简单运算: "2*3", "4/2"
        - 复合: "sqrt(2^2 - 1^2)", "sqrt(4 + 9)"
        - 嵌套: "sqrt(2^2 + 3^2)/2"
        """
        expr = str(expr).strip()
        
        # 替换 ^ 为 **
        expr = expr.replace('^', '**')
        
        # 替换sqrt为math.sqrt
        expr = re.sub(r'sqrt\(([^)]+)\)', r'math.sqrt(\1)', expr)
        
        # 处理隐式乘法: 2math.sqrt → 2*math.sqrt
        expr = re.sub(r'(\d)\s*math\.sqrt', r'\1*math.sqrt', expr)
        
        try:
            result = eval(expr, {"__builtins__": {}, "math": math}, {})
            return float(result)
        except Exception:
            # 无法计算，尝试直接转换
            return float(expr)
    
    def _format_number(self, num: float, precision: int = 6) -> Union[int, float, str]:
        """
        格式化数字
        
        - 整数返回int
        - 小数保留precision位
        - 特殊值返回字符串
        """
        # 检查是否为整数
        if abs(num - round(num)) < 1e-9:
            return int(round(num))
        
        # 保留精度
        formatted = round(num, precision)
        
        # 去除尾部0
        if isinstance(formatted, float):
            return float(f"{formatted:.{precision}g}")
        
        return formatted
