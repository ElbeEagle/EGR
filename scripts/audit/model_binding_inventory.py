"""Reproducible structural inventory, not a semantic model-coverage benchmark."""
import argparse
import ast
from collections import Counter
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def build_inventory():
    data_path = ROOT / 'data/train_with_models_v3.json'
    raw = data_path.read_bytes()
    records = json.loads(raw)
    names = json.loads((ROOT / 'model/conic_model_ids.json').read_text())
    assert set(names.values()) == set(range(80))
    counts = Counter(mid for r in records for mid in set(r.get('models', [])))
    models = []
    for name, mid in sorted(names.items(), key=lambda item: item[1]):
        path = ROOT / f'src/theorems/models/model_{mid:03}.py'
        tree = ast.parse(path.read_text()) if path.exists() else ast.Module(body=[], type_ignores=[])
        methods = {n.name for cls in tree.body if isinstance(cls, ast.ClassDef)
                   for n in cls.body if isinstance(n, ast.FunctionDef)}
        candidates = sorted((r for r in records if mid in r.get('models', [])),
                            key=lambda r: (len(r['fact_expressions']), r['id']))[:3]
        models.append(dict(model_id=mid, name=name, source=str(path.relative_to(ROOT)),
                           legacy_methods_present={'can_apply', 'apply'} <= methods,
                           bound_method_present='propose_bound' in methods,
                           weak_label_record_count=counts[mid],
                           short_candidate_ids=[r['id'] for r in candidates]))
    return dict(schema_version='model-binding-inventory-v1',
                scope='AST method presence and weak-label counts; no semantic or runtime coverage claim',
                dataset_sha256=hashlib.sha256(raw).hexdigest(), records=len(records),
                bound_method_ids=[m['model_id'] for m in models if m['bound_method_present']],
                models=models)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    report = build_inventory()
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
    print(f"{len(report['models'])} IDs; {len(report['bound_method_ids'])} bound methods; {report['records']} records")
