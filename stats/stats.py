import os
import csv

def count_image_files(directory):
    results = []
    for root, dirs, files in os.walk(directory):
        folder_name = os.path.basename(root)
        image_count = sum(1 for file_name in files if file_name.lower().endswith(('.jpg', '.png')))
        results.append([folder_name, image_count])
    return results

# Ask the user for the directory path
directory_path = input("Enter the directory path: ")

# Ask the user for the CSV file name
csv_file_name = input("Enter the CSV file name: ")

# Ask the user for the CSV file path
csv_file_path = input("Enter the CSV file path: ")

# Get the image file counts
image_file_counts = count_image_files(directory_path)

# Write the results to the CSV file
with open(csv_file_path, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Folder Name", "Image Count"])  # Write the header row
    writer.writerows(image_file_counts)  # Write the data rows

print(f"Image file counts have been written to '{csv_file_path}'.")
