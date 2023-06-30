import os
import glob
import yaml
import math

def find_folders_with_images(root_directory, image_threshold):
    folders_with_images = []
    for root, dirs, files in os.walk(root_directory):
        image_count = len([file for file in files if file.endswith(('.jpg', '.jpeg', '.png'))])
        if image_count >= image_threshold:
            folders_with_images.append(root)
    return folders_with_images

def calculate_multiply_value(image_count):
    target_value = 150
    n = target_value / image_count
    rounded_n = round(n, 1)
    rounded_n = int(rounded_n) if rounded_n.is_integer() else rounded_n
    return rounded_n

def update_local_yaml(folder_path, multiply_value):
    yaml_file = os.path.join(folder_path, 'local.yaml')
    if os.path.isfile(yaml_file):
        with open(yaml_file, 'r') as file:
            try:
                yaml_data = yaml.safe_load(file)
                if yaml_data is None:
                    yaml_data = {}
                if 'multiply' in yaml_data:
                    del yaml_data['multiply']
                yaml_data['multiply'] = multiply_value
                with open(yaml_file, 'w') as updated_file:
                    yaml.dump(yaml_data, updated_file, default_flow_style=False, sort_keys=False)
                print(f'Updated local.yaml in folder: {folder_path}')
            except yaml.YAMLError as e:
                print(f'Error parsing YAML file: {yaml_file}')
                print(e)


# Provide the root directory to start scanning
root_directory = input("path: ")

# Set the threshold for the minimum number of images per folder
image_threshold = 50

# Find folders with at least the specified number of images
folders_with_images = find_folders_with_images(root_directory, image_threshold)

# Update local.yaml files in the found folders
for folder in folders_with_images:
    image_count = len(glob.glob(os.path.join(folder, '*.jpg')) +
                      glob.glob(os.path.join(folder, '*.jpeg')) +
                      glob.glob(os.path.join(folder, '*.png')))
    multiply_value = calculate_multiply_value(image_count)
    update_local_yaml(folder, multiply_value)