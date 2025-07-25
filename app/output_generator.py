# app/output_generator.py
import json

def generate_json_output(headings, output_path):
    """
    Formats the list of headings into the required JSON structure and saves it.
    """
    # The spec requires a root object with one key, "outline"
    output_data = {
        "outline": []
    }
    
    for heading in headings:
        output_data["outline"].append({
            "level": heading["level"],
            "text": heading["text"],
            "page": heading["page_num"]
        })
        
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=4)