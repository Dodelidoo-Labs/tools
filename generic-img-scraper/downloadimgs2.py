##
# Scrape a website to download images asynchroneusly.
# Defaulted the wallpaperflare.com
##
import requests
from bs4 import BeautifulSoup
import urllib.parse
import os
import concurrent.futures

def download_image(url, folder, alt):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        filename = url.split('/')[-1]
        subfolder = os.path.basename(folder)  # Get the subfolder name (e.g., 'dali')
        save_path = os.path.join(folder, filename)  # Include the subfolder in the save path
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        print(f"Downloaded {filename}")
        # Create and write to text file
        text_file_path = os.path.join(folder, f"{os.path.splitext(filename)[0]}.txt")  # Include the subfolder in the text file path
        with open(text_file_path, 'w') as text_file:
            text_file.write(alt)
    else:
        print(f"Failed to download {url}")

def process_image_link(link, base_url, folder):
    image_url = urllib.parse.urljoin(base_url, link['href']) + "/download"
    response = requests.get(image_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        img_tag = soup.find('img', id='show_img')
        if img_tag:
            image_url = img_tag['src']
            alt = img_tag.get('alt', '')
            download_image(image_url, folder, alt)
        else:
            print("Failed to find show_img link.")
    else:
        print(f"Failed to fetch {image_url}")

def main():
    wallpaper = input("Enter the search term: ")
    base_url = f"https://www.wallpaperflare.com/search?wallpaper={wallpaper}&width=1024&height=1024"

    download_folder = os.path.join('imgs_from_wp', wallpaper)
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    response = requests.get(base_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        image_links = soup.find_all('a', itemprop='url')

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for link in image_links:
                futures.append(executor.submit(process_image_link, link, base_url, download_folder))

            # Wait for all tasks to complete
            concurrent.futures.wait(futures)
    else:
        print(f"Failed to fetch {base_url}")

if __name__ == "__main__":
    main()