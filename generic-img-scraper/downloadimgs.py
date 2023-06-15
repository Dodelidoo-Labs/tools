##
# Scrape more general website - needs amendments according the HTML markup of the target site.
##
import aiohttp
import asyncio
from bs4 import BeautifulSoup
import os

async def download_image(session, url, alt_text):
    async with session.get(url) as response:
        if response.status == 200:
            image_data = await response.read()
            file_name = url.split("/")[-1]
            image_path = os.path.join("imgs", file_name)
            with open(image_path, "wb") as f:
                f.write(image_data)
            with open(os.path.splitext(image_path)[0] + ".txt", "w") as f:
                f.write(alt_text)
            print(f"Downloaded {file_name} with alt text: {alt_text}")

async def process_url(session, url):
    async with session.get(url) as response:
        if response.status == 200:
            html = await response.text()
            soup = BeautifulSoup(html, "html.parser")
            hrefs = soup.find_all(href=True, class_="highslide")
            tasks = []
            for href in hrefs:
                image_url = href["href"]
                img_tag = href.find("img")
                alt_text = img_tag.get("alt") if img_tag else ""
                tasks.append(download_image(session, image_url, alt_text))
            await asyncio.gather(*tasks)

async def main():
    os.makedirs("imgs", exist_ok=True)
    url = "Insert base URL here"
    async with aiohttp.ClientSession() as session:
        await process_url(session, url)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
