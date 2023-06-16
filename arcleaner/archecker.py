import os
import csv
from PIL import Image
import glob
from fractions import Fraction
import shutil

Image.MAX_IMAGE_PIXELS = 100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
def get_image_dimensions(image_path):
    with Image.open(image_path) as img:
        width, height = img.size
        aspect_ratio = Fraction(width, height)
        return width, height, aspect_ratio

def analyze_image_dimensions(folder_path):
    image_dimensions = {}
    image_files = glob.glob(os.path.join(folder_path, '**/*.jpg'), recursive=True) + glob.glob(os.path.join(folder_path, '**/*.png'), recursive=True)
    for image_path in image_files:
        try:
            width, height, aspect_ratio = get_image_dimensions(image_path)
            dimensions = f"{width}x{height}"
            aspect_ratio_str = f"{aspect_ratio.numerator}:{aspect_ratio.denominator}"
            image_dimensions.setdefault(dimensions, {"aspect_ratio": aspect_ratio_str, "count": 0})
            image_dimensions[dimensions]["count"] += 1

            # Copy and resize the image to a 150x150 size
            image_name = os.path.basename(image_path)
            new_image_path = os.path.join(folder_path, "resized_images", image_name)
            resize_image(image_path, new_image_path, (150, 150))

            # Add the image path to the image_dimensions dictionary
            image_dimensions[dimensions].setdefault("image_paths", [])
            image_dimensions[dimensions]["image_paths"].append(new_image_path)

        except (IOError, OSError, ValueError):
            print(f"Failed to process image: {image_path}")
    return image_dimensions

def resize_image(image_path, new_image_path, size):
    with Image.open(image_path) as image:
        image.thumbnail(size)
        image.save(new_image_path)


def write_image_dimensions_to_csv(csv_file_path, image_dimensions):
    with open(csv_file_path, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Image Dimensions", "Aspect Ratio", "Image Count", "Image", "Image Path"])  # Write the header row
        for dimensions, data in image_dimensions.items():
            for image_path in data.get("image_paths", []):
                writer.writerow([dimensions, data["aspect_ratio"], data["count"], image_path, os.path.abspath(image_path)])  # Write the data rows

# Ask the user for the directory path
directory_path = input("Enter the directory path: ")

# Ask the user for the CSV file path
csv_file_path = input("Enter the CSV file path: ")

# Check if the directory exists
if not os.path.isdir(directory_path):
    print("Invalid directory path.")
    exit()


# Create the "resized_images" directory
resized_images_dir = os.path.join(directory_path, "resized_images")
os.makedirs(resized_images_dir, exist_ok=True)

# Analyze the dimensions and aspect ratios of images in the directory and its subdirectories recursively
image_dimensions = analyze_image_dimensions(directory_path)

# Write the image dimensions, aspect ratios, and image counts to the CSV file
write_image_dimensions_to_csv(csv_file_path, image_dimensions)

print(f"Image dimensions, aspect ratios, counts, image paths, and resized images have been written to '{csv_file_path}'.")
