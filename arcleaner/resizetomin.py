import os
from PIL import Image
Image.MAX_IMAGE_PIXELS = 100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000

def get_aspect_ratio(image_path):
    with Image.open(image_path) as img:
        width, height = img.size
        aspect_ratio = width / height
        return aspect_ratio

def resize_image(image_path, new_size):
    with Image.open(image_path) as img:
        resized_img = img.resize(new_size)
        resized_img.save(image_path)

def scan_folder(folder_path):
    aspect_ratios = {}
    
    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            file_path = os.path.join(root, filename)
            
            # Check if the file is an image
            if os.path.splitext(filename)[1].lower() in ('.jpg', '.jpeg', '.png', '.gif'):
                aspect_ratio = get_aspect_ratio(file_path)
                if aspect_ratio not in aspect_ratios:
                    aspect_ratios[aspect_ratio] = []
                aspect_ratios[aspect_ratio].append(file_path)
    
    for aspect_ratio, image_paths in aspect_ratios.items():
        if len(image_paths) > 1:
            smallest_image_path = min(image_paths, key=os.path.getsize)
            with Image.open(smallest_image_path) as smallest_img:
                new_size = smallest_img.size
                for image_path in image_paths:
                    resize_image(image_path, new_size)

# Usage
folder_path = input("Enter the  file path: ")
scan_folder(folder_path)
