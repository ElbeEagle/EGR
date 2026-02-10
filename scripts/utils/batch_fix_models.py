"""
批量修复所有模型文件的apply方法

修复内容:
1. -> None 改为 -> bool
2. 包裹try-except
3. 添加 return True / return False
"""

import os
import re
import sys


def fix_model_file(filepath):
    """修复单个模型文件"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # 跳过已经修复的文件（已有 -> bool）
    if '-> bool:' in content and 'return True' in content and 'return False' in content:
        return False, "已修复"
    
    # 修复 -> None: 为 -> bool:
    content = content.replace(
        'def apply(self, state) -> None:',
        'def apply(self, state) -> bool:'
    )
    
    # 找到apply方法的范围
    lines = content.split('\n')
    new_lines = []
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # 检测apply方法开始
        if 'def apply(self, state)' in line:
            new_lines.append(line)
            i += 1
            
            # 收集docstring
            in_docstring = False
            docstring_done = False
            while i < len(lines) and not docstring_done:
                dline = lines[i]
                new_lines.append(dline)
                stripped = dline.strip()
                
                if '"""' in stripped or "'''" in stripped:
                    if not in_docstring:
                        in_docstring = True
                        # 检查是否是单行docstring
                        quote = '"""' if '"""' in stripped else "'''"
                        if stripped.count(quote) >= 2:
                            docstring_done = True
                    else:
                        docstring_done = True
                elif not in_docstring and stripped and not stripped.startswith('#'):
                    # 没有docstring，回退
                    new_lines.pop()
                    break
                
                i += 1
            
            # 现在收集方法体
            body_lines = []
            method_indent = len(line) - len(line.lstrip())  # def的缩进
            body_indent = method_indent + 4  # 方法体缩进
            
            # 检查是否已经有try:
            has_try = False
            while i < len(lines):
                bline = lines[i]
                
                # 检测方法结束：遇到同级或更外层的def/class
                if bline.strip():
                    current_indent = len(bline) - len(bline.lstrip())
                    if current_indent <= method_indent and bline.strip().startswith(('def ', 'class ')):
                        break
                
                if bline.strip() == 'try:':
                    has_try = True
                
                body_lines.append(bline)
                i += 1
            
            if has_try and 'return True' in '\n'.join(body_lines) and 'return False' in '\n'.join(body_lines):
                # 已经有完整的try-except-return结构
                new_lines.extend(body_lines)
            else:
                # 需要修复
                # 检查是否有return True
                has_return_true = any('return True' in bl for bl in body_lines)
                has_return_false = any('return False' in bl for bl in body_lines)
                
                if not has_try:
                    # 包裹try-except
                    indent = ' ' * body_indent
                    new_lines.append(f'{indent}try:')
                    
                    for bl in body_lines:
                        if bl.strip():
                            new_lines.append(' ' * 4 + bl)
                        else:
                            new_lines.append(bl)
                    
                    if not has_return_true:
                        new_lines.append(f'{indent}    return True')
                    new_lines.append(f'{indent}except Exception:')
                    new_lines.append(f'{indent}    return False')
                else:
                    # 已有try但缺少return
                    for bl in body_lines:
                        new_lines.append(bl)
                    if not has_return_true:
                        new_lines.append(f'{" " * body_indent}    return True')
                    if not has_return_false:
                        new_lines.append(f'{" " * body_indent}except Exception:')
                        new_lines.append(f'{" " * body_indent}    return False')
            
            continue
        
        new_lines.append(line)
        i += 1
    
    content = '\n'.join(new_lines)
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True, "已修复"
    
    return False, "无需修改"


def main():
    models_dir = os.path.join(os.path.dirname(__file__), '../../src/theorems/models')
    models_dir = os.path.abspath(models_dir)
    
    if not os.path.exists(models_dir):
        print(f"目录不存在: {models_dir}")
        sys.exit(1)
    
    files = sorted([
        os.path.join(models_dir, f)
        for f in os.listdir(models_dir)
        if f.startswith('model_') and f.endswith('.py')
    ])
    
    print(f"找到 {len(files)} 个模型文件")
    print("=" * 60)
    
    fixed = 0
    skipped = 0
    errors = 0
    
    for filepath in files:
        fname = os.path.basename(filepath)
        try:
            modified, msg = fix_model_file(filepath)
            if modified:
                fixed += 1
                print(f"  ✓ {fname}: {msg}")
            else:
                skipped += 1
                # print(f"  - {fname}: {msg}")
        except Exception as e:
            errors += 1
            print(f"  ✗ {fname}: 错误 - {e}")
    
    print("=" * 60)
    print(f"完成: 修复={fixed}, 跳过={skipped}, 错误={errors}")


if __name__ == '__main__':
    main()
