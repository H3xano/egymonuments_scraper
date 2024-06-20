import requests
import json
import os
from bs4 import BeautifulSoup

# Define the API endpoints for different categories
API_URLS = {
    "articles": "https://egymonuments.gov.eg/Umbraco/Api/AnnouncementWebAPI/GetAnnouncementPage",
    "archaeological_sites": "https://egymonuments.gov.eg/Umbraco/Api/EgyptianTreasuresWebAPI/GetEgyptianTreasuresPage",
    "monuments": "https://egymonuments.gov.eg/Umbraco/Api/EgyptianTreasuresWebAPI/GetEgyptianTreasuresPage",
    "museums": "https://egymonuments.gov.eg/Umbraco/Api/EgyptianTreasuresWebAPI/GetEgyptianTreasuresPage",
    "collections": "https://egymonuments.gov.eg/Umbraco/Api/EgyptianTreasuresWebAPI/GetEgyptianTreasuresPage",
    "sunken_monuments": "https://egymonuments.gov.eg/Umbraco/Api/EgyptianTreasuresWebAPI/GetEgyptianTreasuresPage"
}

# Define the request headers
HEADERS = {
    "Host": "egymonuments.gov.eg",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:127.0) Gecko/20100101 Firefox/127.0",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Referer": "https://egymonuments.gov.eg/ar/news",
    "culture": "ar",
    "Cache-Control": "no-cache",
    "Pragma": "no-cache",
    "Strict-Transport-Security": "max-age=60000; includeSubDomains",
    "Content-Type": "application/json",
    "Origin": "https://egymonuments.gov.eg",
    "DNT": "1",
    "Connection": "keep-alive",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "Sec-GPC": "1"
}

# Define the initial payloads for each category
PAYLOADS = {
    "articles": {
        "pageIndex": 0,
        "pageSize": 50,
        "filterationCriteria": {
            "containsStringValue": None,
            "nodeId": 1261,
            "announcementType": "All",
            "dateFrom": None,
            "dateTo": None
        }
    },
    "archaeological_sites": {
        "pageIndex": 0,
        "pageSize": 50,
        "filterationCriteria": {
            "selectedPeriods": [],
            "nodeId": 1263
        }
    },
    "monuments": {
        "pageIndex": 0,
        "pageSize": 50,
        "filterationCriteria": {
            "selectedPeriods": [],
            "nodeId": 1270
        }
    },
    "museums": {
        "pageIndex": 0,
        "pageSize": 50,
        "filterationCriteria": {
            "selectedPeriods": [],
            "nodeId": 1271
        }
    },
    "collections": {
        "pageIndex": 0,
        "pageSize": 50,
        "filterationCriteria": {
            "selectedPeriods": [],
            "nodeId": 1262
        }
    },
    "sunken_monuments": {
        "pageIndex": 0,
        "pageSize": 50,
        "filterationCriteria": {
            "selectedPeriods": [],
            "nodeId": 1276
        }
    }
}

def fetch_items(api_url, headers, payload, directory):
    """
    Fetch items (articles, archaeological sites, monuments, museums, collections, sunken monuments) from the API with pagination handling.

    Parameters:
    - api_url (str): The API endpoint URL.
    - headers (dict): Headers for the HTTP request.
    - payload (dict): The payload for the POST request.
    - directory (str): The directory to save the fetched items.

    Returns:
    - list: A list of items with their metadata.
    """
    items = []
    while True:
        response = requests.post(api_url, headers=headers, data=json.dumps(payload))
        if response.status_code != 200:
            print(f"Failed to fetch items: {response.status_code}")
            break

        data = response.json()
        for item in data['result']['items']:
            item_id = item['Id']
            file_path = os.path.join(directory, f"{item_id}.json")
            if os.path.exists(file_path):
                print(f"File {file_path} already exists. Skipping item ID {item_id}.")
                continue
            items.append(item)

        if payload['pageIndex'] >= data['result']['pagesCount'] - 1:
            break
        payload['pageIndex'] += 1

    return items

def fetch_full_content(url, selector):
    """
    Fetch full content from the item's URL.

    Parameters:
    - url (str): The relative URL of the item.
    - selector (str): The CSS selector to extract the content.

    Returns:
    - str: The text content from the specified div or None if not found.
    """
    full_url = f"https://egymonuments.gov.eg{url}"
    response = requests.get(full_url)
    if response.status_code != 200:
        print(f"Failed to fetch content from URL: {response.status_code}")
        return None

    soup = BeautifulSoup(response.content, 'html.parser')
    content_div = soup.select_one(selector)
    return content_div.get_text(strip=True) if content_div else None

def save_item(item, directory, selector):
    """
    Save an item to a JSON file after fetching its full content.

    Parameters:
    - item (dict): The item data.
    - directory (str): The directory to save the item.
    - selector (str): The CSS selector to extract the full content.
    """
    item_id = item['Id']
    file_path = os.path.join(directory, f"{item_id}.json")

    full_content = fetch_full_content(item['ContentUrlName'], selector)
    item_data = {
        'Title': item['Title'],
        'Location': item.get('Location', ''),
        'Description': item['Description'],
        'FullContent': full_content,
        'ContentUrlName': item['ContentUrlName']
    }

    with open(file_path, 'w', encoding='utf-8') as jsonfile:
        json.dump(item_data, jsonfile, ensure_ascii=False, indent=4)
    print(f"Saved item ID {item_id} to {file_path}")

def scrape_data(category, selector):
    """
    Scrape data for a specific category and save each item to a JSON file.

    Parameters:
    - category (str): The category to scrape (e.g., articles, archaeological_sites, etc.).
    - selector (str): The CSS selector to extract the full content.
    """
    print(f"Starting to fetch all {category}...")
    directory = category
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Created '{directory}' directory.")

    items = fetch_items(API_URLS[category], HEADERS, PAYLOADS[category], directory)
    print(f"Total {category} fetched: {len(items)}")

    for item in items:
        save_item(item, directory, selector)

    print(f"Finished scraping {category}.")

# Define selectors for different categories
selectors = {
    "articles": ".firstParagraph",
    "archaeological_sites": ".txtSection",
    "monuments": ".txtSection",
    "museums": ".txtSection",
    "collections": ".txtSection",
    "sunken_monuments": ".txtSection",
}

# Scrape data for each category
for category in API_URLS.keys():
    scrape_data(category, selectors[category])
