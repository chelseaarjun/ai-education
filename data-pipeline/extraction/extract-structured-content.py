#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Enhanced Content Extraction Script for AI Education Chatbot

This script extracts structured content from HTML files, capturing:
1. Hierarchical relationships between pages, modules, and sections
2. Links within content (both inline and reference links)
3. Rich metadata for improved retrieval and citation

The output is designed for use with vector databases like Supabase with pgvector.
"""

import os
import json
import re
import uuid
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration - Use absolute paths
ROOT_DIR = Path(__file__).resolve().parents[2] # ai-education root directory
PAGES_DIR = ROOT_DIR / "pages"
INDEX_FILE = ROOT_DIR / "index.html"
OUTPUT_DIR = ROOT_DIR / "data-pipeline" / "data"
OUTPUT_FILE = OUTPUT_DIR / "structured-content.json"

# Print paths for debugging
print(f"ROOT_DIR: {ROOT_DIR}")
print(f"PAGES_DIR: {PAGES_DIR}")
print(f"INDEX_FILE: {INDEX_FILE}")
print(f"OUTPUT_DIR: {OUTPUT_DIR}")
print(f"OUTPUT_FILE: {OUTPUT_FILE}")

# Ensure output directory exists
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Elements to ignore after extracting their information (navigation, footers, etc.)
IGNORE_SELECTORS = [
    '.course-nav',
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

# Content types
CONTENT_TYPES = {
    "INDEX": "index",
    "MODULE": "module",
    "SECTION": "section",
    "SUBSECTION": "subsection"
}

def clean_text(text):
    """Clean up text by removing extra whitespace, etc."""
    if not text:
        return ""
    # Replace multiple whitespace with single space
    text = re.sub(r'\s+', ' ', text)
    # Remove leading/trailing whitespace
    return text.strip()

def is_relative_url(url):
    """Check if a URL is relative to the current site."""
    if not url:
        return False
    return not bool(urlparse(url).netloc)

def get_content_type(file_path):
    """Determine the content type based on file path."""
    if "index.html" in str(file_path):
        return CONTENT_TYPES["INDEX"]
    if "/pages/" in str(file_path):
        return CONTENT_TYPES["MODULE"]
    return CONTENT_TYPES["SECTION"]

def extract_nav_sections(soup, url):
    """Extract section IDs and titles from module-nav elements."""
    nav_sections = []
    module_nav = soup.select_one('.module-nav')
    
    if module_nav:
        print(f"  Found module-nav in {url}")
        
        # First try to find buttons with data-section attributes (in newer modules)
        for button in module_nav.find_all('button', attrs={'data-section': True}):
            section_id = button.get('data-section')
            if section_id:
                nav_sections.append({
                    "id": section_id,
                    "title": clean_text(button.get_text()),
                    "url": f"{url}#{section_id}"
                })
                print(f"    Found nav section (button): {section_id} - {clean_text(button.get_text())}")
        
        # Also check for regular anchor links with href="#section-id" (in older modules)
        for link in module_nav.find_all('a'):
            href = link.get('href', '')
            if href.startswith('#'):
                section_id = href[1:]  # Remove the # character
                nav_sections.append({
                    "id": section_id,
                    "title": clean_text(link.get_text()),
                    "url": f"{url}#{section_id}"
                })
                print(f"    Found nav section (link): {section_id} - {clean_text(link.get_text())}")
    
    return nav_sections

def extract_links(element, base_url):
    """Extract all links from an HTML element."""
    links = []
    
    # Find all anchor tags
    anchors = element.find_all('a')
    for anchor in anchors:
        href = anchor.get('href')
        if not href:
            continue
            
        link_text = clean_text(anchor.get_text())
        if not link_text:
            link_text = "Link"
            
        # Determine if it's an internal or external link
        is_internal = is_relative_url(href)
        
        # For internal links, make sure we have a full path
        full_url = href
        if is_internal:
            full_url = urljoin(base_url, href)
            
        # Determine if this is a reference link based on context
        # (simplified version - looks for common patterns)
        is_reference = False
        parent = anchor.parent
        if parent:
            parent_text = parent.get_text().lower()
            if any(ref_term in parent_text for ref_term in 
                   ['reference', 'further reading', 'learn more', 'citation']):
                is_reference = True
                
        links.append({
            "id": str(uuid.uuid4()),
            "text": link_text,
            "url": full_url,
            "is_internal": is_internal,
            "is_reference": is_reference
        })
        
    return links

def extract_sections(soup, url, content_type):
    """Extract sections from the page based on module-nav and section IDs."""
    sections = []
    
    # First, extract section IDs from module-nav
    nav_sections = extract_nav_sections(soup, url)
    nav_section_ids = {section["id"] for section in nav_sections}
    
    # Create a mapping of section ID to nav title
    nav_titles = {section["id"]: section["title"] for section in nav_sections}
    
    # Clone the soup to keep original for later
    soup_copy = BeautifulSoup(str(soup), 'html.parser')
    
    # Remove elements we want to ignore
    for selector in IGNORE_SELECTORS:
        for element in soup_copy.select(selector):
            element.decompose()
    
    # Process each section with an ID from navigation
    processed_sections = set()
    
    # Find all sections with IDs matching nav_section_ids
    for section_id in nav_section_ids:
        section_elem = soup_copy.find(id=section_id)
        if section_elem:
            # Get section title from navigation or from first heading
            section_title = nav_titles.get(section_id)
            if not section_title:
                heading = section_elem.find(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
                section_title = clean_text(heading.get_text()) if heading else "Untitled Section"
            
            # Extract content
            section_text = clean_text(section_elem.get_text())
            links = extract_links(section_elem, url)
            
            if section_text:
                sections.append({
                    "id": section_id,
                    "title": section_title,
                    "content": section_text,
                    "type": CONTENT_TYPES["SECTION"],
                    "importance": 0.9,  # High importance for nav sections
                    "links": links,
                    "url": f"{url}#{section_id}"
                })
                processed_sections.add(section_id)
                print(f"    Processed section: {section_id}")
    
    # If no sections were found from nav, try finding module-section elements
    if not sections:
        module_sections = soup_copy.select('.module-section')
        
        # If no module-section found, try content-inner or main content
        if not module_sections:
            main_content = soup_copy.select_one('.content-inner, main, #content-inner, .content, body')
            if main_content:
                module_sections = [main_content]
        
        # Process each module section
        for i, module_section in enumerate(module_sections):
            # Get section ID if it exists
            section_id = module_section.get('id')
            
            # Skip already processed sections
            if section_id in processed_sections:
                continue
            
            # If no ID, generate one (but don't use it in URL)
            if not section_id:
                section_id = f"section-{i}"
                section_url = url  # No fragment if no ID
            else:
                section_url = f"{url}#{section_id}"
            
            # Get section title
            section_title_elem = module_section.find(['h1', 'h2', 'h3'])
            section_title = clean_text(section_title_elem.get_text()) if section_title_elem else f"Section {i+1}"
            
            # Extract content
            section_text = clean_text(module_section.get_text())
            links = extract_links(module_section, url)
            
            if section_text:
                sections.append({
                    "id": section_id,
                    "title": section_title,
                    "content": section_text,
                    "type": CONTENT_TYPES["SECTION"],
                    "importance": 0.8,
                    "links": links,
                    "url": section_url
                })
                processed_sections.add(section_id)
    
    # If we still don't have any sections, try to process the whole page
    if not sections:
        print(f"Warning: No sections found in {url}, processing as a single section")
        page_content = clean_text(soup_copy.get_text())
        if page_content:
            sections.append({
                "id": "page-content",
                "title": soup.title.string if soup.title else "Untitled Page",
                "content": page_content,
                "type": CONTENT_TYPES["SECTION"],
                "importance": 0.7,
                "links": extract_links(soup_copy, url),
                "url": url
            })
    
    # Add module URL as the first "section" for module pages
    if content_type == CONTENT_TYPES["MODULE"] and len(sections) > 0:
        # Create a "whole page" section that represents the entire module
        page_title = soup.title.string if soup.title else os.path.basename(url)
        module_name = os.path.splitext(os.path.basename(url))[0].replace('-', ' ').title()
        
        # Insert as the first section
        sections.insert(0, {
            "id": "module-overview",
            "title": f"{module_name} Overview",
            "content": f"This is the main page for the {module_name} module.",
            "type": CONTENT_TYPES["SECTION"],
            "importance": 1.0,  # Highest importance
            "links": [],
            "url": url  # URL without fragment for the main module page
        })
    
    return sections

def process_html_file(file_path, relative_url):
    """Process a single HTML file and extract structured content."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Extract basic metadata
        title = clean_text(soup.title.string) if soup.title else os.path.basename(file_path)
        
        # Determine content type
        content_type = get_content_type(file_path)
        
        # Extract content sections
        sections = extract_sections(soup, relative_url, content_type)
        
        # For pages, extract the module name from the title or first heading
        module_id = None
        if content_type == CONTENT_TYPES["MODULE"]:
            # Try to get a clean module name from filename or title
            module_name = os.path.splitext(os.path.basename(file_path))[0]
            module_id = f"Module: {module_name.replace('-', ' ').title()}"
        
        return {
            "id": str(uuid.uuid4()),
            "title": title,
            "url": relative_url,
            "type": content_type,
            "module_id": module_id,
            "sections": sections
        }
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None

