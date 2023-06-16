from PIL import Image
import os
from collections import Counter

# Function to get the aspect ratio of an image
def get_aspect_ratio(image_path):
    with Image.open(image_path) as img:
        width, height = img.size
        gcd_val = gcd(width, height)
        return width // gcd_val, height // gcd_val

# Function to find the greatest common divisor
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

# Function to recursively scan folders and collect aspect ratios
def scan_folders(folder_path, aspect_ratios):
    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            if file.lower().endswith(('.jpg', '.png')):
                aspect_ratio = get_aspect_ratio(file_path)
                aspect_ratios.append(aspect_ratio)

# Function to list the 10 most common aspect ratios
def list_common_aspect_ratios(folder_path):
    aspect_ratios = []
    scan_folders(folder_path, aspect_ratios)
    common_ratios = Counter(aspect_ratios).most_common(10)

    print("The 10 most common aspect ratios:")
    for ratio, count in common_ratios:
        print(f"{ratio[0]}:{ratio[1]} - Count: {count}")

# Example usage
path_to_folder = input("Enter the root folder path: ")
list_common_aspect_ratios(path_to_folder)
