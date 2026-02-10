"""
Query解析器 (Query Parser)

解析query表达式，提取操作类型和目标对象
"""

import re
from typing import Dict, Optional, List
from dataclasses import dataclass


@dataclass
class ParsedQuery:
    """解析后的查询结构"""
    operation: str  # 操作类型：Length, Eccentricity, Equation, Coordinate等
    target: Optional[str] = None  # 目标对象：如 "G", "F1"
    nested_operation: Optional[str] = None  # 嵌套操作：如 MajorAxis, Asymptote
    nested_target: Optional[str] = None  # 嵌套目标
    full_expression: str = ""  # 完整表达式


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
        
        # 模式1: 简单变量 "m", "e"
        if re.match(r'^[a-zA-Z]\w*$', query_expr):
            return ParsedQuery(
                operation='Value',
                target=query_expr,
                full_expression=query_expr
            )
        
        # 模式2: 嵌套函数 "Length(MajorAxis(G))"
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
                full_expression=query_expr
            )
        
        # 模式3: 单层函数 "Eccentricity(G)"
        simple_match = re.match(
            r'^(\w+)\(([^)]+)\)$',
            query_expr
        )
        if simple_match:
            operation, target = simple_match.groups()
            return ParsedQuery(
                operation=operation,
                target=target,
                full_expression=query_expr
            )
        
        # 无法解析，返回默认
        return ParsedQuery(
            operation='Unknown',
            full_expression=query_expr
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
