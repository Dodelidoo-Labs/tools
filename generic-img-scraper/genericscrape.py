##
# Scrapes any website for image urls and downlaods them.
# Able to bypass CloudFlare securities
##
import os
import cloudscraper
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import aiohttp
import aiofiles
import asyncio

def create_folder(name):
    os.makedirs(name, exist_ok=True)
    return name

async def download_image(session, url, folder):
    try:
        async with session.get(url) as response:
            if response.status == 200:
                f = await aiofiles.open(os.path.join(folder, url.split('/')[-1]), mode='wb')
                await f.write(await response.read())
                await f.close()
                print(f"Downloaded {url}")
            else:
                print(f"Failed to download {url}. Status: {response.status}")
    except Exception as e:
        print(f"Failed to download {url}. Reason: {e}")

def process_src(src, wikipedia=False):
    if wikipedia and '/thumb/' in src:
        src = src.replace('/thumb', '')  # Remove '/thumb'
        last_slash_index = src.rfind('/')  # Find the last occurrence of '/'
        src = src[:last_slash_index]  # Remove the last part after the last '/'
    return src

async def fetch_and_download(session, base_url, wikipedia_option, tag, class_, folder):
    scraper = cloudscraper.create_scraper()
    data = scraper.get(base_url).text
    soup = BeautifulSoup(data, "html.parser")
    elements = soup.find_all(tag, class_=class_)
    download_tasks = []
    for el in elements:
        src = el.get('src') if tag == 'img' else el.find('img', {}).get('src')
        src = process_src(src, wikipedia_option)
        if src:
            src = urljoin(base_url, src)  # Ensure the url is absolute
            task = asyncio.create_task(download_image(session, src, folder))
            download_tasks.append(task)
    await asyncio.gather(*download_tasks)

def get_user_input():
    base_url = input("Enter the base url to scrape: ")
    wikipedia_option = input("Enable Wikipedia processing? (y/n): ").lower() == 'y'
    tag = input("Enter the HTML tag: ")
    class_ = input("Enter the class of the tag: ")
    folder = input("Enter the folder path to save images: ")
    create_folder(folder)
    return base_url, wikipedia_option, tag, class_, folder

async def main(base_url, wikipedia_option, tag, class_, folder):
    async with aiohttp.ClientSession() as session:
        await fetch_and_download(session, base_url, wikipedia_option, tag, class_, folder)

if __name__ == '__main__':
    base_url, wikipedia_option, tag, class_, folder = get_user_input()
    asyncio.run(main(base_url, wikipedia_option, tag, class_, folder))
