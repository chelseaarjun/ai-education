#!/usr/bin/env python3
"""
Content Extraction Script for AI Education Chatbot

This script extracts relevant content from HTML files and converts it to a structured JSON format
for later embedding generation. It processes index.html and all HTML files in the pages/ directory.
"""

import os
import json
import re
import uuid
from pathlib import Path
from bs4 import BeautifulSoup

# Configuration
ROOT_DIR = Path(__file__).resolve().parents[2]  # ai-education root directory
PAGES_DIR = ROOT_DIR / "pages"
OUTPUT_DIR = ROOT_DIR / "chatbot" / "data"
OUTPUT_FILE = OUTPUT_DIR / "course-content.json"

# Ensure output directory exists
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Elements to ignore (these contain navigation, footers, etc.)
IGNORE_SELECTORS = [
    '.course-nav',
    '.module-nav',
    'nav',
    '.site-footer',
    'footer',
    'script',
    'style',
    '.navigation',
    '.nav-buttons'
]

# Section importance based on heading level (h1, h2, etc.)
HEADING_IMPORTANCE = {
    'h1': 1.0,
    'h2': 0.9,
    'h3': 0.8,
    'h4': 0.7,
    'h5': 0.6,
    'h6': 0.5
}

def clean_text(text):
    """Clean up text by removing extra whitespace, etc."""
    if not text:
        return ""
    # Replace multiple whitespace with single space
    text = re.sub(r'\s+', ' ', text)
    # Remove leading/trailing whitespace
    return text.strip()

def extract_sections(soup, url):
    """Extract sections from the page based on headings."""
    sections = []
    content_div = soup.select_one('.content-inner, .content, main, #content-inner')
    
    if not content_div:
        print(f"Warning: No main content div found in {url}")
        content_div = soup.body  # Fallback to body if no content div
    
    # Remove elements we want to ignore
    for selector in IGNORE_SELECTORS:
        for element in content_div.select(selector):
            element.decompose()
    
    # Find all headings
    headings = content_div.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
    
    # If no headings, treat the entire content as one section
    if not headings:
        section_text = clean_text(content_div.get_text())
        if section_text:
            sections.append({
                "id": str(uuid.uuid4()),
                "title": soup.title.string if soup.title else "Untitled",
                "content": section_text,
                "importance": 0.7  # Default importance
            })
        return sections
    
    # Process each heading and its content
    for i, heading in enumerate(headings):
        # Section title is the heading text
        title = clean_text(heading.get_text())
        if not title:
            continue
            
        # Get importance based on heading level
        importance = HEADING_IMPORTANCE.get(heading.name, 0.5)
        
        # Find all content until the next heading
        content_elements = []
        next_element = heading.next_sibling
        
        while next_element and (i == len(headings) - 1 or next_element != headings[i + 1]):
            if hasattr(next_element, 'get_text'):
                text = clean_text(next_element.get_text())
                if text:
                    content_elements.append(text)
            next_element = next_element.next_sibling
            # Break if we hit the next heading or a major section
            if next_element and next_element.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                break
        
        # Join content elements
        content = " ".join(content_elements)
        
        # Only add if there's actual content
        if content:
            sections.append({
                "id": str(uuid.uuid4()),
                "title": title,
                "content": content,
                "importance": importance
            })
    
    return sections

def process_html_file(file_path, relative_url):
    """Process a single HTML file and extract content."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Extract basic metadata
        title = clean_text(soup.title.string) if soup.title else os.path.basename(file_path)
        
        # Extract content sections
        sections = extract_sections(soup, relative_url)
        
        return {
            "id": str(uuid.uuid4()),
            "title": title,
            "url": relative_url,
            "sections": sections
        }
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None

def main():
    """Main function to process all HTML files and generate JSON."""
    pages = []
    
    # Process index.html
    index_path = ROOT_DIR / "index.html"
    if index_path.exists():
        print(f"Processing {index_path}")
        index_page = process_html_file(index_path, "index.html")
        if index_page:
            pages.append(index_page)
    
    # Process all HTML files in pages directory
    if PAGES_DIR.exists() and PAGES_DIR.is_dir():
        for html_file in PAGES_DIR.glob("*.html"):
            relative_url = f"pages/{html_file.name}"
            print(f"Processing {html_file}")
            page = process_html_file(html_file, relative_url)
            if page:
                pages.append(page)
    
    # Create output JSON
    output = {"pages": pages}
    
    # Save to file
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"\nExtraction complete! Processed {len(pages)} pages.")
    print(f"Output saved to {OUTPUT_FILE}")
    
    # Print some stats
    total_sections = sum(len(page["sections"]) for page in pages)
    print(f"Total sections extracted: {total_sections}")

if __name__ == "__main__":
    main() 