import requests
from bs4 import BeautifulSoup
import os
import sys
import time

BASE_URL = "https://mypersonality.net"
RETRY_COUNT = 3
DELAY_BETWEEN_RETRIES = 5  # in seconds

def extract_mbti_description(mbti_type):
    url = f"{BASE_URL}/personality-type/{mbti_type.lower()}"
    
    for attempt in range(RETRY_COUNT):
        try:
            response = requests.get(url)
            if response.status_code != 200:
                print(f"Error accessing {url}: {response.status_code}. Retrying...")
                time.sleep(DELAY_BETWEEN_RETRIES)
                continue

            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Using the refined extraction method
            potential_elements = soup.find_all(['div', 'section'])
            
            for element in potential_elements:
                text_content = element.get_text()
                if "What is the meaning of" in text_content:
                    start_index = text_content.index("What is the meaning of")
                    return text_content[start_index:]
            
            print(f"Could not extract description for {mbti_type} from {url}")
            return None

        except requests.RequestException as e:
            print(f"Request error for {url}: {e}. Retrying...")
            time.sleep(DELAY_BETWEEN_RETRIES)

    print(f"Failed to access {url} after {RETRY_COUNT} attempts.")
    return None

def main(folder_name):
    # Creazione della cartella se non esiste
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    response = requests.get(f"{BASE_URL}/personality-type")
    soup = BeautifulSoup(response.content, 'html.parser')
    extracted_types = set()  # Using a set to ensure uniqueness

    for link in soup.find_all('a', href=True):
        if "/personality-type/" in link['href'] and len(link['href'].split('/')) == 3:
            mbti_type = link['href'].split('/')[-1]
            if mbti_type not in extracted_types:  # Check if this type was already processed
                content = extract_mbti_description(mbti_type)
                if content:
                    with open(os.path.join(folder_name, f"{mbti_type}.txt"), "w", encoding="utf-8") as file:
                        file.write(content)
                    extracted_types.add(mbti_type)

    if len(extracted_types) != 16:
        print("Not all personality types extracted. Extracted types are:")
        for etype in extracted_types:
            print(etype)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script_name.py <folder_name>")
        sys.exit(1)
    
    folder_name = sys.argv[1]
    main(folder_name)
