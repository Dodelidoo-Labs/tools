import json
import re

def remove_html_tags(text):
    # Remove HTML tags
    clean = re.compile('<.*?>')
    text_without_tags = re.sub(clean, '', text)

    # Replace multiple spaces with a single space
    text_single_space = re.sub(r'\s+', ' ', text_without_tags).strip()

    return text_single_space

def ensure_string_values(arg_obj):
    """Convert all non-string values in a dictionary to their string representations."""
    for key, value in arg_obj.items():
        if not isinstance(value, str):
            arg_obj[key] = str(value)
    return arg_obj

def extract_relevant_data(json_data):
    # List of keys we are interested in
    keys_of_interest = ["hooks", "functions", "methods", "classes"]
    
    # All the items we'll be extracting
    extracted_items = []

    # Iterate through all the items in the input data
    for item in json_data:
        for key in keys_of_interest:
            if key in item:
                for entry in item[key]:
                    # Extract the tags and clean their content
                    tags = []
                    if "doc" in entry and "tags" in entry["doc"]:
                        for tag in entry["doc"]["tags"]:
                            cleaned_tag = remove_html_tags(tag.get("content", ""))
                            tag["content"] = cleaned_tag
                            cleaned_desc = remove_html_tags(tag.get("description", ""))
                            tag["description"] = cleaned_desc
                            tags.append(tag)

                    # Create descriptions array with name, description, and long_description as strings
                    descriptions = [entry.get("name", "")]
                    if "doc" in entry:
                        description_text = remove_html_tags(entry["doc"].get("description", ""))
                        long_description_text = remove_html_tags(entry["doc"].get("long_description", ""))
                        
                        if description_text:
                            descriptions.append(description_text)
                        if long_description_text:
                            descriptions.append(long_description_text)

                    # Ensure arguments are always object[]
                    arguments = []
                    for idx, arg in enumerate(entry.get("arguments", [])): 
                        if isinstance(arg, str):
                            arguments.append({str(idx): arg})
                        else:  # It's already an object
                            arguments.append(ensure_string_values(arg))

                    # Construct the cleaned entry
                    cleaned_entry = {
                        "name": entry.get("name", ""),
                        "type": entry.get("type", ""),
                        "arguments": arguments,
                        "descriptions": descriptions,
                        "tags": tags
                    }
                    extracted_items.append(cleaned_entry)
                    
    return extracted_items







def write_to_jsonl(data, output_file):
    with open(output_file, 'w') as outfile:
        for entry in data:
            outfile.write(json.dumps(entry) + '\n')

def process_input(input_file, output_file):
    with open(input_file, 'r') as f:
        data = json.load(f)
    extracted_data = extract_relevant_data(data)
    write_to_jsonl(extracted_data, output_file)

# Usage
input_file = 'phpdoc.json'
output_file = 'phpdoc.jsonl'
process_input(input_file, output_file)