def process_directory(directory, url_prefix):
    """Process all HTML files in a directory and its subdirectories."""
    pages = []
    
    if not directory.exists() or not directory.is_dir():
        print(f"Directory doesn't exist: {directory}")
        return pages
        
    # Process HTML files in this directory
    for html_file in directory.glob("*.html"):
        relative_url = f"{url_prefix}/{html_file.name}"
        print(f"Processing {html_file}")
        page = process_html_file(html_file, relative_url)
        if page:
            pages.append(page)
            
    # Process subdirectories
    for subdir in directory.iterdir():
        if subdir.is_dir() and not subdir.name.startswith('.'):
            subdir_name = subdir.name
            subdir_pages = process_directory(subdir, f"{url_prefix}/{subdir_name}")
            pages.extend(subdir_pages)
            
    return pages

def extract_parent_child_relationships(pages):
    """Create parent-child relationships between pages and sections."""
    # Map of URL to page
    url_to_page = {page["url"]: page for page in pages}
    
    # Also map URLs with fragments to their base pages
    for page in pages:
        base_url = page["url"].split("#")[0]
        if base_url != page["url"]:
            url_to_page[base_url] = page
    
    # For each page, look for links to other pages
    for page in pages:
        page["children"] = []
        
        # Special case for index.html - it's the parent of all modules
        if page["type"] == CONTENT_TYPES["INDEX"]:
            # Find all pages that are modules and make them children of index
            for potential_child in pages:
                if potential_child["type"] == CONTENT_TYPES["MODULE"] and potential_child["id"] != page["id"]:
                    page["children"].append({
                        "id": potential_child["id"],
                        "title": potential_child["title"],
                        "url": potential_child["url"],
                        "type": potential_child["type"]
                    })
        
        # Check sections for links
        for section in page["sections"]:
            section["parent_id"] = page["id"]
            
            for link in section["links"]:
                if link["is_internal"]:
                    # Handle both URLs with and without fragments
                    target_url = link["url"]
                    base_url = target_url.split("#")[0]
                    
                    # Try to find the target page
                    target_page = None
                    if target_url in url_to_page:
                        target_page = url_to_page[target_url]
                    elif base_url in url_to_page:
                        target_page = url_to_page[base_url]
                    
                    if target_page:
                        # Add as child if not already present
                        if target_page["id"] not in [child["id"] for child in page["children"]]:
                            page["children"].append({
                                "id": target_page["id"],
                                "title": target_page["title"],
                                "url": target_page["url"],
                                "type": target_page["type"]
                            })
    
    return pages

