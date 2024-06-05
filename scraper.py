import os
import time
import random
import requests
from bs4 import BeautifulSoup

BASE_URL = 'https://www.betaarchive.com/wiki/index.php?title=Category:Screenshots_Gallery'
SAVE_DIR = 'images'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def get_soup(url):
    print(f"Fetching URL: {url}")
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return BeautifulSoup(response.text, 'html.parser')

def save_image(img_url, folder):
    try:
        print(f"Downloading image: {img_url}")
        response = requests.get(img_url, headers=HEADERS)
        response.raise_for_status()
        filename = os.path.join(folder, img_url.split('/')[-1])
        with open(filename, 'wb') as f:
            f.write(response.content)
        time.sleep(random.uniform(1, 3))  # Sleep between 1 to 3 seconds
    except requests.exceptions.RequestException as e:
        print(f"Failed to download image {img_url}: {e}")

def get_image_url(file_page_url):
    try:
        soup = get_soup(file_page_url)
        img_tag = soup.find('a', class_='internal', title=True)
        if img_tag:
            return f"https://www.betaarchive.com{img_tag['href']}"
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch file page {file_page_url}: {e}")
    return None

def scrape_category(category_url):
    try:
        print(f"Scraping category: {category_url}")
        soup = get_soup(category_url)
        file_links = soup.select('a.galleryfilename')
        for link in file_links:
            file_page_url = f"https://www.betaarchive.com{link['href']}"
            img_url = get_image_url(file_page_url)
            if img_url:
                save_image(img_url, SAVE_DIR)
    except requests.exceptions.RequestException as e:
        print(f"Failed to scrape category {category_url}: {e}")

def scrape_subcategories(main_url):
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)
    try:
        print(f"Scraping main page: {main_url}")
        soup = get_soup(main_url)
        subcat_links = soup.select('div#mw-subcategories a')
        for link in subcat_links:
            subcat_url = f"https://www.betaarchive.com{link['href']}"
            scrape_category(subcat_url)
            time.sleep(random.uniform(1, 3))  # Sleep between 2 to 5 seconds
    except requests.exceptions.RequestException as e:
        print(f"Failed to scrape main page {main_url}: {e}")

scrape_subcategories(BASE_URL)
