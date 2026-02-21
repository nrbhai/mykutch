#!/usr/bin/env python3
"""
Extract meta titles and descriptions from destination HTML files
and add them to the translation JSON
"""
import json
from pathlib import Path
from bs4 import BeautifulSoup

def extract_meta_from_html(html_file):
    """Extract title and meta description from HTML file"""
    with open(html_file, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    
    # Get title
    title_tag = soup.find('title')
    title = title_tag.get_text().strip() if title_tag else ''
    
    # Get meta description
    meta_desc = soup.find('meta', attrs={'name': 'description'})
    description = meta_desc.get('content', '').strip() if meta_desc else ''
    
    return title, description

def main():
    base_dir = Path(__file__).parent / 'site'
    destinations_dir = base_dir / 'destinations'
    lang_dir = base_dir / 'lang'
    
    # Load English JSON
    en_file = lang_dir / 'en.json'
    with open(en_file, 'r', encoding='utf-8') as f:
        en_data = json.load(f)
    
    if 'destinations' not in en_data:
        en_data['destinations'] = {}
    
    # Get all destination HTML files
    html_files = [f for f in destinations_dir.glob('*.html') 
                  if not f.name.startswith('_') and f.name != 'destination-slug.html']
    
    print(f"Extracting SEO metadata from {len(html_files)} destination pages\n")
    
    updated_count = 0
    for html_file in html_files:
        slug = html_file.stem.replace('-', '_')
        title, description = extract_meta_from_html(html_file)
        
        if title or description:
            if slug not in en_data['destinations']:
                en_data['destinations'][slug] = {}
            
            # Only add if not already present
            if 'meta_title' not in en_data['destinations'][slug] and title:
                en_data['destinations'][slug]['meta_title'] = title
                print(f"✓ {slug}: Added meta_title")
                updated_count += 1
            
            if 'meta_desc' not in en_data['destinations'][slug] and description:
                en_data['destinations'][slug]['meta_desc'] = description
                print(f"✓ {slug}: Added meta_desc")
                updated_count += 1
    
    # Save back to English JSON
    with open(en_file, 'w', encoding='utf-8') as f:
        json.dump(en_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n{'='*70}")
    print(f"EXTRACTION COMPLETE!")
    print(f"{'='*70}")
    print(f"Added {updated_count} SEO metadata entries to en.json")
    print(f"These will be translated along with other content.")

if __name__ == '__main__':
    main()
