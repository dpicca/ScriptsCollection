
# Web Scraping Scripts

This repository contains three scripts designed for web scraping purposes, specifically focusing on extracting personality type descriptions from various websites.

## 1. crawler.py

This script leverages the `requests` and `BeautifulSoup` libraries to crawl and extract content from web pages.

### Key Functions:
- `get_soup_from_link(link)`: Returns a BeautifulSoup object from a provided link.
- `get_text_from_link(link)`: Extracts and returns the textual content from a given link.
- `extract_subsection_links_from_soup(soup)`: Extracts subsection links from a BeautifulSoup object.

### Usage:
Provide an input file containing links and an output directory to store the extracted content. The script will read each link, fetch the content, and write it to a text file in the specified directory.
Example:
```
python crawler.py input_links.txt output_directory
```

---

## 2. mbti_scraper.py

A script that focuses on scraping MBTI personality type descriptions from a specific website using the `requests`, `BeautifulSoup`, and `os` libraries.

### Key Function:
- `extract_mbti_description(mbti_type)`: Extracts the MBTI personality type description from a given link.

### Usage:
Run the script with a folder name as an argument. The script will create the folder (if it doesn't exist), send a request to the base URL, extract descriptions for each personality type, and save each description to a separate text file within the folder. The script ensures all 16 personality types are extracted.
Example:
```
python mbti_scraper.py mbti_descriptions
```

---

## 3. mypersonality_scraper.py

Similar in functionality to `mbti_scraper.py`, this script appears to target a different website or section of a website to extract personality descriptions.

### Usage:
While specific details are similar to `mbti_scraper.py`, users should review the script to understand any unique nuances associated with the targeted website.
Example (assuming similar usage as mbti_scraper.py):
```
python mypersonality_scraper.py mypersonality_descriptions
```

---
Certainly, here's the README using the provided template:

---

## 4. mbti_scraper.py
Similar in functionality to other scraping scripts, this script targets the `typeinmind.com` website to extract descriptions of various MBTI personality types.

**Usage**:
While specific details are provided below, users should review the script to understand any unique nuances associated with the targeted website.

1. Ensure you have Python 3.x installed.
2. Install the necessary Python libraries:

```
pip install requests beautifulsoup4
```

3. Save the script into a file, e.g., `mbti_scraper.py`.
4. Open your terminal or command prompt.
5. Navigate to the directory where the script is located.
6. Run the script specifying the folder where you want the files to be saved:

**Example** (assuming similar usage as provided):

```
python mbti_scraper.py mbti_descriptions
```

After execution, you'll find all the text files with the extracted contents in the `mbti_descriptions` folder in your current directory.

---
---

## General Instructions:

- Ensure you have the required libraries installed using pip:
  ```
  pip install requests beautifulsoup4
  ```
- Always use the scripts responsibly, adhering to the terms of service of the websites you are scraping.
