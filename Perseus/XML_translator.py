
#!/usr/bin/env python3

import time
import textwrap
import concurrent.futures
import xml.etree.ElementTree as ET
from threading import Lock
import argparse

from deep_translator import GoogleTranslator
from tqdm.notebook import tqdm

# Constants
MAX_TOKENS = 5000

class GoogleRateLimiter:
    def __init__(self):
        self.last_call = time.time()

    def wait(self):
        elapsed_time = time.time() - self.last_call
        if elapsed_time < 0.2:
            time.sleep(0.2 - elapsed_time)
        self.last_call = time.time()

class ThreadSafeSet:
    def __init__(self):
        self.set = set()
        self.lock = Lock()

    def add(self, item):
        with self.lock:
            self.set.add(item)

    def items(self):
        with self.lock:
            return list(self.set)

def count_nodes(element):
    count = 0
    if element.text and element.text.strip():
        count += 1
    if element.tail and element.tail.strip():
        count += 1
    for child in element:
        count += count_nodes(child)
    return count

def split_into_chunks(text):
    return textwrap.wrap(text, MAX_TOKENS)

def translate_chunk(chunk, translator):
    try:
        return translator.translate(text=chunk)
    except Exception as e:
        unique_errors.add(str(e))
        return chunk

def translate_chunk_with_rate_limit(chunk, translator, rate_limiter):
    rate_limiter.wait()
    translated_text = translate_chunk(chunk, translator)
    return translated_text if translated_text is not None else ""

def translate_xml_text_with_rate_limit(element, translator, progress_bar, executor, rate_limiter):
    if element.text and element.text.strip():
        chunks = split_into_chunks(element.text)
        translated_chunks = list(executor.map(lambda chunk: translate_chunk_with_rate_limit(chunk, translator, rate_limiter), chunks))
        element.text = ''.join(filter(None, translated_chunks))
        progress_bar.update(1)
    
    for child in element:
        translate_xml_text_with_rate_limit(child, translator, progress_bar, executor, rate_limiter)
        if child.tail and child.tail.strip():
            chunks = split_into_chunks(child.tail)
            translated_chunks = list(executor.map(lambda chunk: translate_chunk_with_rate_limit(chunk, translator, rate_limiter), chunks))
            child.tail = ''.join(filter(None, translated_chunks))
            progress_bar.update(1)

def main():
    parser = argparse.ArgumentParser(description="Translate an XML file using Google's translation service.")
    parser.add_argument('--source', default='en', help='Source language.')
    parser.add_argument('--target', default='fr', help='Target language.')
    parser.add_argument('--input', required=True, help='Input XML filename.')
    parser.add_argument('--output', required=True, help='Output XML filename.')
    args = parser.parse_args()

    translator = GoogleTranslator(source=args.source, target=args.target)
    rate_limiter = GoogleRateLimiter()
    
    tree = ET.parse(args.input)
    root = tree.getroot()
    total_nodes = count_nodes(root)
    
    with tqdm(total=total_nodes, desc="Translating") as pbar:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            translate_xml_text_with_rate_limit(root, translator, pbar, executor, rate_limiter)
    
    tree.write(args.output)
    
    if unique_errors.items():
        print("Encountered the following unique errors during translation:")
        for error in unique_errors.items():
            print(error)

# Thread-safe set for errors
unique_errors = ThreadSafeSet()

if __name__ == "__main__":
    main()

