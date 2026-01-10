#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
详细分析推理过程并转换为精确的模型ID序列
"""

import re
import json

def detailed_model_identification(process_text):
    """
    详细识别推理过程中的所有模型
    采用多层次匹配策略
    """
    models = []
    
    # ============ 1. 曲线定义 (0-2) ============
    # 椭圆定义
    if re.search(r'椭圆.*定义', process_text) or \
       re.search(r'\|PF[_₁1]?\|.*\+.*\|PF[_₂2]?\|.*=.*2a', process_text) or \
       re.search(r'两焦点.*距离.*和.*2a', process_text):
        models.append(0)
    
    # 双曲线定义
    if re.search(r'双曲线.*定义', process_text) or \
       re.search(r'\|\|PF[_₁1]?\|.*-.*\|PF[_₂2]?\|\|.*=.*2a', process_text) or \
       re.search(r'\|PF[_₁1]?\|.*-.*\|PF[_₂2]?\|.*=.*2a', process_text):
        models.append(1)
    
    # 抛物线定义
    if re.search(r'抛物线.*定义', process_text) or \
       re.search(r'到焦点.*距离.*到.*准线.*距离', process_text) or \
       re.search(r'焦点.*距离.*准线.*距离', process_text) or \
       re.search(r'\|PF\|.*=.*d', process_text) or \
       re.search(r'\|P[A-Z]\|.*=.*\|PF\|', process_text):
        models.append(2)
    
    # ============ 2. 标准方程 (3-10) ============
    # 椭圆标准方程 - 焦点在x轴
    if re.search(r'\\frac\{x\^\{2\}\}\{[0-9a-z²]+\}.*\+.*\\frac\{y\^\{2\}\}\{[0-9a-z²]+\}.*=.*1', process_text):
        if '焦点在y轴' not in process_text and 'y^{2}}}{a' not in process_text:
            models.append(3)
        else:
            models.append(4)
    
    # 椭圆标准方程 - 焦点在y轴
    if re.search(r'\\frac\{y\^\{2\}\}\{[0-9a-z²]+\}.*\+.*\\frac\{x\^\{2\}\}\{[0-9a-z²]+\}.*=.*1', process_text) or \
       '焦点在y轴' in process_text:
        if 4 not in models:
            models.append(4)
    
    # 双曲线标准方程 - 焦点在x轴
    if re.search(r'\\frac\{x\^\{2\}\}\{[0-9a-z²]+\}.*-.*\\frac\{y\^\{2\}\}\{[0-9a-z²]+\}.*=.*1', process_text):
        models.append(5)
    
    # 双曲线标准方程 - 焦点在y轴
    if re.search(r'\\frac\{y\^\{2\}\}\{[0-9a-z²]+\}.*-.*\\frac\{x\^\{2\}\}\{[0-9a-z²]+\}.*=.*1', process_text):
        models.append(6)
    
    # 抛物线标准方程 - 需要更精确匹配
    # y² = ... x 形式（开口向左或向右）
    y_eq_match = re.search(r'y\^\{2\}.*=.*(-?[0-9]*[a-z]*x)(?![²\^{])', process_text)
    y2_eq_match = re.search(r'y2.*=.*(-?[0-9]*[a-z]*x)(?![²\^{])', process_text)
    
    if y_eq_match or y2_eq_match:
        # 检查是否有负号
        matched_part = y_eq_match.group(1) if y_eq_match else y2_eq_match.group(1)
        if matched_part.strip().startswith('-'):
            models.append(8)  # 开口向左
        else:
            models.append(7)  # 开口向右
    
    # x² = ... y 形式（开口向上或向下）
    x_eq_match = re.search(r'x\^\{2\}.*=.*(-?[0-9]*[a-z]*y)(?![²\^{])', process_text)
    x2_eq_match = re.search(r'x2.*=.*(-?[0-9]*[a-z]*y)(?![²\^{])', process_text)
    
    if x_eq_match or x2_eq_match:
        # 检查是否有负号
        matched_part = x_eq_match.group(1) if x_eq_match else x2_eq_match.group(1)
        if matched_part.strip().startswith('-'):
            models.append(10)  # 开口向下
        else:
            models.append(9)  # 开口向上
    
    # ============ 3. 参数关系与离心率 (11-15) ============
    # 椭圆参数关系
    if re.search(r'a\^\{2\}.*=.*b\^\{2\}.*\+.*c\^\{2\}', process_text) or \
       re.search(r'b\^\{2\}.*=.*a\^\{2\}.*-.*c\^\{2\}', process_text):
        if '双曲线' not in process_text[:process_text.find('a^{2}') if 'a^{2}' in process_text else 0]:
            models.append(11)
    
    # 双曲线参数关系
    if re.search(r'c\^\{2\}.*=.*a\^\{2\}.*\+.*b\^\{2\}', process_text) or \
       re.search(r'b\^\{2\}.*=.*c\^\{2\}.*-.*a\^\{2\}', process_text):
        models.append(12)
    
    # 离心率公式
    if '离心率' in process_text or re.search(r'e.*=.*\\frac\{c\}\{a\}', process_text):
        models.append(13)
    
    # 椭圆离心率范围
    if re.search(r'0.*<.*e.*<.*1|e.*<.*1.*椭圆', process_text):
        models.append(14)
    
    # 双曲线离心率范围
    if re.search(r'e.*>.*1', process_text) and '双曲线' in process_text:
        models.append(15)
    
    # ============ 4. 焦半径与通径 (16-20) ============
    # 椭圆焦半径
    if re.search(r'\|PF[_₁₂12]?\|.*=.*a.*±.*ex', process_text) or \
       ('椭圆' in process_text and '焦半径' in process_text):
        models.append(16)
    
    # 抛物线焦半径
    if re.search(r'x.*\+.*\\frac\{p\}\{2\}', process_text) or \
       ('抛物线' in process_text and '焦半径' in process_text):
        models.append(17)
    
    # 椭圆通径
    if re.search(r'\\frac\{2b\^\{2\}\}\{a\}', process_text):
        if '椭圆' in process_text or '通径' in process_text:
            models.append(18)
        if '双曲线' in process_text:
            models.append(19)
    
    # 抛物线通径
    if '通径' in process_text and '2p' in process_text and '抛物线' in process_text:
        models.append(20)
    
    # ============ 5. 渐近线相关 (21-24) ============
    # 渐近线
    if '渐近线' in process_text:
        models.append(21)
        # 焦点到渐近线距离
        if re.search(r'd.*=.*b|距离.*=.*b', process_text):
            models.append(22)
    
    # 共渐近线
    if '共渐近线' in process_text or '渐近线系' in process_text:
        models.append(23)
    
    # 等轴双曲线
    if '等轴双曲线' in process_text or \
       (re.search(r'a.*=.*b', process_text) and '双曲线' in process_text and re.search(r'e.*=.*\\sqrt\{2\}', process_text)):
        models.append(24)
    
    # ============ 6. 第二定义与准线 (25-29) ============
    # 椭圆第二定义
    if ('椭圆' in process_text and '第二定义' in process_text) or \
       ('椭圆' in process_text and re.search(r'\|PF\|/d.*=.*e', process_text)):
        models.append(25)
    
    # 双曲线第二定义
    if ('双曲线' in process_text and '第二定义' in process_text) or \
       ('双曲线' in process_text and re.search(r'\|PF\|/d.*=.*e', process_text)):
        models.append(26)
    
    # 椭圆准线
    if '椭圆' in process_text and re.search(r'x.*=.*\\frac\{a\^\{2\}\}\{c\}', process_text):
        models.append(27)
    
    # 双曲线准线
    if '双曲线' in process_text and '准线' in process_text:
        models.append(28)
    
    # 抛物线准线
    if '准线' in process_text and ('抛物线' in process_text or re.search(r'[xy].*=.*-\\frac\{p\}\{2\}', process_text)):
        models.append(29)
    
    # ============ 7. 焦点三角形 (30-32) ============
    # 椭圆焦点三角形面积
    if ('椭圆' in process_text or 'PF_{1}PF_{2}' in process_text) and \
       re.search(r'S.*=.*b\^\{2\}.*tan', process_text):
        models.append(30)
    
    # 双曲线焦点三角形面积
    if '双曲线' in process_text and re.search(r'S.*=.*b\^\{2\}.*cot', process_text):
        models.append(31)
    
    # 椭圆焦点三角形周长
    if '周长' in process_text and re.search(r'4a|2a.*\+.*2c', process_text):
        models.append(32)
    
    # ============ 8. 抛物线焦点弦 (33-36) ============
    # 焦点弦长
    if re.search(r'x[_₁12].*\+.*x[_₂2].*\+.*p(?![a-z²])', process_text) or \
       re.search(r'y[_₁1].*\+.*y[_₂2].*\+.*p(?![a-z²])', process_text):
        models.append(33)
    
    # 焦点弦端点横坐标乘积
    if re.search(r'x[_₁1].*x[_₂2].*=.*p\^\{2\}/4', process_text):
        models.append(34)
    
    # 焦点弦端点纵坐标乘积
    if re.search(r'y[_₁1].*y[_₂2].*=.*-p\^\{2\}', process_text):
        models.append(35)
    
    # 焦点弦公式（角度）
    if re.search(r'\|AB\|.*=.*\\frac\{2p\}\{.*sin\^\{2\}', process_text):
        models.append(36)
    
    # ============ 9. 参数方程与切线 (37-40) ============
    # 椭圆参数方程
    if re.search(r'x.*=.*a.*cos.*θ|参数方程', process_text):
        models.append(37)
    
    # 椭圆切线
    if '切线' in process_text and '椭圆' in process_text:
        models.append(38)
    
    # 抛物线切线
    if '切线' in process_text and '抛物线' in process_text:
        models.append(39)
    
    # 椭圆中点弦斜率关系
    if '椭圆' in process_text and '中点' in process_text and re.search(r'k.*k.*=.*-\\frac\{b\^\{2\}\}\{a\^\{2\}\}', process_text):
        models.append(40)
    
    # ============ 10. 韦达定理 (41-43) ============
    # 韦达定理
    if '韦达定理' in process_text or '根与系数' in process_text:
        models.append(41)
        models.append(42)
        models.append(43)
    else:
        # 两根之和
        if re.search(r'[xy][_₁1].*\+.*[xy][_₂2].*=', process_text):
            models.append(42)
        # 两根之积
        if re.search(r'[xy][_₁1].*[xy][_₂2].*=', process_text):
            models.append(43)
    
    # ============ 11. 点差法 (44-46) ============
    # 点差法
    if '点差法' in process_text or '两式相减' in process_text:
        models.append(44)
        if '椭圆' in process_text:
            models.append(45)
        elif '双曲线' in process_text:
            models.append(46)
    
    # ============ 12. 三角形定理 (47-49) ============
    # 余弦定理
    if '余弦定理' in process_text or re.search(r'c\^\{2\}.*=.*a\^\{2\}.*\+.*b\^\{2\}.*-.*2.*cos', process_text):
        models.append(47)
    
    # 正弦定理
    if '正弦定理' in process_text or re.search(r'\\frac\{[abc]\}\{sin', process_text):
        models.append(48)
    
    # 勾股定理
    if '勾股定理' in process_text or \
       (re.search(r'a\^\{2\}.*\+.*b\^\{2\}.*=.*c\^\{2\}', process_text) and '双曲线' not in process_text):
        models.append(49)
    
    # ============ 13. 弦长公式 (50-51) ============
    # 弦长公式
    if '弦长' in process_text:
        if re.search(r'\\sqrt.*\(1.*\+.*k\^\{2\}\)', process_text) or \
           re.search(r'\\sqrt\{1.*\+.*k\^\{2\}\}', process_text):
            models.append(51)
        else:
            models.append(50)
    
    # ============ 14. 距离与坐标 (52-55) ============
    # 点到直线距离
    if re.search(r'点到.*线.*距离|d.*=.*\\frac\{.*\}\{\\sqrt', process_text):
        models.append(52)
    
    # 两点距离
    if re.search(r'两点.*距离|\\sqrt.*\[?\(.*x[_₁12]?.*-.*x[_₂2]?.*\)\^\{2\}', process_text):
        models.append(53)
    
    # 中点坐标
    if '中点' in process_text:
        models.append(54)
    
    # 斜率公式
    if '斜率' in process_text or re.search(r'k.*=.*\\frac\{y[_₁12]?.*-.*y[_₂2]?\}', process_text):
        models.append(55)
    
    # ============ 15. 三角形面积 (56-58) ============
    # 三角形面积公式
    if re.search(r'S.*=.*\\frac\{1\}\{2\}', process_text) and '面积' in process_text:
        if 'sin' in process_text:
            models.append(57)
        elif re.search(r'x[_₁1]y[_₂2].*-.*x[_₂2]y[_₁1]', process_text):
            models.append(58)
        else:
            models.append(56)
    
    # ============ 16. 向量运算 (59-62) ============
    if '\\overrightarrow' in process_text or 'overrightarrow' in process_text:
        # 向量数量积（代数形式）
        if re.search(r'x[_₁1]x[_₂2].*\+.*y[_₁1]y[_₂2]', process_text):
            models.append(59)
        
        # 向量数量积（几何形式）
        if re.search(r'\|.*\|.*\|.*\|.*cos', process_text):
            models.append(60)
        
        # 垂直条件
        if re.search(r'\\cdot.*=.*0|\\bot', process_text) or '垂直' in process_text:
            models.append(61)
        
        # 共线条件
        if re.search(r'=.*\\lambda', process_text) or '共线' in process_text:
            models.append(62)
    
    # ============ 17. 不等式 (63-64) ============
    # 基本不等式
    if '基本不等式' in process_text or re.search(r'\\geqslant.*2\\sqrt|≥.*2\\sqrt', process_text):
        models.append(63)
    
    # 取等条件
    if '当且仅当' in process_text:
        models.append(64)
    
    # ============ 18. 判别式 (65-67) ============
    # 判别式
    if '判别式' in process_text or re.search(r'[AΔ].*=|\\triangle.*=', process_text):
        models.append(65)
        # 相切条件
        if re.search(r'[AΔ].*=.*0|\\triangle.*=.*0', process_text) and '相切' in process_text:
            models.append(66)
        # 相交条件
        elif re.search(r'[AΔ].*>.*0|\\triangle.*>.*0', process_text):
            models.append(67)
    
    # ============ 19. 中位线 (68-69) ============
    if '中位线' in process_text:
        if '三角形' in process_text:
            models.append(68)
        elif '梯形' in process_text:
            models.append(69)
    
    # ============ 20. 内切圆和等积法 (70-71) ============
    if '内切圆' in process_text:
        models.append(70)
    
    if '等积' in process_text:
        models.append(71)
    
    # ============ 21. 直线方程 (72-74) ============
    # 点斜式
    if '点斜式' in process_text or re.search(r'y.*-.*y[_₀0].*=.*k.*\(x.*-.*x[_₀0]\)', process_text):
        models.append(72)
    
    # 两点式
    if '两点式' in process_text:
        models.append(73)
    
    # 截距式
    if '截距式' in process_text or re.search(r'\\frac\{x\}\{[^}]+\}.*\+.*\\frac\{y\}\{[^}]+\}.*=.*1', process_text):
        models.append(74)
    
    # ============ 22. 圆相关 (75-76) ============
    # 圆的标准方程
    if re.search(r'\(x.*-.*[0-9a-z]+\)\^\{2\}.*\+.*\(y.*-.*[0-9a-z]+\)\^\{2\}.*=', process_text) or \
       re.search(r'圆.*标准方程|圆心|半径', process_text):
        models.append(75)
    
    # 圆的切线条件
    if '圆' in process_text and '相切' in process_text and re.search(r'd.*=.*r', process_text):
        models.append(76)
    
    # ============ 23. 高级技巧 (77-79) ============
    # 齐次化
    if '齐次化' in process_text or re.search(r'同除以.*a\^\{2\}|两边.*除以.*a\^\{2\}', process_text):
        models.append(77)
    
    # 设x=my+n
    if re.search(r'x.*=.*[mt]y.*\+|设.*x.*=', process_text):
        models.append(78)
    
    # 配方法
    if '配方' in process_text or ('最值' in process_text and '二次' in process_text):
        models.append(79)
    
    # 去重并保持顺序
    unique_models = []
    seen = set()
    for m in models:
        if m not in seen:
            seen.add(m)
            unique_models.append(m)
    
    return unique_models

def main():
    input_file = 'data/data_process/train_process_part_1.txt'
    output_file = 'data/data_process/process_models_part_1.json'
    
    result = {}
    
    print(f"开始详细分析: {input_file}")
    
    with open(input_file, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            
            # 提取样本ID和推理过程
            match = re.match(r'\[(\d+)\]\s*(.*)', line)
            if match:
                sample_id = match.group(1)
                process = match.group(2)
                
                # 详细识别模型
                models = detailed_model_identification(process)
                result[sample_id] = models
                
                # 打印进度
                if line_num % 50 == 0:
                    print(f"  已处理 {line_num}/{536} 个样本...")
    
    # 添加元数据
    output_data = {
        "_meta": {
            "total_samples": len(result),
            "model_library": "conic_model_ids.json",
            "version": "v1.0",
            "description": "Part 1推理过程的模型序列映射（详细分析版本）"
        }
    }
    output_data.update(result)
    
    # 保存结果
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    # 统计信息
    total_models = sum(len(models) for models in result.values())
    avg_models = total_models / len(result) if result else 0
    no_models = sum(1 for models in result.values() if len(models) == 0)
    
    print(f"\n=== 分析完成 ===")
    print(f"总样本数: {len(result)}")
    print(f"总模型使用次数: {total_models}")
    print(f"平均每个样本使用模型数: {avg_models:.2f}")
    print(f"未识别到模型的样本数: {no_models}")
    print(f"\n结果已保存到: {output_file}")
    
    # 统计最常用的模型
    from collections import Counter
    model_counter = Counter()
    for models in result.values():
        for model_id in models:
            model_counter[model_id] += 1
    
    print(f"\n前15个最常用模型:")
    for model_id, count in model_counter.most_common(15):
        percentage = count / len(result) * 100
        print(f"  模型 {model_id}: {count} 次 ({percentage:.1f}%)")

if __name__ == '__main__':
    main()

