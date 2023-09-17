import requests
from bs4 import BeautifulSoup
import argparse
import os

def get_soup_from_link(link):
    """Given a link, return its BeautifulSoup object."""
    response = requests.get(link)
    if response.status_code != 200:
        return None
    return BeautifulSoup(response.text, 'html.parser')

def get_text_from_link(link):
    """Given a link, extract and return the textual content."""
    soup = get_soup_from_link(link)
    if not soup:
        return []
    
    # Extract main textual content
    article = soup.find('article', class_='main description')
    if not article:
        return []
    
    # For the strengths-and-weaknesses section, extract h2 and ul elements
    if "strengths-and-weaknesses" in link:
        sections = []
        elements = article.find_all(['h2', 'ul'])
        for element in elements:
            if element.name == 'h2':
                sections.append(element.get_text())
            elif element.name == 'ul':
                sections.extend([li.get_text() for li in element.find_all('li')])
        return sections

    # Return the text from the article
    return [article.get_text()]

def extract_subsection_links_from_soup(soup):
    """Given a BeautifulSoup object, extract the links of the subsections."""
    nav_element = soup.find('nav', class_='sections')
    if not nav_element:
        return []
    links = nav_element.find_all('a', href=True)
    return [link['href'] for link in links]

def main(input_file, output_directory, verbose):
    with open(input_file, 'r') as f:
        links = f.readlines()
    
    visited_links = set()
    for link in links:
        link = link.strip()
        if link in visited_links:
            continue
        visited_links.add(link)
        if verbose:
            print(f"Elaborazione del link: {link}")
        soup = get_soup_from_link(link)
        if not soup:
            continue
        profile_description = get_text_from_link(link)
        personality_type = link.split("/")[-1].split("-")[0]
        filename = os.path.join(output_directory, f"{personality_type}.txt")
        with open(filename, 'w', encoding='utf-8') as f:
            for section in profile_description:
                f.write(section + '\n\n')
        subsection_links = extract_subsection_links_from_soup(soup)
        for sub_link in subsection_links:
            if sub_link in visited_links:
                continue
            visited_links.add(sub_link)
            if verbose:
                print(f"Elaborazione della sottosezione: {sub_link}")
            section_content = get_text_from_link(sub_link)
            with open(filename, 'a', encoding='utf-8') as f:
                for section in section_content:
                    f.write(section + '\n\n')

    if verbose:
        print(f"I testi sono stati salvati in {output_directory}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract MBTI profile descriptions from given links.")
    parser.add_argument("input_file", type=str, help="Input file containing the links.")
    parser.add_argument("output_directory", type=str, help="Output directory to save the extracted text files.")
    parser.add_argument("--verbose", action='store_true', help="Print verbose output.")
    args = parser.parse_args()

    if not os.path.exists(args.output_directory):
        os.makedirs(args.output_directory)

    main(args.input_file, args.output_directory, args.verbose)
