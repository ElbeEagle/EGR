"""
批量测试推理引擎

在Conic10K样本上测试推理引擎的端到端性能。
"""

import sys
import os
import json
import time
import random
from collections import Counter, defaultdict

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from src.reasoning import ReasoningEngine, ModelSelector
from src.reasoning.answer_comparator import compare_answers, safe_eval
from src.selector import MaxEntropyClassifier
from src.theorems import TheoremLibrary
from src.state import StateConstructor
import torch


def init_engine(verbose=False):
    """初始化推理引擎"""
    library = TheoremLibrary()
    constructor = StateConstructor(theorem_library=library)
    
    neural_network = MaxEntropyClassifier()
    try:
        checkpoint = torch.load('checkpoints/model_selector.pth', map_location='cpu')
        neural_network.load_state_dict(checkpoint['model_state_dict'])
    except Exception:
        print("⚠ 无法加载模型权重，使用未训练模型")
    neural_network.eval()
    
    selector = ModelSelector(neural_network, library, strategy='neural_topk')
    
    engine = ReasoningEngine(
        library, selector, constructor,
        max_steps=15,
        completeness_threshold=0.99,
        min_steps=1,
        max_retries_per_step=3,
        verbose=verbose
    )
    
    return engine


def load_test_data(path='data/train_with_models_v2.json', num_samples=200, seed=42):
    """加载并抽样测试数据"""
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 过滤：必须有fact_expressions、query_expressions、answer_expressions
    valid = [
        d for d in data
        if d.get('fact_expressions') and d.get('query_expressions') and d.get('answer_expressions')
    ]
    
    print(f"总样本: {len(data)}, 有效样本: {len(valid)}")
    
    # 抽样
    random.seed(seed)
    if num_samples < len(valid):
        samples = random.sample(valid, num_samples)
    else:
        samples = valid
    
    print(f"测试样本: {len(samples)}")
    return samples


def run_batch_test(engine, samples, verbose_failures=True):
    """批量测试"""
    results = []
    
    success_count = 0
    answer_correct = 0
    failure_reasons = Counter()
    curve_stats = defaultdict(lambda: {'total': 0, 'success': 0, 'correct': 0})
    query_stats = defaultdict(lambda: {'total': 0, 'success': 0, 'correct': 0})
    missing_models = Counter()
    step_counts = []
    failure_details = []
    
    total = len(samples)
    start_time = time.time()
    
    for i, sample in enumerate(samples):
        sid = sample['id']
        facts = sample['fact_expressions']
        query = sample['query_expressions']
        expected = sample['answer_expressions']
        
        # 分类统计
        curve_type = _detect_curve_type(facts)
        query_type = _detect_query_type(query)
        curve_stats[curve_type]['total'] += 1
        query_stats[query_type]['total'] += 1
        
        # 推理
        try:
            result = engine.solve(facts, query)
        except Exception as e:
            result = None
            failure_reasons['exception'] += 1
        
        # 评估
        if result and result.success:
            success_count += 1
            curve_stats[curve_type]['success'] += 1
            query_stats[query_type]['success'] += 1
            step_counts.append(result.num_steps)
            
            # 答案比较
            is_correct = compare_answers(result.answer, expected)
            if is_correct:
                answer_correct += 1
                curve_stats[curve_type]['correct'] += 1
                query_stats[query_type]['correct'] += 1
        else:
            reason = result.failure_reason if result else 'exception'
            # 简化原因分类
            if 'No applicable model' in str(reason):
                failure_reasons['no_model'] += 1
            elif 'max steps' in str(reason).lower():
                failure_reasons['max_steps'] += 1
            elif 'apply failed' in str(reason):
                failure_reasons['apply_failed'] += 1
            else:
                failure_reasons['other'] += 1
            
            # 记录失败详情（前30个）
            if len(failure_details) < 30:
                failure_details.append({
                    'id': sid,
                    'facts': facts[:100],
                    'query': query,
                    'expected': expected,
                    'reason': str(reason) if result else 'exception',
                    'steps': result.num_steps if result else 0,
                    'models_tried': result.model_names if result else []
                })
        
        # 进度
        if (i + 1) % 50 == 0 or i == total - 1:
            elapsed = time.time() - start_time
            rate = (i + 1) / elapsed
            print(f"  进度: {i+1}/{total} ({(i+1)*100/total:.0f}%)  "
                  f"成功:{success_count}  正确:{answer_correct}  "
                  f"速度:{rate:.1f}题/秒")
    
    elapsed = time.time() - start_time
    
    # 汇总
    report = {
        'summary': {
            'total_samples': total,
            'success_count': success_count,
            'success_rate': success_count / total if total > 0 else 0,
            'answer_correct': answer_correct,
            'accuracy': answer_correct / total if total > 0 else 0,
            'answer_accuracy_of_success': answer_correct / success_count if success_count > 0 else 0,
            'avg_steps': sum(step_counts) / len(step_counts) if step_counts else 0,
            'elapsed_seconds': round(elapsed, 1),
        },
        'failure_reasons': dict(failure_reasons),
        'curve_type_stats': {
            k: {
                'total': v['total'],
                'success_rate': v['success'] / v['total'] if v['total'] > 0 else 0,
                'accuracy': v['correct'] / v['total'] if v['total'] > 0 else 0,
            }
            for k, v in curve_stats.items()
        },
        'query_type_stats': {
            k: {
                'total': v['total'],
                'success_rate': v['success'] / v['total'] if v['total'] > 0 else 0,
                'accuracy': v['correct'] / v['total'] if v['total'] > 0 else 0,
            }
            for k, v in query_stats.items()
        },
        'failure_details': failure_details[:20],
    }
    
    return report


