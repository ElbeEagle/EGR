"""
Stage 2.3 集成测试

测试目标：
1. 验证100个样本的状态序列能否正确构建
2. 统计成功率、失败模式
3. 验证completeness单调性
4. 为Module 3准备训练数据
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.state.state_sequence_builder import StateSequenceBuilder
from src.state.state_constructor import StateConstructor
from src.theorems.theorem_library import TheoremLibrary


class IntegrationTester:
    """
    集成测试器
    """
    
    def __init__(self):
        """初始化"""
        self.theorem_library = TheoremLibrary()
        self.state_constructor = StateConstructor()
        self.sequence_builder = StateSequenceBuilder(
            self.theorem_library,
            self.state_constructor
        )
    
    def load_samples(self, data_path: str, limit: int = None) -> List[Dict]:
        """
        加载测试样本
        
        Args:
            data_path: 数据文件路径
            limit: 限制样本数量（None表示全部）
        
        Returns:
            样本列表
        """
        with open(data_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        samples = []
        for item in data:
            if 'models' not in item or not item['models']:
                continue
            samples.append(item)
            
            if limit and len(samples) >= limit:
                break
        
        return samples
    
    def test_sample(self, sample: Dict, sample_id: int) -> Dict[str, Any]:
        """
        测试单个样本
        
        Args:
            sample: 样本数据
            sample_id: 样本ID
        
        Returns:
            测试结果字典
        """
        # 构建状态序列
        transitions = self.sequence_builder.build_sequence(
            fact_expressions=sample['fact_expressions'],
            query_expressions=sample['query_expressions'],
            model_ids=sample['models']
        )
        
        # 分析序列
        analysis = self.sequence_builder.analyze_sequence(transitions)
        
        # 分类样本状态
        if analysis['success_rate'] == 1.0:
            sample_status = 'fully_success'
        elif analysis['success_rate'] > 0.0:
            sample_status = 'partial_success'
        else:
            sample_status = 'failed'
        
        return {
            'sample_id': sample_id,
            'status': sample_status,
            'transitions': transitions,
            'analysis': analysis,
            'model_sequence': sample['models']
        }
    
    def test_all_samples(self, samples: List[Dict]) -> Dict[str, Any]:
        """
        测试所有样本
        
        Args:
            samples: 样本列表
        
        Returns:
            总体测试结果
        """
        print(f"{'='*80}")
        print(f"  Stage 2.3 集成测试")
        print(f"{'='*80}\n")
        
        print(f"测试样本数: {len(samples)}")
        print(f"已实现模型: {len([m for m in range(80) if self.theorem_library.get_model(m)])}/80\n")
        
        results = []
        
        # 统计信息
        fully_success = 0
        partial_success = 0
        failed = 0
        
        total_steps = 0
        total_success_steps = 0
        total_skipped_steps = 0
        total_failed_steps = 0
        
        monotonic_count = 0
        
        completeness_gains = []
        param_gains = []
        
        # 逐个测试
        for i, sample in enumerate(samples):
            print(f"测试样本 {i+1}/{len(samples)}...", end='\r')
            
            result = self.test_sample(sample, i)
            results.append(result)
            
            # 统计
            if result['status'] == 'fully_success':
                fully_success += 1
            elif result['status'] == 'partial_success':
                partial_success += 1
            else:
                failed += 1
            
            analysis = result['analysis']
            total_steps += analysis['total_steps']
            total_success_steps += analysis['success_steps']
            total_skipped_steps += analysis['skipped_steps']
            total_failed_steps += analysis['failed_steps']
            
            if analysis['completeness_monotonic']:
                monotonic_count += 1
            
            completeness_gains.append(analysis['completeness_gain'])
            param_gains.append(analysis['param_gain'])
        
        print(f"\n")
        
        # 汇总结果
        summary = {
            'total_samples': len(samples),
            'sample_classification': {
                'fully_success': fully_success,
                'partial_success': partial_success,
                'failed': failed,
                'fully_success_rate': fully_success / len(samples) * 100,
                'partial_success_rate': partial_success / len(samples) * 100,
                'failed_rate': failed / len(samples) * 100
            },
            'step_statistics': {
                'total_steps': total_steps,
                'success_steps': total_success_steps,
                'skipped_steps': total_skipped_steps,
                'failed_steps': total_failed_steps,
                'success_rate': total_success_steps / total_steps * 100 if total_steps > 0 else 0,
                'skipped_rate': total_skipped_steps / total_steps * 100 if total_steps > 0 else 0,
                'failed_rate': total_failed_steps / total_steps * 100 if total_steps > 0 else 0
            },
            'quality_metrics': {
                'completeness_monotonic_rate': monotonic_count / len(samples) * 100,
                'avg_completeness_gain': sum(completeness_gains) / len(completeness_gains) if completeness_gains else 0,
                'avg_param_gain': sum(param_gains) / len(param_gains) if param_gains else 0
            },
            'results': results
        }
        
        return summary
    
    def print_summary(self, summary: Dict[str, Any]):
        """
        打印测试总结
        
        Args:
            summary: 测试结果总结
        """
        print(f"{'='*80}")
        print(f"  测试结果总结")
        print(f"{'='*80}\n")
        
        # 样本分类
        sample_class = summary['sample_classification']
        print(f"样本分类:")
        print(f"  - 完全成功: {sample_class['fully_success']} ({sample_class['fully_success_rate']:.1f}%)")
        print(f"  - 部分成功: {sample_class['partial_success']} ({sample_class['partial_success_rate']:.1f}%)")
        print(f"  - 完全失败: {sample_class['failed']} ({sample_class['failed_rate']:.1f}%)")
        print()
        
        # 步骤统计
        step_stats = summary['step_statistics']
        print(f"步骤统计:")
        print(f"  - 总步骤数: {step_stats['total_steps']}")
        print(f"  - 成功: {step_stats['success_steps']} ({step_stats['success_rate']:.1f}%)")
        print(f"  - 跳过: {step_stats['skipped_steps']} ({step_stats['skipped_rate']:.1f}%)")
        print(f"  - 失败: {step_stats['failed_steps']} ({step_stats['failed_rate']:.1f}%)")
        print()
        
        # 质量指标
        quality = summary['quality_metrics']
        print(f"质量指标:")
        print(f"  - Completeness单调性: {quality['completeness_monotonic_rate']:.1f}%")
        print(f"  - 平均Completeness增长: {quality['avg_completeness_gain']:.3f}")
        print(f"  - 平均参数增长: {quality['avg_param_gain']:.1f}")
        print()
        
        print(f"{'='*80}\n")
    
    def analyze_unimplemented_models(self, summary: Dict[str, Any]):
        """
        分析未实现模型的影响
        
        Args:
            summary: 测试结果总结
        """
        # 统计未实现模型
        unimplemented_models = {}
        affected_samples = set()
        
        for result in summary['results']:
            for transition in result['transitions']:
                if transition.status == 'skipped':
                    model_id = transition.model_id
                    if model_id not in unimplemented_models:
                        unimplemented_models[model_id] = 0
                    unimplemented_models[model_id] += 1
                    affected_samples.add(result['sample_id'])
        
        if unimplemented_models:
            print(f"{'='*80}")
            print(f"  未实现模型影响分析")
            print(f"{'='*80}\n")
            
            print(f"未实现模型数量: {len(unimplemented_models)}")
            print(f"受影响样本数: {len(affected_samples)}\n")
            
            print("未实现模型调用频率 Top 10:")
            sorted_models = sorted(unimplemented_models.items(), key=lambda x: x[1], reverse=True)
            for model_id, count in sorted_models[:10]:
                print(f"  Model {model_id}: {count}次")
            
            print(f"\n{'='*80}\n")
    
    def save_results(self, summary: Dict[str, Any], output_path: str):
        """
        保存测试结果（不包含完整transitions以节省空间）
        
        Args:
            summary: 测试结果总结
            output_path: 输出文件路径
        """
        # 简化版结果（去掉详细的transitions）
        simplified_summary = {
            'total_samples': summary['total_samples'],
            'sample_classification': summary['sample_classification'],
            'step_statistics': summary['step_statistics'],
            'quality_metrics': summary['quality_metrics'],
            'sample_results': [
                {
                    'sample_id': r['sample_id'],
                    'status': r['status'],
                    'model_sequence': r['model_sequence'],
                    'analysis': r['analysis']
                }
                for r in summary['results']
            ]
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(simplified_summary, f, indent=2, ensure_ascii=False)
        
        print(f"结果已保存到: {output_path}")


def main():
    """主函数"""
    # 初始化测试器
    tester = IntegrationTester()
    
    # 加载数据
    data_path = project_root / 'data' / 'train_with_models_1_100.json'
    samples = tester.load_samples(str(data_path))
    
    print(f"加载了 {len(samples)} 个样本\n")
    
    # 执行测试
    summary = tester.test_all_samples(samples)
    
    # 打印总结
    tester.print_summary(summary)
    
    # 分析未实现模型
    tester.analyze_unimplemented_models(summary)
    
    # 保存结果
    output_path = project_root / 'outputs' / 'integration_test_results.json'
    output_path.parent.mkdir(exist_ok=True)
    tester.save_results(summary, str(output_path))


if __name__ == '__main__':
    main()
