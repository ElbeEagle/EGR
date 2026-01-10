#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将推理过程转换为模型ID序列
基于关键词、公式模式和数学表达式的精确识别
"""

import re
import json
from collections import Counter

def identify_models_in_process(process_text):
    """
    识别推理过程中使用的所有模型
    返回按使用顺序排列的模型ID列表
    """
    models = []
    text = process_text.lower()
    
    # 1. 曲线定义 (0-2) - 极高优先级
    if re.search(r'(椭圆.*定义|两焦点.*距离.*和|pf[_₁₂]*.*\+.*pf[_₁₂]*.*=.*2a)', process_text):
        models.append(0)
    if re.search(r'(双曲线.*定义|两焦点.*距离.*差|\|pf[_₁₂]*\|.*-.*\|pf[_₁₂]*\|.*=.*2a)', process_text):
        models.append(1)
    if re.search(r'(抛物线.*定义|到焦点.*距离.*到.*准线|pf.*=.*p[a-z]|准线.*距离)', process_text):
        models.append(2)
    
    # 2. 标准方程 (3-10)
    # 椭圆
    if re.search(r'\\frac\{x\^\{2\}\}\{[^}]+\}\s*\+\s*\\frac\{y\^\{2\}\}\{[^}]+\}\s*=\s*1', process_text):
        if '焦点在x轴' in process_text or 'm>4' in process_text or 'm-' in process_text:
            models.append(3)
        elif '焦点在y轴' in process_text:
            models.append(4)
        else:
            models.append(3)  # 默认焦点在x轴
    
    # 双曲线
    if re.search(r'\\frac\{x\^\{2\}\}\{[^}]+\}\s*-\s*\\frac\{y\^?\{2\}\}\{[^}]+\}\s*=\s*1', process_text):
        if '焦点在y轴' in process_text:
            models.append(6)
        else:
            models.append(5)
    if re.search(r'\\frac\{y\^?\{2\}\}\{[^}]+\}\s*-\s*\\frac\{x\^?\{2\}\}\{[^}]+\}\s*=\s*1', process_text):
        models.append(6)
    
    # 抛物线
    if re.search(r'(y\^?\{?2\}?\s*=\s*[^x]*x|y2\s*=.*x)', process_text) and '(' not in process_text.split('y')[0][-5:]:
        if '-' in process_text and 'y^{2}=-' in process_text:
            models.append(8)  # 开口向左
        else:
            models.append(7)  # 开口向右
    if re.search(r'x\^?\{?2\}?\s*=\s*[^y]*y', process_text):
        if '-' in process_text and 'x^{2}=-' in process_text:
            models.append(10)  # 开口向下
        else:
            models.append(9)  # 开口向上
    
    # 3. 参数关系与离心率 (11-15)
    if re.search(r'(a\^?\{?2\}?\s*=\s*b\^?\{?2\}?\s*\+\s*c\^?\{?2\}?|b\^?\{?2\}?\s*=\s*a\^?\{?2\}?\s*-\s*c\^?\{?2\}?)', process_text):
        if '双曲线' not in process_text:
            models.append(11)  # 椭圆参数关系
    if re.search(r'c\^?\{?2\}?\s*=\s*a\^?\{?2\}?\s*\+\s*b\^?\{?2\}?', process_text):
        models.append(12)  # 双曲线参数关系
    if re.search(r'(离心率|e\s*=\s*\\frac\{c\}\{a\})', process_text):
        models.append(13)
    
    # 4. 焦半径与通径 (16-20)
    if re.search(r'(\|pf\|.*=.*a.*±.*ex|焦半径.*椭圆)', process_text):
        models.append(16)
    if re.search(r'(x.*\+.*\\frac\{p\}\{2\}|焦半径.*抛物线)', process_text):
        models.append(17)
    if re.search(r'\\frac\{2b\^?\{?2\}?\}\{a\}', process_text):
        if '椭圆' in process_text or '通径' in process_text:
            models.append(18)  # 椭圆通径
        if '双曲线' in process_text:
            models.append(19)  # 双曲线通径
    if re.search(r'通径.*2p', process_text):
        models.append(20)
    
    # 5. 渐近线相关 (21-24)
    if re.search(r'渐近线', process_text):
        models.append(21)
        if re.search(r'(焦点.*渐近线.*距离.*=.*b|d\s*=\s*b)', process_text):
            models.append(22)
    if '等轴双曲线' in process_text or ('a=b' in text and '双曲线' in process_text):
        models.append(24)
    
    # 6. 准线 (29)
    if re.search(r'准线', process_text):
        models.append(29)
    
    # 7. 焦点三角形 (30-32)
    if re.search(r'(焦点三角形.*面积|s.*=.*b\^?\{?2\}?.*tan)', process_text):
        if '椭圆' in process_text:
            models.append(30)
        elif '双曲线' in process_text:
            models.append(31)
    if re.search(r'(焦点三角形.*周长|周长.*4a)', process_text):
        models.append(32)
    
    # 8. 抛物线焦点弦 (33-36)
    if re.search(r'(x[_₁₂1]+.*\+.*x[_₁₂2]+.*\+.*p(?![a-z])|焦点弦)', process_text):
        models.append(33)
    if re.search(r'x[_₁₂1]+.*x[_₁₂2]+.*=.*p\^?\{?2\}?/4', process_text):
        models.append(34)
    if re.search(r'y[_₁₂1]+.*y[_₁₂2]+.*=.*-p\^?\{?2\}?', process_text):
        models.append(35)
    
    # 9. 韦达定理 (41-43) - 极高频
    if re.search(r'韦达定理', process_text):
        models.append(41)
    if re.search(r'(x[_₁₂1]+.*\+.*x[_₁₂2]+|y[_₁₂1]+.*\+.*y[_₁₂2]+).*=', process_text):
        if 41 not in models and 42 not in models:
            models.append(42)
    if re.search(r'(x[_₁₂1]+.*x[_₁₂2]+|y[_₁₂1]+.*y[_₁₂2]+).*=', process_text):
        if 41 not in models and 43 not in models:
            models.append(43)
    
    # 10. 点差法 (44-46)
    if re.search(r'(点差法|两式相减|代入.*相减)', process_text):
        models.append(44)
        if '椭圆' in process_text:
            models.append(45)
        elif '双曲线' in process_text:
            models.append(46)
    
    # 11. 三角形定理 (47-49)
    if re.search(r'(余弦定理|cos.*c\^?\{?2\}?.*=.*a\^?\{?2\}?.*\+.*b\^?\{?2\}?)', process_text):
        models.append(47)
    if re.search(r'正弦定理', process_text):
        models.append(48)
    if re.search(r'勾股定理', process_text):
        models.append(49)
    
    # 12. 弦长公式 (50-51)
    if re.search(r'弦长', process_text):
        if re.search(r'\\sqrt.*1.*\+.*k\^?\{?2\}?', process_text):
            models.append(51)
        else:
            models.append(50)
    
    # 13. 距离与坐标 (52-55)
    if re.search(r'点到.*线.*距离', process_text):
        models.append(52)
    if re.search(r'(两点.*距离|\|ab\|.*=.*\\sqrt)', process_text):
        models.append(53)
    if re.search(r'中点', process_text):
        models.append(54)
    if re.search(r'(斜率|k.*=.*\\frac\{y)', process_text):
        models.append(55)
    
    # 14. 三角形面积 (56-58)
    if re.search(r's.*=.*\\frac\{1\}\{2\}.*sin', process_text):
        models.append(57)
    elif re.search(r's.*=.*\\frac\{1\}\{2\}', process_text):
        models.append(56)
    
    # 15. 向量运算 (59-62)
    if re.search(r'\\overrightarrow', process_text):
        if re.search(r'(\\cdot.*=.*x.*x.*\+.*y.*y|数量积)', process_text):
            models.append(59)
        if re.search(r'\\cdot.*=\s*0', process_text) or re.search(r'\\bot', process_text):
            models.append(61)
        if re.search(r'\\overrightarrow.*=.*\\lambda', process_text):
            models.append(62)
    
    # 16. 不等式 (63-64)
    if re.search(r'(基本不等式|≥.*2\\sqrt|\\geqslant.*2\\sqrt)', process_text):
        models.append(63)
    if re.search(r'当且仅当', process_text):
        models.append(64)
    
    # 17. 判别式 (65-67)
    if re.search(r'(判别式|[δΔ]|\\triangle)', process_text):
        models.append(65)
        if re.search(r'([δΔ]|\\triangle).*=\s*0', process_text):
            models.append(66)
        elif re.search(r'([δΔ]|\\triangle).*>\s*0', process_text):
            models.append(67)
    
    # 18. 中位线 (68-69)
    if re.search(r'中位线', process_text):
        if '三角形' in process_text:
            models.append(68)
        elif '梯形' in process_text:
            models.append(69)
    
    # 19. 内切圆和等积法 (70-71)
    if re.search(r'内切圆', process_text):
        models.append(70)
    if re.search(r'等积', process_text):
        models.append(71)
    
    # 20. 直线方程 (72-74)
    if re.search(r'(点斜式|y.*-.*y[_₀].*=.*k)', process_text):
        models.append(72)
    
    # 21. 圆相关 (75-76)
    if re.search(r'\(x.*-.*\)\^?\{?2\}?.*\+.*\(y.*-.*\)\^?\{?2\}?.*=', process_text):
        models.append(75)
    
    # 22. 高级技巧 (77-79)
    if re.search(r'(齐次化|同除以.*a\^?\{?2\}?|两边.*除以)', process_text):
        models.append(77)
    if re.search(r'x\s*=\s*my\s*\+|x\s*=\s*ty\s*\+', process_text):
        models.append(78)
    if re.search(r'配方', process_text):
        models.append(79)
    
    # 去重并保持顺序
    seen = set()
    unique_models = []
    for m in models:
        if m not in seen:
            seen.add(m)
            unique_models.append(m)
    
    return unique_models

def process_file(input_path, output_path):
    """处理整个文件"""
    result = {}
    
    with open(input_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            
            # 提取样本ID和推理过程
            match = re.match(r'\[(\d+)\]\s*(.*)', line)
            if match:
                sample_id = match.group(1)
                process = match.group(2)
                
                # 识别模型
                models = identify_models_in_process(process)
                result[sample_id] = models
                
                # 打印进度
                if line_num % 100 == 0:
                    print(f"已处理 {line_num} 行...")
    
    # 保存结果
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    return result

def print_statistics(result):
    """打印统计信息"""
    total_samples = len(result)
    total_models_used = sum(len(models) for models in result.values())
    avg_models = total_models_used / total_samples if total_samples > 0 else 0
    
    # 统计每个模型的使用次数
    model_counter = Counter()
    for models in result.values():
        for model_id in models:
            model_counter[model_id] += 1
    
    print(f"\n=== 处理完成 ===")
    print(f"总样本数: {total_samples}")
    print(f"总模型使用次数: {total_models_used}")
    print(f"平均每个样本使用模型数: {avg_models:.2f}")
    
    print(f"\n前10个最常用模型:")
    for model_id, count in model_counter.most_common(10):
        percentage = count / total_samples * 100
        print(f"  模型 {model_id}: 使用 {count} 次 ({percentage:.1f}%)")
    
    # 统计没有模型的样本
    no_models = [sid for sid, models in result.items() if len(models) == 0]
    if no_models:
        print(f"\n警告: {len(no_models)} 个样本未识别到任何模型")
        print(f"  样本ID: {no_models[:10]}..." if len(no_models) > 10 else f"  样本ID: {no_models}")

def main():
    input_file = 'data/data_process/train_process_part_3.txt'
    output_file = 'data/data_process/process_models_part_3.json'
    
    print(f"开始处理: {input_file}")
    result = process_file(input_file, output_file)
    print_statistics(result)
    print(f"\n结果已保存到: {output_file}")

if __name__ == '__main__':
    main()

