import requests
from bs4 import BeautifulSoup
import os
import json
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

BASE_URLS = {
    'freesound': 'https://freesound.org',
    'soundbible': 'https://soundbible.com'
}

SEARCH_URLS = {
    'freesound': BASE_URLS['freesound'] + '/search/?q=',
    'soundbible': BASE_URLS['soundbible'] + '/search.php?q='
}

# Session 및 Retry Logic 설정
session = requests.Session()
retries = Retry(total=5, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504])
adapter = HTTPAdapter(max_retries=retries)
session.mount('http://', adapter)
session.mount('https://', adapter)

# User-Agent 설정
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

def search_sounds_freesound(query, page, num_sounds=5):
    sounds = []
    page_url = f"{SEARCH_URLS['freesound']}{query}&page={page}"
    response = session.get(page_url, headers=headers, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')
    new_sounds = [{'title': link.find('a').text.strip(), 'url': BASE_URLS['freesound'] + link.find('a')['href']}
                  for link in soup.find_all('div', {'class': 'sound_title'})]
    sounds.extend(new_sounds)
    return sounds

def search_sounds_soundbible(query, page, num_sounds=5):
    sounds = []
    page_url = f"{SEARCH_URLS['soundbible']}{query}&page={page}"
    response = session.get(page_url, headers=headers, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')
    new_sounds = [{'title': link.find('a').text.strip(), 'url': BASE_URLS['soundbible'] + '/' + link.find('a')['href']}
                  for link in soup.find_all('h3') if link.find('a')]
    sounds.extend(new_sounds)
    return sounds

def download_sound_freesound(sound_info, download_path):
    response = session.get(sound_info['url'], headers=headers, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')
    download_link = soup.find('a', {'class': 'mp3_file'})
    if download_link:
        download_link = BASE_URLS['freesound'] + download_link['href']
        response = session.get(download_link, headers=headers, timeout=10)
        response.raise_for_status()
        with open(download_path, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded Freesound: {download_path}")
    else:
        print(f"Download link not found for: {sound_info['url']}")

def download_sound_soundbible(sound_info, download_path):
    response = session.get(sound_info['url'], headers=headers, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')
    download_link = None
    for a_tag in soup.find_all('a'):
        href = a_tag.get('href', '')
        if href.endswith('mp3') and 'grab.php' in href:
            download_link = href
            break
    if download_link:
        response = session.get(download_link, headers=headers, timeout=10)
        response.raise_for_status()
        with open(download_path, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded SoundBible: {download_path}")
    else:
        print(f"Download link not found for: {sound_info['url']}")

def load_download_history(history_file):
    if os.path.exists(history_file):
        with open(history_file, 'r') as f:
            return json.load(f)
    return []

def save_download_history(history_file, download_history):
    with open(history_file, 'w') as f:
        json.dump(download_history, f)

def collect_sounds(keywords, output_dir='effect', num_sounds_per_keyword=5, history_file='download_history.json'):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    download_history = load_download_history(history_file)
    skipped_files = set()
    
    for site in ['freesound', 'soundbible']:
        print(f"Collecting sounds from {site}...")
        for keyword in keywords:
            print(f"Searching for sounds with keyword: {keyword}")
            page = 1
            downloaded_count = 0
            while downloaded_count < num_sounds_per_keyword:
                if site == 'freesound':
                    new_sounds = search_sounds_freesound(keyword, page, num_sounds=num_sounds_per_keyword)
                elif site == 'soundbible':
                    new_sounds = search_sounds_soundbible(keyword, page, num_sounds=num_sounds_per_keyword)
                
                # 새로운 소리가 없으면 루프 종료
                if not new_sounds:
                    break

                for sound_info in new_sounds:
                    if downloaded_count >= num_sounds_per_keyword:
                        break

                    sound_name = f"{site}_{sound_info['title'].replace(' ', '_')}.mp3"
                    if sound_name in download_history:
                        print(f"Skipping already downloaded sound: {sound_name}")
                        if sound_name in skipped_files:
                            print(f"Skipping same file twice, ending loop for {keyword}")
                            downloaded_count = num_sounds_per_keyword  # 강제로 종료
                            break
                        skipped_files.add(sound_name)
                        continue

                    print(f"Downloading sound: {sound_name}")
                    download_path = os.path.join(output_dir, sound_name)
                    download_function = download_sound_freesound if site == 'freesound' else download_sound_soundbible
                    download_function(sound_info, download_path)
                    download_history.append(sound_name)
                    save_download_history(history_file, download_history)
                    downloaded_count += 1

                page += 1

if __name__ == "__main__":
    keywords = ['bounce', 'collision', 'hit', 'impact', 'explosion','bouncy','anime','spring', 'jump', '']
    collect_sounds(keywords)
