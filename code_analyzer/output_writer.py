import json

def write_json(data, path="outputs/extracted_knowledge.json"):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
