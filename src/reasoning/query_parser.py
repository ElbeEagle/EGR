"""
Query解析器 (Query Parser)

解析query表达式，提取操作类型和目标对象
"""

import re
from typing import Optional, List
from dataclasses import dataclass


@dataclass
class ParsedQuery:
    """解析后的查询结构"""
    operation: str  # 操作类型：Length, Eccentricity, Equation, Coordinate等
    target: Optional[str] = None  # 目标对象：如 "G", "F1"
    nested_operation: Optional[str] = None  # 嵌套操作：如 MajorAxis, Asymptote
    nested_target: Optional[str] = None  # 嵌套目标
    full_expression: str = ""  # 完整表达式
    arguments: List[str] = None  # 顶层参数列表


class QueryParser:
    """
    Query表达式解析器
    
    支持的表达式格式：
    1. 简单值: "m", "e"
    2. 单层函数: "Eccentricity(G)", "Coordinate(A)"
    3. 嵌套函数: "Length(MajorAxis(G))", "Equation(Asymptote(G))"
    """
    
    def parse(self, query_expr: str) -> ParsedQuery:
        """
        解析query表达式
        
        Args:
            query_expr: 查询表达式
        
        Returns:
            ParsedQuery: 解析结果
        
        Examples:
            >>> parser.parse("m")
            ParsedQuery(operation='Value', target='m')
            
            >>> parser.parse("Eccentricity(G)")
            ParsedQuery(operation='Eccentricity', target='G')
            
            >>> parser.parse("Length(MajorAxis(G))")
            ParsedQuery(operation='Length', 
                       nested_operation='MajorAxis', 
                       nested_target='G')
        """
        query_expr = query_expr.strip()
        top_level_parts = self._split_top_level(query_expr, [';', '\n'])
        if len(top_level_parts) > 1:
            return ParsedQuery(
                operation='MultiQuery',
                full_expression=query_expr,
                arguments=top_level_parts
            )
        
        # 模式1: 简单变量 "m", "e"
        if re.match(r'^[a-zA-Z]\w*$', query_expr):
            return ParsedQuery(
                operation='Value',
                target=query_expr,
                full_expression=query_expr,
                arguments=[query_expr]
            )

        # 模式2: 顶层函数调用，支持多层嵌套和多个参数
        function_call = self._parse_function_call(query_expr)
        if function_call:
            operation, args = function_call
            parsed = ParsedQuery(
                operation=operation,
                target=args[0] if args else None,
                full_expression=query_expr,
                arguments=args
            )
            if args:
                nested_call = self._parse_function_call(args[0])
                if nested_call:
                    nested_operation, nested_args = nested_call
                    parsed.nested_operation = nested_operation
                    parsed.nested_target = nested_args[0] if nested_args else None
            return parsed
        
        # 兼容旧模式: 嵌套函数 "Length(MajorAxis(G))"
        nested_match = re.match(
            r'^(\w+)\((\w+)\(([^)]+)\)\)$',
            query_expr
        )
        if nested_match:
            outer_op, inner_op, target = nested_match.groups()
            return ParsedQuery(
                operation=outer_op,
                nested_operation=inner_op,
                nested_target=target,
                full_expression=query_expr,
                arguments=[f"{inner_op}({target})"]
            )
        
        # 兼容旧模式: 单层函数 "Eccentricity(G)"
        simple_match = re.match(
            r'^(\w+)\(([^)]+)\)$',
            query_expr
        )
        if simple_match:
            operation, target = simple_match.groups()
            return ParsedQuery(
                operation=operation,
                target=target,
                full_expression=query_expr,
                arguments=[target]
            )

        # 模式4: 代数表达式 "b/a", "x1^2+2*y1"
        if any(op in query_expr for op in ['+', '-', '*', '/', '^']):
            return ParsedQuery(
                operation='AlgebraicExpression',
                target=query_expr,
                full_expression=query_expr,
                arguments=[query_expr]
            )
        
        # 无法解析，返回默认
        return ParsedQuery(
            operation='Unknown',
            full_expression=query_expr,
            arguments=[]
        )
    
    def extract_all_variables(self, query_expr: str) -> List[str]:
        """
        提取表达式中的所有变量名
        
        Args:
            query_expr: 查询表达式
        
        Returns:
            List[str]: 变量名列表
        
        Example:
            >>> parser.extract_all_variables("Length(MajorAxis(G))")
            ['G']
        """
        # 提取所有标识符（字母开头的单词）
        matches = re.findall(r'\b[a-zA-Z]\w*\b', query_expr)
        
        # 过滤掉函数名（首字母大写的）
        variables = [m for m in matches if not m[0].isupper()]
        
        return list(set(variables))

    def _parse_function_call(self, expr: str) -> Optional[tuple]:
        """解析顶层函数调用，参数按顶层逗号切分。"""
        match = re.match(r'^(\w+)\(', expr)
        if not match or not expr.endswith(')'):
            return None
        open_index = expr.find('(')
        if self._find_matching_paren(expr, open_index) != len(expr) - 1:
            return None
        op = match.group(1)
        inner = expr[open_index + 1:-1]
        return op, self._split_top_level(inner, [','])

    def _find_matching_paren(self, text: str, open_index: int) -> int:
        depth = 0
        for idx in range(open_index, len(text)):
            char = text[idx]
            if char == '(':
                depth += 1
            elif char == ')':
                depth -= 1
                if depth == 0:
                    return idx
        return -1

    def _split_top_level(self, text: str, separators: List[str]) -> List[str]:
        parts = []
        depth = 0
        start = 0
        for idx, char in enumerate(text):
            if char in '([{':
                depth += 1
            elif char in ')]}':
                depth = max(0, depth - 1)
            elif depth == 0 and char in separators:
                part = text[start:idx].strip()
                if part:
                    parts.append(part)
                start = idx + 1
        tail = text[start:].strip()
        if tail:
            parts.append(tail)
        return parts
