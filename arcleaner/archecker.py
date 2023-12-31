import os
import csv
from PIL import Image
import glob
from fractions import Fraction

Image.MAX_IMAGE_PIXELS = 100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000

def get_image_dimensions(image_path):
    with Image.open(image_path) as img:
        width, height = img.size
        aspect_ratio = Fraction(width, height)
        return aspect_ratio

def analyze_image_dimensions(folder_path):
    image_dimensions = {}
    image_files = glob.glob(os.path.join(folder_path, '**/*.jpg'), recursive=True) + glob.glob(os.path.join(folder_path, '**/*.png'), recursive=True)
    for image_path in image_files:
        try:
            aspect_ratio = get_image_dimensions(image_path)
            aspect_ratio_str = f"{aspect_ratio.numerator}:{aspect_ratio.denominator}"
            image_dimensions.setdefault(aspect_ratio_str, 0)
            image_dimensions[aspect_ratio_str] += 1
        except (IOError, OSError, ValueError):
            print(f"Failed to process image: {image_path}")
    return image_dimensions

def write_image_dimensions_to_csv(csv_file_path, image_dimensions):
    with open(csv_file_path, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Aspect Ratio", "Image Count"])  # Write the header row
        for aspect_ratio, count in image_dimensions.items():
            writer.writerow([aspect_ratio, count])  # Write the data rows

# Ask the user for the directory path
directory_path = input("Enter the directory path: ")

# Ask the user for the CSV file path
csv_file_path = input("Enter the CSV file path: ")

# Check if the directory exists
if not os.path.isdir(directory_path):
    print("Invalid directory path.")
    exit()

# Analyze the dimensions of images in the directory and its subdirectories recursively
image_dimensions = analyze_image_dimensions(directory_path)

# Write the aspect ratios and image counts to the CSV file
write_image_dimensions_to_csv(csv_file_path, image_dimensions)

print(f"Aspect ratios and counts have been written to '{csv_file_path}'.")
