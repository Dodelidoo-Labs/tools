import os
from PIL import Image
Image.MAX_IMAGE_PIXELS = 100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000

aspect_ratios = [(16, 9), (1, 1), (8, 5), (3, 2), (4, 3), (3, 4), (2, 3), (2048, 1365), (5, 4), (43, 18)]

def get_closest_aspect_ratio(file_path, width, height):
    min_diff = float("inf")
    closest_width, closest_height = width, height

    for ratio in aspect_ratios:
        for w in range(width-50, width+50):
            h = w * ratio[1] / ratio[0]
            diff = abs(w - width) + abs(h - height)

            if diff < min_diff:
                min_diff = diff
                closest_width, closest_height = w, int(h)

    # Add user input check after each image processing
    # if abs(closest_width - width) > 500 or abs(closest_height - height) > 500:
    #     proceed = input(f"the image {file_path} would become {closest_width} x {closest_height} from {width} x {height}. Proceed? y/n:")
    #     if proceed.lower() != 'y':
    #         print(f"the image {file_path} will stay the same {closest_width} x {closest_height} from {width} x {height}")
    #         return  width, height

    #print(f"the image {file_path} will become {closest_width} x {closest_height} from {width} x {height}")
    return closest_width, closest_height

def process_image(file_path):
    with Image.open(file_path) as img:
        width, height = img.size
        original_aspect_ratio = (width, height)

        if original_aspect_ratio not in aspect_ratios:
            resize_width, resize_height = get_closest_aspect_ratio(file_path, width, height)

            # Check if resize is possible
            if abs(resize_width - width) <= 50 and abs(resize_height - height) <= 50:
                resized_img = img.resize((resize_width, resize_height))
                resized_img.save(file_path)
                print(f'Resized: {file_path}')
            else:
                # Crop image
                left = (width - resize_width)/2
                top = (height - resize_height)/2
                right = (width + resize_width)/2
                bottom = (height + resize_height)/2

                cropped_img = img.crop((left, top, right, bottom))
                cropped_img.save(file_path)
                print(f'Cropped: {file_path}')

def scan_folder(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.png') or file.endswith('.jpg'):
                file_path = os.path.join(root, file)
                process_image(file_path)

custom_path = input("Enter the Folder path: ")
scan_folder(custom_path)
