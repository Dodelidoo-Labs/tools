import os

def rename_files_in_folder(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            old_file_path = os.path.join(root, file)
            base = os.path.splitext(file)[0]
            ext = os.path.splitext(file)[1]
            new_file_path = os.path.join(root, f"f-{base}{ext}")
            
            os.rename(old_file_path, new_file_path)  # Rename the file
            print(f"Renamed file {old_file_path} to {new_file_path}")

folder_path = input("Folder path: ")  # Replace with your folder path
rename_files_in_folder(folder_path)
