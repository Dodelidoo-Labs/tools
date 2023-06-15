import os
from collections import Counter
from PIL import Image
from pathlib import Path

Image.MAX_IMAGE_PIXELS = 100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000

def aspect_ratio(width, height):
    ratio = width / height
    return round(ratio, 2)

def closest_aspect_ratio(width, height, aspect_ratios):
    ratio = width / height
    closest_ratio = min(aspect_ratios, key=lambda x: abs(x - ratio))
    return closest_ratio

def resize_or_crop_image(image_path, aspect_ratios):
    img = Image.open(image_path)
    width, height = img.size

    # Skip images that are smaller than 1200x900 or 900x1200
    if width < 1200 and height < 900 or width < 900 and height < 1200:
        print(f"Skipping {image_path} because it is too small")
        return

    aspect_ratio = closest_aspect_ratio(width, height, aspect_ratios)

    if abs(aspect_ratio - width/height) < 0.01:  # Adjust this value to control how close the aspect ratios need to be
        new_height = round(width / aspect_ratio)
        img = img.resize((width, new_height), Image.ANTIALIAS)
    else:  # If resizing isn't possible, crop
        if aspect_ratio > width/height:
            new_height = round(width / aspect_ratio)
            img = img.crop((0, 0, width, new_height))
        else:
            new_width = round(height * aspect_ratio)
            img = img.crop((0, 0, new_width, height))

    img.save(image_path)

def main():
    path = input("Enter the path to the directory: ")
    aspect_ratios_counter = Counter()

    # First pass: find the aspect ratios and count the occurrences
    for filename in Path(path).rglob('*'):
        if filename.is_file() and filename.suffix.lower() in ['.png', '.jpg', '.jpeg']:
            img = Image.open(filename)
            width, height = img.size
            aspect_ratios_counter[aspect_ratio(width, height)] += 1

    # Get aspect ratios with fewer than 10 images or not a multiple of 10 images
    filtered_ratios = [ratio for ratio, count in aspect_ratios_counter.items() if count < 10 or count % 10 != 0]

    # Filter out aspect ratios that have at least 10 images or a multiple of 10 images
    aspect_ratios = [ratio for ratio in aspect_ratios_counter.keys() if ratio not in filtered_ratios]

    # Second pass: resize or crop the images
    for filename in Path(path).rglob('*'):
        if filename.is_file() and filename.suffix.lower() in ['.png', '.jpg', '.jpeg']:
            print(f"Processing {filename}")
            resize_or_crop_image(str(filename), aspect_ratios)

if __name__ == "__main__":
    main()