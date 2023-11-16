import xml.etree.ElementTree as ET
import csv
from bs4 import BeautifulSoup

# Parse the XML
filepath = input("XMLFilePath: ")
tree = ET.parse(filepath)
root = tree.getroot()

def strip_html(text):
    soup = BeautifulSoup(text, "html.parser")
    return soup.get_text()

# Extract post data
posts = []
for item in root.findall('.//item'):
    title = item.find('title').text
    content = item.find('{http://purl.org/rss/1.0/modules/content/}encoded').text
    url = item.find('link').text
    post_id = item.find('{http://wordpress.org/export/1.2/}post_id').text
    posts.append((title, content, url, post_id))
    
for idx, (title, content, url, post_id) in enumerate(posts):
    clean_content = strip_html(content)
    posts[idx] = (title, clean_content, url, post_id)

with open('processed_posts.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Title", "Content", "URL", "ID"])
    writer.writerows(posts)