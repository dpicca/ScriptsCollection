import requests
from bs4 import BeautifulSoup
import os
import sys

BASE_URL = "https://www.16-personality-types.com"

def get_mbti_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find all the MBTI type links
    mbti_links = {}
    for mbti_type in ["ISTJ", "ISFJ", "INFJ", "INTJ", "ISTP", "ISFP", "INFP", "INTP", "ESTP", "ESFP", "ENFP", "ENTP", "ESTJ", "ESFJ", "ENFJ", "ENTJ"]:
        link = soup.find('a', href=True, string=mbti_type)
        if link:
            mbti_links[mbti_type] = link['href']
    return mbti_links

def get_mbti_description(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract the main content of the page, which should contain the MBTI description
    content = soup.find('div', class_='entry-content')
    if content:
        return content.get_text(strip=True)
    return None

def main(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    mbti_links = get_mbti_links("https://www.16-personality-types.com/16-mbti-personality-types/")
    for mbti_type, link in mbti_links.items():
        description = get_mbti_description(link)
        if description:
            with open(os.path.join(folder_name, f"{mbti_type}.txt"), 'w') as file:
                file.write(description)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide a folder name as an argument.")
        sys.exit(1)
    folder_name = sys.argv[1]
    main(folder_name)
