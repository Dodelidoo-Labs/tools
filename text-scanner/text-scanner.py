import os
from PIL import Image
import pytesseract
from pytesseract import TesseractError

def find_images_with_text(folder_path):
    images_with_text = []
    
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                with Image.open(file_path) as img:
                    try:
                        # Perform OCR on the image
                        print( f"checking image {file_path}")
                        text = pytesseract.image_to_string(img)
                        if text.strip():
                            images_with_text.append(file_path)
                    except TesseractError as e:
                        print(f"Error processing image: {file_path} ({e})")
                        continue
            except (IOError, OSError):
                # Skip files that cannot be opened as images
                continue

    return images_with_text

# Ask for folder path from user
folder_path = input("Enter the folder path: ")

# Find images with text
result_list = find_images_with_text(folder_path)

# Print the final list of images with text
print("Images with text:")
for image_path in result_list:
    print(image_path)

# Ask for confirmation before deleting the images
confirmation = input("Do you want to delete these images? (y/n): ")

if confirmation.lower() == 'y':
    # Delete the images
    for image_path in result_list:
        os.remove(image_path)
        print(f"Deleted: {image_path}")
else:
    print("No images were deleted.")
