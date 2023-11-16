import csv
import json
from datetime import datetime

# File paths
input_filepath = 'dreams.csv'   # The name of your mixed CSV+JSON file
output_filepath = 'dreams-processed.csv' # The name of the desired output CSV file

# New CSV format
output_csv = []
headers = ["text", "date", "h_date"]
output_csv.append(headers)

# Open and read the input file
with open(input_filepath, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    
    # Skip the first two lines
    next(reader)
    next(reader)
    
    # Process each line
    for row in reader:
        _, _, json_data = row
        record = json.loads(json_data)
        
        text = record.get("text", "")
        date_timestamp = record.get("date", {}).get("T", "")
        if date_timestamp:
            h_date = datetime.utcfromtimestamp(int(date_timestamp) / 1000).strftime('%Y-%m-%d %H:%M:%S')
        else:
            h_date = ''  # or you can set a default value
        
        output_csv.append([text, date_timestamp, h_date])

# Write the transformed data to the output CSV file
with open(output_filepath, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerows(output_csv)

print(f"Output saved to {output_filepath}")
