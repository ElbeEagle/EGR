#!/usr/bin/env python3
"""
分析Conic10K训练集，提取常用定理和推理模式
"""

import json
import re
from collections import Counter, defaultdict

def load_data(filepath):
    """加载数据"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def extract_theorem_patterns(process_text):
    """从推理过程中提取定理模式"""
    patterns = []
    
    # 模式1: 参数关系
    if re.search(r'a\^?\{?2\}?\s*[=+-]\s*b\^?\{?2\}?\s*[+-]\s*c\^?\{?2\}?', process_text):
        patterns.append('param_relation_abc')
    
    # 模式2: 离心率公式
    if re.search(r'e\s*=\s*\\?frac\{c\}\{a\}', process_text):
        patterns.append('eccentricity_formula')
    
    # 模式3: 渐近线
    if re.search(r'渐近线', process_text):
        patterns.append('asymptote')
    
    # 模式4: 焦点
    if re.search(r'焦点', process_text):
        patterns.append('focus')
    
    # 模式5: 标准方程/参数提取
    if re.search(r'\\frac\{x\^?\{?2\}?\}\{[0-9a-z]+\}', process_text):
        patterns.append('standard_equation')
    
    # 模式6: 抛物线定义
    if re.search(r'准线|抛物线.*距离', process_text):
        patterns.append('parabola_definition')
    
    # 模式7: 双曲线定义
    if re.search(r'双曲线定义|2a', process_text):
        patterns.append('hyperbola_definition')
    
    # 模式8: 椭圆定义
    if re.search(r'椭圆定义|\|.*\+.*\|.*=.*2a', process_text):
        patterns.append('ellipse_definition')
    
    # 模式9: 代入/求解
    if re.search(r'代入|解得|求得', process_text):
        patterns.append('substitution_solve')
    
    # 模式10: 距离公式
    if re.search(r'距离公式|\\sqrt\{.*\^2.*\+.*\^2', process_text):
        patterns.append('distance_formula')
    
    # 模式11: 中点公式
    if re.search(r'中点', process_text):
        patterns.append('midpoint')
    
    # 模式12: 斜率
    if re.search(r'斜率|k\s*=', process_text):
        patterns.append('slope')
    
    # 模式13: 垂直/垂线
    if re.search(r'垂直|垂线|\\bot', process_text):
        patterns.append('perpendicular')
    
    # 模式14: 切线
    if re.search(r'切线|相切', process_text):
        patterns.append('tangent')
    
    # 模式15: 焦半径
    if re.search(r'焦半径|焦点弦', process_text):
        patterns.append('focal_radius')
    
    return patterns

def analyze_query_types(data):
    """分析查询类型分布"""
    query_types = Counter()
    
    for item in data:
        query = item.get('query_expressions', '')
        
        if 'Eccentricity' in query:
            query_types['eccentricity'] += 1
        elif 'Expression' in query:
            query_types['equation'] += 1
        elif 'Coordinate' in query:
            query_types['coordinate'] += 1
        elif 'Distance' in query or 'Abs' in query:
            query_types['distance'] += 1
        elif 'Range' in query:
            query_types['range'] += 1
        elif 'Length' in query:
            query_types['length'] += 1
        elif 'Area' in query:
            query_types['area'] += 1
        else:
            query_types['other'] += 1
    
    return query_types

def analyze_curve_types(data):
    """分析曲线类型分布"""
    curve_types = Counter()
    
    for item in data:
        facts = item.get('fact_expressions', '')
        
        if 'Ellipse' in facts:
            curve_types['Ellipse'] += 1
        if 'Hyperbola' in facts:
            curve_types['Hyperbola'] += 1
        if 'Parabola' in facts:
            curve_types['Parabola'] += 1
        if 'Circle' in facts:
            curve_types['Circle'] += 1
    
    return curve_types

def main():
    print("="*80)
    print("Conic10K 定理模式分析")
    print("="*80)
    
    # 加载数据
    data = load_data('Conic10K/conic10k/train.json')
    print(f"\n总样本数: {len(data)}")
    
    # 分析有process的样本
    samples_with_process = [item for item in data if item.get('process', '').strip()]
    print(f"有推理过程的样本: {len(samples_with_process)} ({len(samples_with_process)/len(data)*100:.1f}%)")
    
    # 提取定理模式
    print("\n" + "-"*80)
    print("定理模式使用频率统计")
    print("-"*80)
    
    all_patterns = []
    for item in samples_with_process:
        patterns = extract_theorem_patterns(item['process'])
        all_patterns.extend(patterns)
    
    pattern_counter = Counter(all_patterns)
    
    print(f"\n{'定理模式':<30} {'出现次数':<10} {'占比'}")
    print("-"*60)
    for pattern, count in pattern_counter.most_common(20):
        percentage = count / len(samples_with_process) * 100
        print(f"{pattern:<30} {count:<10} {percentage:.1f}%")
    
    # 分析查询类型
    print("\n" + "-"*80)
    print("查询类型分布")
    print("-"*80)
    
    query_types = analyze_query_types(data)
    print(f"\n{'查询类型':<20} {'数量':<10} {'占比'}")
    print("-"*50)
    for qtype, count in query_types.most_common():
        percentage = count / len(data) * 100
        print(f"{qtype:<20} {count:<10} {percentage:.1f}%")
    
    # 分析曲线类型
    print("\n" + "-"*80)
    print("曲线类型分布")
    print("-"*80)
    
    curve_types = analyze_curve_types(data)
    print(f"\n{'曲线类型':<20} {'数量':<10} {'占比'}")
    print("-"*50)
    for ctype, count in curve_types.most_common():
        percentage = count / len(data) * 100
        print(f"{ctype:<20} {count:<10} {percentage:.1f}%")
    
    # 保存结果
    results = {
        'total_samples': len(data),
        'samples_with_process': len(samples_with_process),
        'theorem_patterns': dict(pattern_counter.most_common()),
        'query_types': dict(query_types),
        'curve_types': dict(curve_types)
    }
    
    with open('outputs/theorem_analysis.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print("\n" + "="*80)
    print("分析完成！结果已保存到: outputs/theorem_analysis.json")
    print("="*80)

if __name__ == '__main__':
    main()

