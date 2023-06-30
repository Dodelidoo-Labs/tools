import os
from PIL import Image
from fractions import Fraction
Image.MAX_IMAGE_PIXELS = 100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000

def find_unique_aspect_ratio_images(folder_path):
    unique_images = {}  # Dictionary to store unique aspect ratios and their corresponding images

    # Recursively search for images in the folder
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                image_path = os.path.join(root, file)
                try:
                    with Image.open(image_path) as img:
                        aspect_ratio = Fraction(img.width, img.height)
                        if aspect_ratio not in unique_images:
                            unique_images[aspect_ratio] = []
                        unique_images[aspect_ratio].append(image_path)
                except (IOError, OSError):
                    # Handle invalid or corrupt images
                    pass

    # Filter out aspect ratios with only one image
    unique_aspect_ratios = {ratio: image_list for ratio, image_list in unique_images.items() if len(image_list) == 1}

    # Define the shared aspect ratios
    shared_aspect_ratios = [Fraction(1, 1), Fraction(16, 9), Fraction(4, 3)]  # Add or modify the desired aspect ratios

    # Iterate over the unique aspect ratios
    for aspect_ratio, image_list in unique_aspect_ratios.items():
        # Check if the aspect ratio is within tolerance of any shared aspect ratio
        for target_ratio in shared_aspect_ratios:
            if abs(aspect_ratio - target_ratio) <= Fraction(100, min(img.width, img.height)):
                # Crop or resize the image to the target aspect ratio
                for image_path in image_list:
                    try:
                        with Image.open(image_path) as img:
                            width, height = img.size
                            current_ratio = Fraction(width, height)

                            if current_ratio != target_ratio:
                                # Calculate the new dimensions
                                if current_ratio > target_ratio:
                                    new_width = int(height * target_ratio)
                                    left = (width - new_width) // 2
                                    right = left + new_width
                                    img = img.crop((left, 0, right, height))
                                    print(f"we would have changed this image {image_path} to be {new_width} wide")
                                else:
                                    new_height = int(width / target_ratio)
                                    top = (height - new_height) // 2
                                    bottom = top + new_height
                                    img = img.crop((0, top, width, bottom))
                                    print(f"we would have changed this image {image_path} to be {new_height} tall")

                                # Replace the original image with the cropped or resized image
                                #img.save(image_path)
                    except (IOError, OSError):
                        # Handle invalid or corrupt images
                        pass

# Provide the folder path to search for images
folder_path = input("Enter the folder path: ")
find_unique_aspect_ratio_images(folder_path)
