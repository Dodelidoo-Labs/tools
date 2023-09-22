import os
from PIL import Image

def is_image_file(filename):
    supported_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']
    file_ext = os.path.splitext(filename)[1].lower()
    return file_ext in supported_extensions

def split_image(image_path, output_folder):
    # Open the image
    image = Image.open(image_path)

    # Get the dimensions of the original image
    width, height = image.size

    # Calculate the splitting positions
    x_split = width // 2
    y_split = height // 2

    # Split the image into four parts
    images = []
    for i in range(2):
        for j in range(2):
            left = i * x_split
            upper = j * y_split
            right = (i + 1) * x_split
            lower = (j + 1) * y_split
            cropped_image = image.crop((left, upper, right, lower))
            images.append(cropped_image)

    # Generate output file paths
    file_name = os.path.splitext(os.path.basename(image_path))[0]
    output_file_paths = [
        os.path.join(output_folder, f"{file_name}-v{i+1}{os.path.splitext(image_path)[1]}") for i in range(4)
    ]

    # Save the cropped images
    for i, cropped_image in enumerate(images):
        cropped_image.save(output_file_paths[i])
        print(f"Saved {output_file_paths[i]}")

# Folder path containing input images
input_folder = input("Input folder: ")

# Folder path to store output images
output_folder = input("Output folder: ")

# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Process each image in the input folder
for filename in os.listdir(input_folder):
    file_path = os.path.join(input_folder, filename)
    if is_image_file(filename):
        split_image(file_path, output_folder)
    else:
        print(f"Skipping non-image file: {filename}")
