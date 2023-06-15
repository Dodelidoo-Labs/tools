##
# Download images from a CSV, two columns, first is prompt, second is URL
# Optimised for MJ Scraped images with discord scraper
# @see DiscordChatExporter.Cli
##
import csv
import os
import requests
from urllib.parse import urlparse

input_file = 'clean_img.csv'
output_directory = 'imgs_from_mj'
counter = 1

# Create the output directory if it doesn't exist
os.makedirs(output_directory, exist_ok=True)

with open(input_file, 'r') as file:
    reader = csv.reader(file)
    data = list(reader)

for row in data:
    url = row[1]
    prompt = row[0]
    extension = os.path.splitext(url)[1]  # Get the file extension from the URL

    # Check if the URL is valid
    if urlparse(url).scheme == '':
        print(f"Invalid URL: {url}. Skipping...")
        continue

    # Filenames
    img_filename = str(counter) + extension
    txt_filename = str(counter) + '.txt'
    img_output_path = os.path.join(output_directory, img_filename)
    txt_output_path = os.path.join(output_directory, txt_filename)

    # Download the image from the URL
    try:
        response = requests.get(url)
        response.raise_for_status()
        with open(img_output_path, 'wb') as f:
            f.write(response.content)

        with open(txt_output_path, 'w') as txt_file:
            txt_file.write(prompt)

        print(f"Downloaded and saved image: {img_filename}")
        print(f"Created and saved text prompt file: {txt_filename}")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading {url}: {e}")
        continue
    counter += 1

print("Image download, renaming and text prompts are complete.")