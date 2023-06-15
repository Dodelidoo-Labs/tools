import os
import csv
import yaml

def get_multiply_value(folder_path):
    yaml_file = os.path.join(folder_path, "local.yaml")
    if os.path.isfile(yaml_file):
        with open(yaml_file) as file:
            data = yaml.safe_load(file)
            multiply_value = data.get("multiply")
            if multiply_value:
                return multiply_value
    return 1

def get_flip_value(folder_path):
    yaml_file = os.path.join(folder_path, "local.yaml")
    if os.path.isfile(yaml_file):
        with open(yaml_file) as file:
            data = yaml.safe_load(file)
            flip_value = data.get("flip_p")
            if flip_value:
                return flip_value
    return "NA"

def count_image_files(directory):
    results = []
    for root, dirs, files in os.walk(directory):
        folder_path = os.path.relpath(root, directory)
        multiply_value = get_multiply_value(root)
        flip_value = get_flip_value(root)
        image_count = sum(1 for file_name in files if file_name.lower().endswith(('.jpg', '.png')))
        total_images = image_count * multiply_value
        results.append([folder_path, multiply_value, image_count, total_images, flip_value])
    return results

# Ask the user for the directory path
directory_path = input("Enter the directory path: ")

# Ask the user for the CSV file path
csv_file_path = input("Enter the CSV file path: ")

# Get the image file counts
image_file_counts = count_image_files(directory_path)

# Write the results to the CSV file
with open(csv_file_path, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Folder Path", "Multiply Value", "Actual Image Count", "Total Images", "Flip Value"])  # Write the header row
    writer.writerows(image_file_counts)  # Write the data rows

print(f"Image file counts have been written to '{csv_file_path}'.")
