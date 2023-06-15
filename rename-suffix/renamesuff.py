import os

def rename_files(directory):
    for root, dirs, files in os.walk(directory):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            if file_name.endswith('.JPG'):
                new_file_path = file_path[:-3] + 'jpg'
                os.rename(file_path, new_file_path)
            elif file_name.endswith('.PNG'):
                new_file_path = file_path[:-3] + 'png'
                os.rename(file_path, new_file_path)

        for dir_name in dirs:
            rename_files(os.path.join(root, dir_name))

# Ask the user for the directory path
directory_path = input("Enter the directory path: ")

# Call the function to rename the files
rename_files(directory_path)
