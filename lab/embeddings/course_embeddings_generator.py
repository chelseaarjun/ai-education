# Course Content Embeddings Generator
# This notebook creates embeddings from course HTML files for use in the Module 3 Agent Lab

import os
import json
import boto3
import numpy as np
from bs4 import BeautifulSoup
import html2text
from datetime import datetime
from typing import List, Dict, Any
from pathlib import Path

# Configuration
COURSE_DIR = "/Users/arjunasoknair/workspace/ai-education"  # Update this path to your course directory
OUTPUT_FILE = "course_embeddings.json"
AWS_REGION = "us-west-2"  # Update if using different region
EMBEDDING_MODEL = "amazon.titan-embed-text-v2:0"

print("🚀 Course Content Embeddings Generator")
print("=" * 50)

# Setup AWS Bedrock client
try:
    bedrock_client = boto3.client("bedrock-runtime", region_name=AWS_REGION)
    print(f"✅ Connected to AWS Bedrock in {AWS_REGION}")
except Exception as e:
    print(f"❌ Failed to connect to AWS Bedrock: {e}")
    print("Please ensure your AWS credentials are configured correctly")
    exit(1)

def extract_text_from_html(html_file_path: str) -> List[Dict[str, Any]]:
    """
    Extract clean text from HTML file and chunk by sections
    
    Args:
        html_file_path: Path to HTML file
        
    Returns:
        List of content chunks with metadata
    """
    try:
        with open(html_file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
    except Exception as e:
        print(f"❌ Error reading {html_file_path}: {e}")
        return []
    
    # Setup html2text converter
    h = html2text.HTML2Text()
    h.ignore_links = True
    h.ignore_images = True
    h.ignore_emphasis = False
    h.body_width = 0  # Don't wrap lines
    
    # Parse HTML for section-based chunking
    soup = BeautifulSoup(html_content, 'html.parser')
    
    chunks = []
    file_name = os.path.basename(html_file_path)
    
    # Find all sections (or fallback to main content areas)
    sections = soup.find_all('section')
    
    if not sections:
        # Fallback: look for main content divs or just process whole file
        sections = soup.find_all(['div'], class_=['content', 'main', 'module-section'])
        
    if not sections:
        # Last resort: process entire file as one chunk
        full_text = h.handle(html_content)
        if full_text.strip():
            chunks.append({
                'content': full_text.strip(),
                'source': file_name,
                'section_id': 'full_content',
                'title': soup.find('title').get_text() if soup.find('title') else file_name,
                'word_count': len(full_text.split())
            })
    else:
        # Process each section
        for i, section in enumerate(sections):
            section_html = str(section)
            section_text = h.handle(section_html)
            
            if len(section_text.strip()) < 50:  # Skip very short sections
                continue
                
            # Extract title from section
            title_elem = section.find(['h1', 'h2', 'h3', 'h4'])
            title = title_elem.get_text().strip() if title_elem else f"Section {i+1}"
            
            chunks.append({
                'content': section_text.strip(),
                'source': file_name,
                'section_id': section.get('id', f'section_{i}'),
                'title': title,
                'word_count': len(section_text.split())
            })
    
    return chunks

def create_embedding(text: str) -> List[float]:
    """
    Create embedding for text using AWS Bedrock Titan
    
    Args:
        text: Text to embed
        
    Returns:
        Embedding vector as list of floats
    """
    try:
        # Titan embeddings API call
        response = bedrock_client.invoke_model(
            modelId=EMBEDDING_MODEL,
            body=json.dumps({
                "inputText": text
            })
        )
        
        response_body = json.loads(response['body'].read())
        return response_body['embedding']
        
    except Exception as e:
        print(f"❌ Error creating embedding: {e}")
        return []

def process_course_content():
    """
    Main function to process all course HTML files and create embeddings
    """
    print(f"\n📂 Processing course content from: {COURSE_DIR}")
    
    if not os.path.exists(COURSE_DIR):
        print(f"❌ Course directory not found: {COURSE_DIR}")
        print("Please update COURSE_DIR variable to point to your course content")
        return
    
    all_chunks = []
    processed_files = []
    
    # Process index.html
    index_path = os.path.join(COURSE_DIR, "index.html")
    if os.path.exists(index_path):
        print(f"📄 Processing: index.html")
        chunks = extract_text_from_html(index_path)
        all_chunks.extend(chunks)
        processed_files.append("index.html")
    
    # Process all HTML files in pages directory
    pages_dir = os.path.join(COURSE_DIR, "pages")
    if os.path.exists(pages_dir):
        html_files = [f for f in os.listdir(pages_dir) if f.endswith('.html')]
        
        for html_file in sorted(html_files):
            print(f"📄 Processing: pages/{html_file}")
            file_path = os.path.join(pages_dir, html_file)
            chunks = extract_text_from_html(file_path)
            all_chunks.extend(chunks)
            processed_files.append(f"pages/{html_file}")
    
    print(f"\n📊 Content Processing Summary:")
    print(f"   Files processed: {len(processed_files)}")
    print(f"   Total chunks: {len(all_chunks)}")
    print(f"   Total words: {sum(chunk['word_count'] for chunk in all_chunks):,}")
    
    if not all_chunks:
        print("❌ No content found to process")
        return
    
    # Create embeddings
    print(f"\n🧠 Creating embeddings using {EMBEDDING_MODEL}...")
    print("This may take a few minutes depending on content size...")
    
    embedded_chunks = []
    
    for i, chunk in enumerate(all_chunks):
        print(f"   Processing chunk {i+1}/{len(all_chunks)}: {chunk['title'][:50]}...")
        
        embedding = create_embedding(chunk['content'])
        
        if embedding:
            chunk['embedding'] = embedding
            embedded_chunks.append(chunk)
        else:
            print(f"   ⚠️  Failed to create embedding for chunk: {chunk['title']}")
    
    # Prepare final output
    output_data = {
        "metadata": {
            "created_at": datetime.now().isoformat(),
            "embedding_model": EMBEDDING_MODEL,
            "chunk_count": len(embedded_chunks),
            "total_words": sum(chunk['word_count'] for chunk in embedded_chunks),
            "embedding_dimension": len(embedded_chunks[0]['embedding']) if embedded_chunks else 0,
            "processed_files": processed_files
        },
        "chunks": embedded_chunks
    }
    
    # Save to file
    print(f"\n💾 Saving embeddings to: {OUTPUT_FILE}")
    
    try:
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Successfully saved {len(embedded_chunks)} embedded chunks")
        print(f"   File size: {os.path.getsize(OUTPUT_FILE) / 1024 / 1024:.1f} MB")
        
    except Exception as e:
        print(f"❌ Error saving embeddings: {e}")
        return
    
    # Validate the output
    print(f"\n🔍 Validation:")
    print(f"   Embedding dimension: {output_data['metadata']['embedding_dimension']}")
    print(f"   Sample chunk titles:")
    for chunk in embedded_chunks[:5]:
        print(f"      - {chunk['title']} ({chunk['word_count']} words)")
    
    print(f"\n🎉 Embeddings creation complete!")
    print(f"Use '{OUTPUT_FILE}' in your Module 3 Agent Lab")

def test_embeddings():
    """
    Test function to verify embeddings work correctly
    """
    if not os.path.exists(OUTPUT_FILE):
        print("❌ No embeddings file found. Run process_course_content() first.")
        return
    
    print(f"\n🧪 Testing embeddings from {OUTPUT_FILE}")
    
    try:
        with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        chunks = data['chunks']
        metadata = data['metadata']
        
        print(f"✅ Loaded {len(chunks)} chunks")
        print(f"✅ Embedding dimension: {metadata['embedding_dimension']}")
        
        # Test similarity calculation
        if len(chunks) >= 2:
            emb1 = np.array(chunks[0]['embedding'])
            emb2 = np.array(chunks[1]['embedding'])
            
            # Cosine similarity
            similarity = np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))
            print(f"✅ Sample similarity score: {similarity:.3f}")
        
        print("✅ Embeddings file is valid and ready for use!")
        
    except Exception as e:
        print(f"❌ Error testing embeddings: {e}")

# Main execution
if __name__ == "__main__":
    print("Choose an option:")
    print("1. Create embeddings from course content")
    print("2. Test existing embeddings file")
    
    choice = input("\nEnter choice (1 or 2): ").strip()
    
    if choice == "1":
        process_course_content()
    elif choice == "2":
        test_embeddings()
    else:
        print("Invalid choice. Please run the notebook again.")

# Uncomment the line below to run automatically without input
# process_course_content()