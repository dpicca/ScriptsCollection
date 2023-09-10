# MBTI Profile Description Extractor

This script is designed to extract personality profile descriptions from the 16Personalities website. It specifically targets the main description and all subsections for each personality type.

## Features

- Extracts the main personality description and all related subsections (e.g., "strengths-and-weaknesses", "romantic-relationships", etc.)
- Saves the extracted content in separate `.txt` files for each personality type.

## Requirements

- Python 3.x
- BeautifulSoup4 and Requests Python libraries.

## Usage

1. Prepare an input file containing the base links for each personality type, one link per line.
2. Specify an output directory where the extracted text files will be saved.

### Command Line Execution

```
python3 extractor_script.py input_file.txt output_directory --verbose
```

Arguments:
- `input_file.txt`: Path to the input file containing the base links.
- `output_directory`: Directory where the extracted text files will be saved.
- `--verbose`: (Optional) If set, the script will print out the links it's currently processing.

## How It Works

1. The script reads the base links for each personality type from the provided input file.
2. For each link, it extracts the main personality description.
3. It then identifies and extracts all related subsections by analyzing the page's navigation structure.
4. All the extracted content is saved in separate `.txt` files named after the personality type.

### Special Handling for "strengths-and-weaknesses"

Given the unique structure of the "strengths-and-weaknesses" section, the script has special logic to extract content from both the `<h2>` tags (titles) and the subsequent `<ul>` tags (lists of strengths and weaknesses).

---
