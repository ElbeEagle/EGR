"""
安全地修复所有模型文件的apply方法返回值

策略:
1. 替换 `-> None:` 为 `-> bool:`
2. 在 apply 方法的 docstring 后插入 try:
3. 将方法体增加4格缩进
4. 在 state.applied_models.append() 后添加 return True
5. 在末尾添加 except Exception: return False
"""

import os
import re
import sys


def fix_file(filepath):
    """修复单个文件"""
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    original_text = ''.join(lines)
    
    # 检查是否已修复（apply方法已经是 -> bool）
    if 'def apply(self, state) -> bool:' in original_text:
        return False, "already fixed"
    
    # 检查是否有 apply 方法
    if 'def apply(self, state)' not in original_text:
        return False, "no apply method"
    
    new_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # 检测 apply 方法
        if 'def apply(self, state)' in line:
            # 获取方法缩进
            method_indent = len(line) - len(line.lstrip())
            body_indent = method_indent + 4
            
            # 修改返回类型
            line = line.replace('-> None:', '-> bool:')
            new_lines.append(line)
            i += 1
            
            # 收集docstring
            docstring_lines = []
            in_docstring = False
            found_docstring = False
            
            while i < len(lines):
                dline = lines[i]
                stripped = dline.strip()
                
                if not found_docstring and not stripped:
                    # 空行在docstring之前
                    docstring_lines.append(dline)
                    i += 1
                    continue
                
                if '"""' in stripped or "'''" in stripped:
                    found_docstring = True
                    if not in_docstring:
                        in_docstring = True
                        docstring_lines.append(dline)
                        # 单行docstring
                        quote = '"""' if '"""' in stripped else "'''"
                        if stripped.count(quote) >= 2:
                            i += 1
                            break
                        i += 1
                        continue
                    else:
                        # docstring结束
                        docstring_lines.append(dline)
                        i += 1
                        break
                elif in_docstring:
                    docstring_lines.append(dline)
                    i += 1
                    continue
                else:
                    # 没有docstring
                    break
            
            # 输出docstring
            new_lines.extend(docstring_lines)
            
            # 插入try:
            new_lines.append(' ' * body_indent + 'try:\n')
            
            # 收集方法体并增加缩进
            body_lines = []
            while i < len(lines):
                bline = lines[i]
                stripped = bline.strip()
                
                # 检测方法结束
                if stripped and not stripped.startswith('#'):
                    current_indent = len(bline) - len(bline.lstrip())
                    if current_indent <= method_indent and (stripped.startswith('def ') or stripped.startswith('class ')):
                        break
                
                body_lines.append(bline)
                i += 1
            
            # 输出缩进后的方法体
            for bl in body_lines:
                if bl.strip():
                    # 非空行增加4格缩进
                    new_lines.append(' ' * 4 + bl)
                else:
                    new_lines.append(bl)
            
            # 找到最后一个 applied_models.append 行，在后面添加 return True
            # 先回溯看看最后面是否已经有空行
            # 添加 return True
            new_lines.append(' ' * (body_indent + 4) + 'return True\n')
            new_lines.append('\n')
            # 添加 except
            new_lines.append(' ' * body_indent + 'except Exception:\n')
            new_lines.append(' ' * (body_indent + 4) + 'return False\n')
            
            continue
        
        new_lines.append(line)
        i += 1
    
    new_text = ''.join(new_lines)
    
    if new_text != original_text:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_text)
        return True, "fixed"
    
    return False, "no change needed"


def verify_syntax(filepath):
    """验证文件语法"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            code = f.read()
        compile(code, filepath, 'exec')
        return True, "OK"
    except SyntaxError as e:
        return False, f"SyntaxError at line {e.lineno}: {e.msg}"


def main():
    models_dir = os.path.join(os.path.dirname(__file__), '../../src/theorems/models')
    models_dir = os.path.abspath(models_dir)
    
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
            modified, msg = fix_file(filepath)
            if modified:
                # 验证语法
                ok, err = verify_syntax(filepath)
                if ok:
                    fixed += 1
                    print(f"  ✓ {fname}: 已修复")
                else:
                    errors += 1
                    print(f"  ✗ {fname}: 语法错误 - {err}")
            else:
                skipped += 1
        except Exception as e:
            errors += 1
            print(f"  ✗ {fname}: 异常 - {e}")
    
    print("=" * 60)
    print(f"结果: 修复={fixed}, 跳过={skipped}, 错误={errors}")
    
    # 最终语法检查
    print("\n语法验证:")
    syntax_errors = 0
    for filepath in files:
        fname = os.path.basename(filepath)
        ok, err = verify_syntax(filepath)
        if not ok:
            syntax_errors += 1
            print(f"  ✗ {fname}: {err}")
    
    if syntax_errors == 0:
        print("  ✓ 所有文件语法正确！")
    else:
        print(f"  共 {syntax_errors} 个文件有语法错误")


if __name__ == '__main__':
    main()
