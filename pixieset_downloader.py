import requests
import json
import csv
import os
import time
from urllib.parse import urlparse
from datetime import datetime

def get_fresh_cookie(url):
    session = requests.Session()
    response = session.get(url)
    return session.cookies

def download_image(url, parent_dir, size_folder, original_name, size):
    try:
        full_path = os.path.join(parent_dir, size_folder)
        os.makedirs(full_path, exist_ok=True)
        response = requests.get(url)
        response.raise_for_status()
        
        name_parts = os.path.splitext(original_name)
        new_filename = f"{name_parts[0]}_{size}{name_parts[1]}"
        
        file_path = os.path.join(full_path, new_filename)
        with open(file_path, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded: {file_path}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to download {url}: {e}")

def download_images(base_url, cid):
    parsed_url = urlparse(base_url)
    domain = parsed_url.netloc
    path_parts = parsed_url.path.strip('/').split('/')
    gallery_name = path_parts[-1]
    
    photographer_name = domain.split('.')[0]
    current_date = datetime.now().strftime("%Y%m%d")
    parent_dir = f"{photographer_name}_{gallery_name}_{current_date}"
    os.makedirs(parent_dir, exist_ok=True)

    cookies = get_fresh_cookie(base_url)

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0",
        "Accept": "*/*",
        "Accept-Language": "en-CA,en-US;q=0.7,en;q=0.3",
        "Accept-Encoding": "gzip, deflate, br",
        "X-Requested-With": "XMLHttpRequest",
        "Connection": "keep-alive",
        "Referer": base_url,
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
    }

    photos = []
    page = 1

    while True:
        print(f"Fetching page: {page}")
        api_url = f"https://{domain}/client/loadphotos/?cuk={gallery_name}&cid={cid}&gs=highlights&fk=&clientDownloads=false&page={page}"
        
        try:
            response = requests.get(api_url, headers=headers, cookies=cookies)
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.RequestException as e:
            print(f'Failed to retrieve page: {e}')
            print(f'Response content: {response.text[:500]}...')
            break
        except json.JSONDecodeError as e:
            print(f'Failed to parse JSON: {e}')
            print(f'Response content: {response.text[:500]}...')
            break

        if data.get('status') == 'error':
            print(f"Error: {data.get('content')}")
            print("Refreshing cookie and retrying...")
            cookies = get_fresh_cookie(base_url)
            continue

        content = json.loads(data.get('content', '[]'))
        if not content:
            print('No more content. Stopping.')
            break

        photos.extend(content)

        if data.get('isLastPage', False):
            print("Reached last page. Stopping.")
            break

        page += 1
        time.sleep(2)

    if not photos:
        print("No photos found. Exiting.")
        return

    for photo in photos:
        original_name = photo.get('name', 'unknown')
        for size in ['Thumb', 'Small', 'Medium', 'Large', 'Xlarge', 'Xxlarge']:
            url_key = f'path{size}'
            if url_key in photo:
                img_url = 'https://' + photo[url_key].lstrip('//')
                size_folder = size.lower()
                download_image(img_url, parent_dir, size_folder, original_name, size)

    csv_path = os.path.join(parent_dir, 'image_data.csv')
    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = list(photos[0].keys())
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for photo in photos:
            writer.writerow(photo)

    print(f"Downloaded {len(photos)} images and created image_data.csv in {parent_dir}")

if __name__ == "__main__":
    base_url = input("Enter the Pixieset.com URL: ")
    cid = input("Enter the 'cid' value (you can find this in the network tab of your browser's developer tools): ")
    download_images(base_url, cid)
