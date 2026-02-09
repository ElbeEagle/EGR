"""
训练数据生成器

功能：
1. 从数据集构建完整的状态序列（包含transitions和状态向量）
2. 提取成功的状态转换作为训练样本
3. 保存为Module 3可直接使用的训练数据格式

【关键修复 2026-01-20】因果倒置问题：
- 错误做法：(state_after_applying_model, model_just_applied) ❌
- 正确做法：(state_before_applying_model, model_to_apply) ✅

训练样本格式：
- state_vector: 应用模型前的状态（28维向量）
- model_id: 即将应用的模型ID（0-79）
即：用当前状态预测下一步应该选择哪个模型

输入: data/train_with_models_1_100.json
输出: data/train_state_model.json
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.state.state_sequence_builder import StateSequenceBuilder
from src.state.state_constructor import StateConstructor
from src.theorems.theorem_library import TheoremLibrary


class TrainingDataGenerator:
    """
    训练数据生成器
    """
    
    def __init__(self):
        """初始化"""
        self.theorem_library = TheoremLibrary()
        self.state_constructor = StateConstructor(theorem_library=self.theorem_library)
        self.sequence_builder = StateSequenceBuilder(
            self.theorem_library,
            self.state_constructor
        )
    
    def load_samples(self, data_path: str) -> List[Dict]:
        """
        加载数据集
        
        Args:
            data_path: 数据文件路径
        
        Returns:
            样本列表（只包含有模型序列的样本）
        """
        with open(data_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        samples = []
        for item in data:
            if 'models' in item and item['models']:
                samples.append(item)
        
        return samples
    
    def generate_training_data(self, samples: List[Dict]) -> Dict[str, Any]:
        """
        生成训练数据
        
        Args:
            samples: 样本列表
        
        Returns:
            训练数据字典
        """
        print(f"{'='*80}")
        print(f"  训练数据生成器")
        print(f"{'='*80}\n")
        
        print(f"数据集样本数: {len(samples)}")
        print(f"已实现模型数: {len([m for m in range(80) if self.theorem_library.get_model(m)])}/80\n")
        
        training_data = {
            'total_samples': 0,
            'total_transitions': 0,
            'sample_results': []
        }
        
        # 统计信息
        total_success_transitions = 0
        total_samples_with_data = 0
        model_usage_count = {}
        
        # 逐个处理样本
        for i, sample in enumerate(samples):
            print(f"处理样本 {i+1}/{len(samples)}...", end='\r')
            
            # 构建状态序列
            transitions = self.sequence_builder.build_sequence(
                fact_expressions=sample['fact_expressions'],
                query_expressions=sample['query_expressions'],
                model_ids=sample['models']
            )
            
            # 【关键修复】提取训练样本：(state_before_applying_model, model_to_apply)
            # 修复因果倒置问题：必须用"应用前状态"预测"要应用的模型"
            sample_data = {
                'sample_id': i,
                'problem': sample.get('problem', ''),
                'transitions': []
            }
            
            # 构建step到transition的映射
            step_to_trans = {trans.step: trans for trans in transitions}
            
            # 遍历所有转换，提取训练样本
            for trans in transitions:
                # 只处理成功的转换，且必须有model_id（step>0）
                if trans.status != 'success' or trans.step == 0:
                    continue
                
                # 获取"应用模型前的状态" = 上一步的状态
                prev_step = trans.step - 1
                if prev_step not in step_to_trans:
                    continue  # 如果上一步不存在，跳过
                
                state_before = step_to_trans[prev_step].abstract_state
                
                # 提取状态向量（应用前的状态）
                state_vector = state_before.to_vector()
                
                # 训练样本：(state_before, model_to_apply)
                transition_data = {
                    'step': trans.step,
                    'model_id': trans.model_id,
                    'model_name': trans.model_name,
                    'status': trans.status,
                    # 注意：这是应用模型前的状态（用于训练）
                    'state_before': {
                        'curve_type': state_before.curve_type.value,
                        'query_type': state_before.query_type.value,
                        'param_count': len(state_before.has_parameters),
                        'completeness_score': round(state_before.completeness_score, 3),
                        'has_focus_info': state_before.has_focus_info,
                        'has_asymptote_info': state_before.has_asymptote_info,
                        'has_directrix_info': state_before.has_directrix_info,
                        'has_vertex_info': state_before.has_vertex_info,
                        'reasoning_depth': state_before.reasoning_depth
                    },
                    'state_vector': [round(x, 4) for x in state_vector]
                }
                
                sample_data['transitions'].append(transition_data)
                total_success_transitions += 1
                
                # 统计模型使用次数
                model_usage_count[trans.model_id] = model_usage_count.get(trans.model_id, 0) + 1
            
            # 只保存有成功转换的样本
            if sample_data['transitions']:
                training_data['sample_results'].append(sample_data)
                total_samples_with_data += 1
        
        print(f"\n")
        
        # 更新统计信息
        training_data['total_samples'] = total_samples_with_data
        training_data['total_transitions'] = total_success_transitions
        
        # 添加模型使用统计
        training_data['model_usage_statistics'] = {
            'total_models_used': len(model_usage_count),
            'model_counts': dict(sorted(model_usage_count.items(), key=lambda x: x[1], reverse=True))
        }
        
        return training_data, model_usage_count
    
    def save_training_data(self, training_data: Dict[str, Any], output_path: str):
        """
        保存训练数据
        
        Args:
            training_data: 训练数据字典
            output_path: 输出文件路径
        """
        # 确保输出目录存在
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(training_data, f, indent=2, ensure_ascii=False)
        
        print(f"✓ 训练数据已保存到: {output_path}")
    
    def print_statistics(self, training_data: Dict[str, Any], model_usage_count: Dict[int, int]):
        """
        打印统计信息
        
        Args:
            training_data: 训练数据字典
            model_usage_count: 模型使用次数统计
        """
        print(f"\n{'='*80}")
        print(f"  统计结果")
        print(f"{'='*80}\n")
        
        print(f"总样本数: {training_data['total_samples']}")
        print(f"总训练样本数: {training_data['total_transitions']}")
        print(f"平均每样本: {training_data['total_transitions'] / training_data['total_samples']:.2f} 个转换\n")
        
        print(f"使用的模型数: {len(model_usage_count)}/80\n")
        
        print("Top 10 高频模型:")
        print(f"{'模型ID':<10} {'使用次数':<10} {'占比':<10}")
        print("-" * 30)
        
        sorted_models = sorted(model_usage_count.items(), key=lambda x: x[1], reverse=True)[:10]
        for model_id, count in sorted_models:
            model = self.theorem_library.get_model(model_id)
            model_name = model.name if model else f"Model_{model_id}"
            percentage = count / training_data['total_transitions'] * 100
            print(f"{model_id:<10} {count:<10} {percentage:.1f}%")
            print(f"  └─ {model_name}")
        
        print(f"\n{'='*80}\n")
    
    def validate_data(self, training_data: Dict[str, Any]) -> bool:
        """
        验证生成的数据
        
        Args:
            training_data: 训练数据字典
        
        Returns:
            是否通过验证
        """
        print("验证数据质量...\n")
        
        checks = []
        
        # 检查1: 是否有训练样本
        has_samples = training_data['total_transitions'] > 0
        checks.append(('有训练样本', has_samples))
        
        # 检查2: 状态向量维度一致性
        state_vector_dims = []
        for sample in training_data['sample_results']:
            for trans in sample['transitions']:
                state_vector_dims.append(len(trans['state_vector']))
        
        dim_consistent = len(set(state_vector_dims)) == 1 and state_vector_dims[0] == 28
        checks.append(('状态向量维度=28且一致', dim_consistent))
        
        # 检查3: 所有model_id都有效
        all_model_ids = []
        for sample in training_data['sample_results']:
            for trans in sample['transitions']:
                all_model_ids.append(trans['model_id'])
        
        valid_model_ids = all(0 <= mid < 80 for mid in all_model_ids)
        checks.append(('模型ID范围有效(0-79)', valid_model_ids))
        
        # 检查4: 完整度在[0,1]范围内
        all_completeness = []
        for sample in training_data['sample_results']:
            for trans in sample['transitions']:
                all_completeness.append(trans['state_before']['completeness_score'])
        
        valid_completeness = all(0 <= c <= 1 for c in all_completeness)
        checks.append(('完整度范围有效[0,1]', valid_completeness))
        
        # 打印验证结果
        all_passed = True
        for check_name, passed in checks:
            status = '✓' if passed else '✗'
            print(f"{status} {check_name}")
            if not passed:
                all_passed = False
        
        print()
        return all_passed


def main():
    """主函数"""
    # 初始化生成器
    generator = TrainingDataGenerator()
    
    # 路径配置
    input_path = project_root / 'data' / 'train_with_models_1_100.json'
    output_path = project_root / 'data' / 'train_state_model.json'
    
    print(f"输入文件: {input_path}")
    print(f"输出文件: {output_path}\n")
    
    # 加载数据
    samples = generator.load_samples(str(input_path))
    print(f"✓ 加载了 {len(samples)} 个有效样本\n")
    
    # 生成训练数据
    training_data, model_usage_count = generator.generate_training_data(samples)
    
    # 打印统计信息
    generator.print_statistics(training_data, model_usage_count)
    
    # 验证数据
    if not generator.validate_data(training_data):
        print("⚠️  数据验证失败！")
        return
    
    # 保存数据
    generator.save_training_data(training_data, str(output_path))
    
    print("✅ 训练数据生成完成！")
    print(f"\n下一步: 使用此数据训练Module 3的模型选择网络")


if __name__ == '__main__':
    main()
