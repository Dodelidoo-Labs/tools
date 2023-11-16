import csv
import json

input_file = 'dreams-processed.csv'
output_file = 'dreams-processed.jsonl'

with open(input_file, 'r', newline='', encoding='utf-8') as csv_file, \
     open(output_file, 'w', encoding='utf-8') as jsonl_file:
     
    reader = csv.DictReader(csv_file)
    
    for row in reader:
        # Replacing newline characters
        for key, value in row.items():
            value = value.replace('\n', ' ')  # replacing newline characters with spaces
            row[key] = value
        
        jsonl_file.write(json.dumps(row, ensure_ascii=False) + '\n')