def _detect_curve_type(facts):
    """从facts中检测曲线类型"""
    fl = facts.lower()
    if 'ellipse' in fl:
        return 'Ellipse'
    elif 'hyperbola' in fl:
        return 'Hyperbola'
    elif 'parabola' in fl:
        return 'Parabola'
    elif 'circle' in fl:
        return 'Circle'
    return 'Other'


def _detect_query_type(query):
    """从query中检测查询类型"""
    ql = query.lower()
    if 'eccentricity' in ql:
        return 'Eccentricity'
    elif 'equation' in ql or 'expression' in ql:
        return 'Equation'
    elif 'length' in ql:
        return 'Length'
    elif 'coordinate' in ql:
        return 'Coordinate'
    elif 'distance' in ql:
        return 'Distance'
    elif 'area' in ql:
        return 'Area'
    elif 'range' in ql:
        return 'Range'
    return 'Value'


def print_report(report):
    """打印测试报告"""
    s = report['summary']
    
    print("\n" + "=" * 70)
    print("批量测试报告")
    print("=" * 70)
    
    print(f"\n总样本:  {s['total_samples']}")
    print(f"推理成功: {s['success_count']} ({s['success_rate']*100:.1f}%)")
    print(f"答案正确: {s['answer_correct']} ({s['accuracy']*100:.1f}%)")
    print(f"成功中正确率: {s['answer_accuracy_of_success']*100:.1f}%")
    print(f"平均步数: {s['avg_steps']:.1f}")
    print(f"耗时: {s['elapsed_seconds']}秒")
    
    print(f"\n失败原因分布:")
    for reason, count in sorted(report['failure_reasons'].items(), key=lambda x: -x[1]):
        print(f"  {reason}: {count}")
    
    print(f"\n按曲线类型:")
    for curve, stats in sorted(report['curve_type_stats'].items()):
        print(f"  {curve:12s}: total={stats['total']:3d}  "
              f"success={stats['success_rate']*100:5.1f}%  "
              f"accuracy={stats['accuracy']*100:5.1f}%")
    
    print(f"\n按查询类型:")
    for qtype, stats in sorted(report['query_type_stats'].items()):
        print(f"  {qtype:15s}: total={stats['total']:3d}  "
              f"success={stats['success_rate']*100:5.1f}%  "
              f"accuracy={stats['accuracy']*100:5.1f}%")
    
    print(f"\n失败案例 (前10个):")
    for fd in report['failure_details'][:10]:
        print(f"  id={fd['id']}: query={fd['query']}")
        print(f"    expected={fd['expected']}, reason={fd['reason'][:60]}")
    
    print("=" * 70)


def main():
    import argparse
    parser = argparse.ArgumentParser(description='批量测试推理引擎')
    parser.add_argument('--num', type=int, default=200, help='测试样本数')
    parser.add_argument('--seed', type=int, default=42, help='随机种子')
    parser.add_argument('--output', type=str, default='outputs/reasoning/batch_test_report.json')
    args = parser.parse_args()
    
    print("初始化推理引擎...")
    engine = init_engine(verbose=False)
    
    print("加载测试数据...")
    samples = load_test_data(num_samples=args.num, seed=args.seed)
    
    print(f"\n开始批量测试 ({args.num} 样本)...")
    report = run_batch_test(engine, samples)
    
    # 打印报告
    print_report(report)
    
    # 保存报告
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    print(f"\n报告已保存: {args.output}")


if __name__ == '__main__':
    main()
