import os

def find_empty_files(folder_path):
    empty_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            if os.path.getsize(file_path) == 0:
                empty_files.append(file_path)
    return empty_files

# Prompt the user to enter the folder path
folder_path = input("Enter the folder path: ")
empty_files = find_empty_files(folder_path)

if empty_files:
    print("Empty files found:")
    for file in empty_files:
        print(file)
        #os.remove(file)
else:
    print("No empty files found.")
