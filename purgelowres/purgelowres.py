import os
from PIL import Image

def delete_small_images(folder_path, width_threshold, height_threshold):
    Image.MAX_IMAGE_PIXELS = 100000000000000000000000000000000000000000000000000  # Stupidly high value to make sure BLIP does not bomb
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                with Image.open(file_path) as img:
                    try:
                        width, height = img.size
                        if width < width_threshold or height < height_threshold:
                            os.remove(file_path)
                            print(f"Deleted: {file_path}")

                            # Delete the corresponding .txt file
                            txt_file_path = os.path.splitext(file_path)[0] + ".txt"
                            if os.path.exists(txt_file_path):
                                os.remove(txt_file_path)
                                print(f"Deleted .txt file: {txt_file_path}")
                    except OSError as e:
                        if "DecompressionBombError" in str(e):
                            print(f"DecompressionBombError: {file_path} ({e})")
                        else:
                            raise
            except (IOError, OSError):
                # Skip files that cannot be opened as images
                continue

# Ask for folder path from user
folder_path = input("Enter the folder path: ")

# Set the width and height thresholds
width_threshold = 900
height_threshold = 900

# Delete small images
delete_small_images(folder_path, width_threshold, height_threshold)
