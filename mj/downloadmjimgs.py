##
# Download images from a CSV, two columns, first is prompt, second is URL
# Optimised for MJ Scraped images with discord scraper
# @see DiscordChatExporter.Cli
##
import aiohttp
import asyncio
import csv
import os
from urllib.parse import urlparse

input_file = input("input CSV: ")
output_directory = input("output Dir: ")

# Create the output directory if it doesn't exist
os.makedirs(output_directory, exist_ok=True)

# Function to download an image
async def download(session, url, counter, prompt):
    extension = os.path.splitext(url)[1]

    img_filename = str(counter) + extension
    txt_filename = str(counter) + '.txt'
    img_output_path = os.path.join(output_directory, img_filename)
    txt_output_path = os.path.join(output_directory, txt_filename)
    
    # If image file already exists, skip
    if os.path.isfile(img_output_path):
        print(f"Image file {img_output_path} already exists. Skipping...")
        return

    try:
        async with session.get(url) as resp:
            if resp.status == 200:
                with open(img_output_path, 'wb') as f:
                    f.write(await resp.read())
                    print( f"Downloaded image at {img_output_path}")

                with open(txt_output_path, 'w') as txt_file:
                    txt_file.write(prompt)
                    print( f"Written prompt to {txt_output_path}")

    except (asyncio.TimeoutError, aiohttp.client_exceptions.ClientPayloadError):
        print(f"Error when downloading {url}, skipping...")


# Main function that reads the CSV and starts the download tasks
async def main():
    tasks = []
    with open(input_file, 'r') as file:
        reader = csv.reader(file)
        data = list(reader)
    
    async with aiohttp.ClientSession() as session:
        for counter, row in enumerate(data, start=1):
            prompt, url = row
            if urlparse(url).scheme == '':
                print(f"Invalid URL: {url}. Skipping...")
                continue
            task = download(session, url, counter, prompt)
            tasks.append(task)

        await asyncio.gather(*tasks)

# Run the main function
asyncio.run(main())