def main():
    """Main function to process all HTML files and generate JSON."""
    all_pages = []
    
    # Process index.html
    if INDEX_FILE.exists():
        print(f"Processing {INDEX_FILE}")
        index_page = process_html_file(INDEX_FILE, "index.html")
        if index_page:
            all_pages.append(index_page)
    else:
        print("Warning: index.html not found")
    
    # Process all HTML files in pages directory
    if PAGES_DIR.exists():
        print(f"Processing pages directory: {PAGES_DIR}")
        pages_content = process_directory(PAGES_DIR, "pages")
        all_pages.extend(pages_content)
    else:
        print(f"Warning: Pages directory not found: {PAGES_DIR}")
    
    # Extract parent-child relationships
    all_pages = extract_parent_child_relationships(all_pages)
    
    # Create output JSON
    output = {
        "pages": all_pages,
        "metadata": {
            "total_pages": len(all_pages),
            "total_sections": sum(len(page["sections"]) for page in all_pages),
            "extraction_date": str(Path(__file__).stat().st_mtime)
        }
    }
    
    # Save to file
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"\nExtraction complete! Processed {len(all_pages)} pages.")
    print(f"Output saved to {OUTPUT_FILE}")
    
    # Print some stats
    total_sections = sum(len(page["sections"]) for page in all_pages)
    total_links = sum(sum(len(section["links"]) for section in page["sections"]) for page in all_pages)
    print(f"Total sections extracted: {total_sections}")
    print(f"Total links extracted: {total_links}")

if __name__ == "__main__":
    main() 