import os
import re
import yaml
import glob

def delete_files_with_dot(folder):
    deleted_files = []
    for root, dirs, files in os.walk(folder):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            if file_name.startswith('.'):
                os.remove(file_path)
                deleted_files.append(file_path)

    return deleted_files

def check_image_txt_files(folder):
    errors = []
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp', '.tiff', '.bmp')):
                image_file = os.path.join(root, file)
                txt_file = os.path.join(root, os.path.splitext(file)[0] + '.txt')
                
                if not os.path.exists(txt_file):
                    errors.append(f"Missing text file for image: {image_file}")
                elif os.path.getsize(txt_file) == 0:
                    errors.append(f"Empty text file: {txt_file}")
    
    return errors

def check_txt_image_files(folder):
    errors = []
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.tiff', '.bmp']  # Add or remove image extensions as needed
    
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.lower().endswith('.txt'):
                txt_file = os.path.join(root, file)
                image_basename = os.path.splitext(txt_file)[0]
                
                # Find any image file that matches the basename
                image_files = [img for img in glob.glob(image_basename + '*') if os.path.splitext(img)[1] in image_extensions]
                
                if not image_files:  # If no image files were found, add to errors
                    errors.append(f"Missing image for txt file: {txt_file}")
    
    return errors

def check_txt_file_count(folder):
    errors = []
    for root, dirs, files in os.walk(folder):
        txt_files = [file for file in files if file.lower().endswith('.txt')]
        image_files = [file.lower() for file in files if file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp', '.tiff', '.bmp', '.JPG', '.JPEG', '.PNG', '.GIF', '.WEBP', '.TIFF', '.BMP'))]
        
        if len(txt_files) != len(image_files):
            diff = len(txt_files) - len(image_files)
            errors.append(f"Inconsistent number of text files in folder: {root}. Difference: {diff}")
    
    return errors

def check_yaml_files(folder):
    errors = []
    for root, dirs, files in os.walk(folder):
        yaml_files = [file for file in files if file.lower().endswith('.yaml')]
        
        if len(yaml_files) > 0:
            if len(dirs) == 0:
                local_yaml_file = os.path.join(root, 'local.yaml')
                if not os.path.exists(local_yaml_file):
                    errors.append(f"Missing local.yaml file in folder: {root}")
                elif os.path.getsize(local_yaml_file) == 0:
                    errors.append(f"Empty local.yaml file: {local_yaml_file}")
                else:
                    with open(local_yaml_file, 'r') as f:
                        data = yaml.safe_load(f)
                        if not data or 'tags' not in data or not data['tags']:
                            errors.append(f"Invalid local.yaml file: {local_yaml_file}")
                        else:
                            tag_text = data['tags'][0]['tag']
                            expected_tag_text = re.sub(r'[-]', ' ', os.path.basename(root))
                            expected_tag_text = f"in the style of {expected_tag_text}"
                            if tag_text != expected_tag_text:
                                errors.append(f"Mismatched tag in local.yaml file: {local_yaml_file} | Expected: {expected_tag_text} | Found: {tag_text}")
            else:
                global_yaml_file = os.path.join(root, 'global.yaml')
                if not os.path.exists(global_yaml_file):
                    errors.append(f"Missing global.yaml file in folder: {root}")
                elif os.path.getsize(global_yaml_file) == 0:
                    errors.append(f"Empty global.yaml file: {global_yaml_file}")
                else:
                    with open(global_yaml_file, 'r') as f:
                        data = yaml.safe_load(f)
                        if not data or 'tags' not in data or not data['tags']:
                            errors.append(f"Invalid global.yaml file: {global_yaml_file}")
                        else:
                            tag_text = data['tags'][0]['tag']
                            expected_tag_text = re.sub(r'[-]', ' ', os.path.basename(root))
                            if tag_text != expected_tag_text:
                                errors.append(f"Mismatched tag in global.yaml file: {global_yaml_file}")
    
    return errors

def check_folder_names(folder):
    errors = []
    for root, dirs, files in os.walk(folder):
        for dir in dirs:
            if not re.match(r'^[a-z-]+$', dir):
                errors.append(f"Invalid folder name: {os.path.join(root, dir)}")
    
    return errors

def check_folder_structure(folder):
    errors = []
    for root, dirs, files in os.walk(folder):
        if len(dirs) > 0:
            global_yaml_file = os.path.join(root, 'global.yaml')
            if not os.path.exists(global_yaml_file):
                errors.append(f"Missing global.yaml file in folder: {root}")
        else:
            local_yaml_file = os.path.join(root, 'local.yaml')
            if not os.path.exists(local_yaml_file):
                errors.append(f"Missing local.yaml file in folder: {root}")
    
    return errors

# Prompt the user to enter the folder to scan
folder_path = input("Enter the folder to scan: ")

# Validate the items based on the criteria
errors = []
errors.extend(check_image_txt_files(folder_path))
errors.extend(check_txt_file_count(folder_path))
errors.extend(check_yaml_files(folder_path))
errors.extend(check_folder_names(folder_path))
errors.extend(check_folder_structure(folder_path))
errors.extend(check_txt_image_files(folder_path))

# Print the list of errors
if errors:
    print("Validation errors found:")
    for error in errors:
        print(error)
else:
    print("Validation successful. No errors found.")

delete_files_with_dot(folder_path)
print("hidden files deleted")
