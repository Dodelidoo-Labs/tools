import os
import re

def rename_files(directory):
    for root, dirs, files in os.walk(directory):
        for file_name in files:
            original_path = os.path.join(root, file_name)
            new_file_name = re.sub(r'[%_]', '', file_name)
            new_path = os.path.join(root, new_file_name)

            # Rename the file
            os.rename(original_path, new_path)

        for dir_name in dirs:
            rename_files(os.path.join(root, dir_name))

# Ask the user for the directory path
directory_path = input("Enter the directory path: ")

# Call the function to rename the files
rename_files(directory_path)
