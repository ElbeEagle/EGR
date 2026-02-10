"""
批量修复模型apply方法的返回值

将所有模型的apply方法从返回None改为返回bool
"""

import os
import re
import glob


def fix_model_file(filepath):
    """修复单个模型文件"""
    print(f"处理: {filepath}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    modified = False
    
    # 修复1: 将 def apply(self, state) -> None: 改为 -> bool:
    if '-> None:' in content and 'def apply' in content:
        content = re.sub(
            r'(def apply\([^)]+\))\s*->\s*None:',
            r'\1 -> bool:',
            content
        )
        modified = True
        print("  ✓ 修改返回类型: None -> bool")
    
    # 修复2: 在方法末尾添加 return True（如果没有return语句）
    # 查找apply方法的结束位置
    if 'def apply' in content:
        # 分析apply方法
        lines = content.split('\n')
        in_apply = False
        apply_indent = 0
        last_statement_line = -1
        
        for i, line in enumerate(lines):
            # 检测apply方法开始
            if 'def apply' in line:
                in_apply = True
                apply_indent = len(line) - len(line.lstrip())
                continue
            
            if in_apply:
                # 检测方法结束（遇到同级或更外层的定义）
                if line.strip() and not line.strip().startswith('#'):
                    current_indent = len(line) - len(line.lstrip())
                    if current_indent <= apply_indent and line.strip():
                        # 方法结束，检查是否需要添加return True
                        if last_statement_line > 0:
                            last_line = lines[last_statement_line].strip()
                            if not last_line.startswith('return'):
                                # 需要添加return True
                                # 在last_statement_line后插入
                                indent_str = ' ' * (apply_indent + 4)
                                lines.insert(last_statement_line + 1, f'{indent_str}return True')
                                modified = True
                                print("  ✓ 添加 return True")
                        break
                    
                    # 记录最后一个实际语句行（非空、非注释）
                    if line.strip() and not line.strip().startswith('#'):
                        last_statement_line = i
        
        if modified:
            content = '\n'.join(lines)
    
    # 修复3: 包裹整个apply方法体到try-except（如果还没有）
    if 'def apply' in content and 'try:' not in content[content.find('def apply'):content.find('def apply')+500]:
        # 需要添加try-except
        lines = content.split('\n')
        new_lines = []
        in_apply = False
        apply_indent = 0
        first_body_line = -1
        
        for i, line in enumerate(lines):
            if 'def apply' in line:
                in_apply = True
                apply_indent = len(line) - len(line.lstrip())
                new_lines.append(line)
                # 添加docstring后，插入try:
                continue
            
            if in_apply and first_body_line == -1:
                # 跳过docstring
                if '"""' in line or "'''" in line:
                    new_lines.append(line)
                    if line.count('"""') == 2 or line.count("'''") == 2:
                        # 单行docstring
                        first_body_line = i + 1
                    continue
                elif len(new_lines) > 0 and ('"""' in new_lines[-1] or "'''" in new_lines[-1]):
                    new_lines.append(line)
                    if '"""' in line or "'''" in line:
                        first_body_line = i + 1
                    continue
                else:
                    # 第一个实际代码行
                    first_body_line = i
                    indent_str = ' ' * (apply_indent + 4)
                    new_lines.append(f'{indent_str}try:')
                    new_lines.append(' ' * 4 + line)  # 增加缩进
                    continue
            
            if in_apply and i > first_body_line:
                current_indent = len(line) - len(line.lstrip())
                if current_indent <= apply_indent and line.strip():
                    # 方法结束，添加except
                    indent_str = ' ' * (apply_indent + 4)
                    new_lines.append(f'{indent_str}except Exception:')
                    new_lines.append(f'{indent_str}    return False')
                    new_lines.append(line)
                    in_apply = False
                    continue
                else:
                    # 增加缩进
                    if line.strip():
                        new_lines.append(' ' * 4 + line)
                    else:
                        new_lines.append(line)
                    continue
            
            new_lines.append(line)
        
        content = '\n'.join(new_lines)
        # modified = True  # 这个改动太复杂，暂时不自动应用
    
    # 保存文件
    if modified and content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✓ 文件已更新")
        return True
    else:
        print(f"  - 无需修改")
        return False


def main():
    """批量处理所有模型文件"""
    models_dir = 'src/theorems/models'
    
    if not os.path.exists(models_dir):
        print(f"错误：目录不存在: {models_dir}")
        return
    
    # 查找所有模型文件
    pattern = os.path.join(models_dir, 'model_*.py')
    files = glob.glob(pattern)
    
    print(f"找到 {len(files)} 个模型文件")
    print("=" * 60)
    
    modified_count = 0
    for filepath in sorted(files):
        if fix_model_file(filepath):
            modified_count += 1
        print()
    
    print("=" * 60)
    print(f"完成！共修改 {modified_count}/{len(files)} 个文件")


if __name__ == '__main__':
    main()
