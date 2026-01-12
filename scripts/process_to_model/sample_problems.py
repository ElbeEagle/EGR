import json
import random
import os

# Paths
TRAIN_PATH = r"c:\Users\ThinkPad\Desktop\EGR\train.json"
TRAIN_MODELS_PATH = r"c:\Users\ThinkPad\Desktop\EGR\train_with_models.json"
MODEL_IDS_PATH = r"c:\Users\ThinkPad\Desktop\EGR\conic_model_ids.json"
OUTPUT_PATH = r"c:\Users\ThinkPad\Desktop\EGR\sampled_problems.md"

def load_json(path):
    print(f"Loading {path}...")
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def main():
    # Load data
    try:
        train_data = load_json(TRAIN_PATH)
        train_models_data = load_json(TRAIN_MODELS_PATH)
        model_ids = load_json(MODEL_IDS_PATH)
    except Exception as e:
        print(f"Error loading files: {e}")
        return
    
    # Invert model IDs to Name mapping
    # model_ids is {"Name": ID} -> we want {ID: "Name"}
    id_to_name = {v: k for k, v in model_ids.items()}
    
    # Basic validation
    if len(train_data) != len(train_models_data):
        print(f"Warning: train.json has {len(train_data)} items, train_with_models.json has {len(train_models_data)} items.")
        return

    # Find valid indices (non-empty process)
    print("Filtering for non-empty process...")
    valid_indices = []
    for i, item in enumerate(train_data):
        process = item.get('process')
        # Check if process is not None and not empty string
        if process and isinstance(process, str) and process.strip():
            # Check text match to ensure alignment (sanity check)
            if i < len(train_models_data) and train_models_data[i].get('text') == item.get('text'):
                valid_indices.append(i)
            
    print(f"Found {len(valid_indices)} items with non-empty process.")
    
    if not valid_indices:
        print("No items found with non-empty process.")
        return
    
    # Sample
    sample_size = min(80, len(valid_indices))
    print(f"Sampling {sample_size} items...")
    sampled_indices = random.sample(valid_indices, sample_size)
    sampled_indices.sort()
    
    # Generate Markdown
    lines = []
    lines.append(f"# Sampled 80 Problems with Non-Empty Process")
    lines.append(f"Total valid problems available: {len(valid_indices)}")
    lines.append(f"Sampled: {len(sampled_indices)}")
    lines.append("")
    
    for idx in sampled_indices:
        item_train = train_data[idx]
        item_models = train_models_data[idx]
        
        # Get models names
        models_list = item_models.get('models', [])
        models_names = [id_to_name.get(m_id, f"Unknown({m_id})") for m_id in models_list]
        
        lines.append(f"## Problem Index: {idx}")
        # ID if available in models
        if 'id' in item_models:
             lines.append(f"**ID**: {item_models['id']}")
             
        lines.append(f"**Text**:  \n{item_train['text']}")
        lines.append("")
        lines.append(f"**Process**:  \n{item_train['process']}")
        lines.append("")
        lines.append(f"**Theorem Sequence**:  \n{', '.join(models_names) if models_names else 'None'}")
        lines.append("")
        lines.append("---")
        lines.append("")
        
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
        
    print(f"Successfully saved to {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
