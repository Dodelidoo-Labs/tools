##
#Deletes files recursively in folder by extension
##
import os

def delete_files_by_extension(folder_path, file_extension):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(file_extension):
                file_path = os.path.join(root, file)
                os.remove(file_path)
                print(f"Deleted: {file_path}")

# Ask for folder path from user
folder_path = input("Enter the folder path: ")
file_extension = input("Enter the file extension (e.g., .txt): ")

# Validate file extension
if not file_extension.startswith('.'):
    file_extension = '.' + file_extension

# Delete files with the specified extension recursively
delete_files_by_extension(folder_path, file_extension)
