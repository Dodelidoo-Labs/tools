import xml.etree.ElementTree as ET
import csv
import phpserialize

def parse_meta_value(value):
    try:
        data = phpserialize.loads(value.encode())
        result = []

        # Recursive function to drill down through nested dictionaries and lists
        def extract_items(data, prefix=""):
            if isinstance(data, dict):
                for key, val in data.items():
                    key_str = key.decode() if isinstance(key, bytes) else str(key)
                    if isinstance(val, (dict, list)):
                        result.append(f"{prefix}{key_str}:")
                        extract_items(val, prefix + "  ")  # Added indentation for nested structures
                    else:
                        val_str = val.decode() if isinstance(val, bytes) else str(val)
                        result.append(f"{prefix}{key_str} ({val_str})")
            elif isinstance(data, list):
                for idx, item in enumerate(data):
                    result.append(f"{prefix}Item {idx + 1}:")
                    extract_items(item, prefix + "  ")  # Added indentation for nested structures

        extract_items(data)
        return '\n'.join(result)
    except Exception as e:
        print(e)
        return value

tree = ET.parse('wpxml.xml')
root = tree.getroot()

namespace = {'wp': 'http://wordpress.org/export/1.2/', 'content': 'http://purl.org/rss/1.0/modules/content/', 'excerpt': 'http://wordpress.org/export/1.2/excerpt/'}

rows = []
all_meta_keys = set()  # Collect all meta keys

for item in root.findall(".//item", namespace):
    row_data = {}
    post_id_elem = item.find("wp:post_id", namespace)
    title_elem = item.find("title")
    content_elem = item.find("content:encoded", namespace)
    excerpt_elem = item.find("excerpt:encoded", namespace)
    post_type_elem = item.find("wp:post_type", namespace)

    post_id = post_id_elem.text if post_id_elem is not None else ""
    title = title_elem.text if title_elem is not None else ""
    content = content_elem.text if content_elem is not None else ""
    excerpt = excerpt_elem.text if excerpt_elem is not None else ""
    post_type = post_type_elem.text if post_type_elem is not None else ""
    row_data['Post ID'] = post_id
    row_data['Title'] = title
    row_data['Content'] = content
    row_data['Excerpt'] = excerpt
    row_data['Post Type'] = post_type
    meta_values = []

    for meta in item.findall("wp:postmeta", namespace):
        meta_key_elem = meta.find("wp:meta_key", namespace)
        meta_value_elem = meta.find("wp:meta_value", namespace)

        if meta_key_elem is not None and meta_value_elem is not None:
            meta_key = meta_key_elem.text
            meta_value = parse_meta_value(meta_value_elem.text)
            row_data[meta_key] = meta_value
            all_meta_keys.add(meta_key)  # Collect this meta key

    rows.append(row_data)
csv_columns = ['Post ID', 'Title', 'Content', 'Excerpt', 'Post Type'] + sorted(list(all_meta_keys))

with open('output.csv', 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
    writer.writeheader()
    for row in rows:
        writer.writerow(row)
