import os

def count_files(folder_path):
    file_count = 0
    for root, dirs, files in os.walk(folder_path):
        file_count += len(files)
    return file_count

# Prompt the user to enter the folder path
folder_path = input("Enter the folder path: ")
total_files = count_files(folder_path)
print(f"Total files: {total_files}")
