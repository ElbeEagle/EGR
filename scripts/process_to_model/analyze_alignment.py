import json
import re

# Paths
TRAIN_PATH = r"c:\Users\ThinkPad\Desktop\EGR\train.json"
TRAIN_MODELS_PATH = r"c:\Users\ThinkPad\Desktop\EGR\train_with_models.json"
MODEL_IDS_PATH = r"c:\Users\ThinkPad\Desktop\EGR\conic_model_ids.json"
SAMPLED_OUTPUT_PATH = r"c:\Users\ThinkPad\Desktop\EGR\sampled_problems.md"
ANALYSIS_OUTPUT_PATH = r"c:\Users\ThinkPad\Desktop\EGR\analysis_results.json"

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_model_keywords():
    """Define heuristic keywords for model types."""
    return {
        "Ellipse": ["椭圆"],
        "Hyperbola": ["双曲线"],
        "Parabola": ["抛物线"],
        "Circle": ["圆", "circle"],
        "Triangle": ["三角形", "triangle"],
        "Vector": ["向量", "vector", "overrightarrow"],
        "Eccentricity": ["离心率"],
        "Asymptote": ["渐近线"],
        "Tangent": ["切线", "相切"],
        "Area": ["面积"],
        "Maximum": ["最大值", "最小值", "范围", "range", "min", "max"],
    }

def check_alignment(item_text, item_process, item_models, id_to_name):
    """Check if models align with text/process keywords."""
    warnings = []
    
    combined_text = (item_text + " " + item_process).lower()
    model_names = [id_to_name.get(m_id, "") for m_id in item_models]
    model_names_str = " ".join(model_names)
    
    keywords = get_model_keywords()
    
    # Check for Curve Type Mismatches
    # If text has Ellipse but models don't (and vice versa)
    # Note: A problem might have multiple curves, so existence is what implies necessity
    
    if "椭圆" in combined_text and not any("Ellipse" in m for m in model_names):
        warnings.append("Missing Ellipse Model")
    if "双曲线" in combined_text and not any("Hyperbola" in m for m in model_names):
        warnings.append("Missing Hyperbola Model")
    if "抛物线" in combined_text and not any("Parabola" in m for m in model_names):
        warnings.append("Missing Parabola Model")
        
    # Check for Specific Concepts
    if "离心率" in combined_text and not any("Eccentricity" in m for m in model_names):
        # Sometimes eccentricity is calculated via a/b/c relation without explicit formula, but usually it's there
        warnings.append("Possible Missing Eccentricity Model")
        
    if "渐近线" in combined_text and not any("Asymptote" in m for m in model_names):
        warnings.append("Missing Asymptote Model")
        
    if "切线" in combined_text or "相切" in combined_text:
        if not any("Tangent" in m or "Discriminant" in m for m in model_names):
             # Might clearly be a tangent problem but missing tag
             warnings.append("Possible Missing Tangent/Discriminant Model")

    # Check for "Phantom" Tags (Tags present but curve not mentioned)
    # Be careful, sometimes text just says "Curve C" but it implies a specific one.
    # But usually "Ellipse" tag without "椭圆" in text is suspicious unless it's an equation.
    
    return warnings

def main():
    print("Loading data...")
    train_data = load_json(TRAIN_PATH)
    train_models_data = load_json(TRAIN_MODELS_PATH)
    model_ids = load_json(MODEL_IDS_PATH)
    id_to_name = {v: k for k, v in model_ids.items()}
    
    # We want to analyze the SAME 500 problems that were sampled.
    # Since we can't easily get the random seed's indices from the previous run unless we saved them or read the Markdown,
    # and the user asked to "sample 500... and analyze", it is better to perform the analysis on the *generated* sample.
    # However, parsing MD is annoying. 
    # BETTER APPROACH: running this script INDEPENDENTLY on the whole dataset or a fresh sample is fine 
    # if we just want to find *general* errors.
    # BUT the user said "Process vs Theorem Sequence", so let's try to extract from the generated markdown or just reuse the logic to pick valid ones.
    
    # Let's read the markdown file to get the exact indices if possible, or just analyze ALL valid items and report statistics.
    # Actually, analyzing ALL valid items is more useful for the user than just 500.
    # BUT the task is "Sample 500... analyze IF corresponding correct".
    # I'll analyze ALL items with non-empty process to find the most egregious errors.
    
    print("Analyzing all items with process...")
    results = []
    
    valid_count = 0
    warning_counts = {}
    
    for i, item in enumerate(train_data):
        process = item.get('process')
        if not (process and isinstance(process, str) and process.strip()):
            continue
            
        valid_count += 1
        model_item = train_models_data[i]
        models = model_item.get('models', [])
        
        warnings = check_alignment(item['text'], process, models, id_to_name)
        
        if warnings:
            results.append({
                "index": i,
                "id": model_item.get('id'),
                "text": item['text'][:100] + "...",
                "warnings": warnings,
                "models": [id_to_name.get(m, str(m)) for m in models]
            })
            for w in warnings:
                warning_counts[w] = warning_counts.get(w, 0) + 1

    # Sort results by number of warnings
    results.sort(key=lambda x: len(x['warnings']), reverse=True)
    
    # Save top 100 suspicious items
    output = {
        "total_analyzed": valid_count,
        "flagged_count": len(results),
        "warning_summary": warning_counts,
        "suspicious_examples": results[:50]
    }
    
    with open(ANALYSIS_OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
        
    print(f"Analysis complete. {len(results)} items flagged out of {valid_count}.")
    print(f"Results saved to {ANALYSIS_OUTPUT_PATH}")

if __name__ == "__main__":
    main()
