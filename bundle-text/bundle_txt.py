##
# Combine text in txt files into one big txt file, one line equals one original txt file content
##
import os

# Directory path containing the .txt files
directory_path = '/path/to/files' # will recursively scan all folders

# Output file to store the combined content
output_file = 'combined_content.txt'

# List to store the content from each .txt file
content_list = []

# Loop through all .txt files in the directory
for file_name in os.listdir(directory_path):
    if file_name.endswith('.txt'):
        file_path = os.path.join(directory_path, file_name)
        with open(file_path, 'r') as file:
            content = file.read().strip()
            content_list.append(content)

# Combine the content into a single string with each content on a separate line
combined_content = '\n'.join(content_list)

# Write the combined content to the output file
output_file_path = os.path.join(directory_path, output_file)
with open(output_file_path, 'w') as output_file:
    output_file.write(combined_content)

print('Combined content saved to:', output_file_path)
