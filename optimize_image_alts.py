"""
Image Alt Tag Optimization Script for MyKutch.org
Updates image alt tags to be more descriptive and SEO-friendly
"""

import os
import re
from pathlib import Path
from bs4 import BeautifulSoup

# Mapping of common image names to better alt text
ALT_TEXT_IMPROVEMENTS = {
    # Destinations
    'mandvi': 'Mandvi beach and Vijay Vilas Palace on Arabian Sea coast in Kutch Gujarat',
    'mandvi beach': 'Mandvi Beach sunset on Arabian Sea coast in Kutch Gujarat',
    'vijayvilas': 'Vijay Vilas Palace in Mandvi, historic royal palace in Kutch',
    'shipbuilding': 'Traditional wooden shipbuilding yard in Mandvi, Kutch heritage craft',
    
    'bhuj': 'Bhuj city, capital of Kutch district in Gujarat India',
    'aina mahal': 'Aina Mahal palace in Bhuj, historic mirror palace in Kutch',
    'prag mahal': 'Prag Mahal palace in Bhuj, Gothic architecture in Kutch Gujarat',
    
    'white rann': 'White Rann of Kutch salt desert during Rann Utsav festival',
    'dhordo': 'Dhordo tent city at White Rann of Kutch during Rann Utsav',
    'rann': 'Great Rann of Kutch white salt desert in Gujarat',
    
    'dholavira': '5000 year old Harappan civilization archaeological site in Kutch',
    'harappan': 'Dholavira Harappan ruins, UNESCO World Heritage Site in Kutch',
    
    'kadia dhrow': 'Kadia Dhrow Grand Canyon of India with colorful rock formations in Kutch Gujarat',
    'kadia dungar': 'Kadia Dungar geological wonder with layered rocks in Kutch',
    
    # Crafts
    'bandhani': 'Bandhani tie-dye fabric with intricate dot patterns, traditional Kutch craft',
    'ajrakh': 'Ajrakh block-printed fabric with geometric patterns, traditional Kutch craft',
    'rogan': 'Rogan Art painted fabric with castor oil colors, traditional Kutch craft',
    'mirror work': 'Shisha mirror work embroidery, traditional Kutch craft',
    'pottery': 'Khavda pottery with red and white geometric patterns, traditional Kutch craft',
    'weaving': 'Kutch handloom weaving with vibrant patterns, traditional craft',
    'leather': 'Handcrafted leather goods with threadwork, traditional Kutch craft',
}

def improve_alt_text(current_alt, image_src, page_context):
    """Improve alt text based on current text, image source, and page context"""
    
    if not current_alt or current_alt.strip() == '':
        # Generate alt text from image filename
        filename = Path(image_src).stem.lower()
        
        # Check for known patterns
        for key, improved_text in ALT_TEXT_IMPROVEMENTS.items():
            if key in filename:
                return improved_text
        
        # Generate from filename and context
        clean_name = filename.replace('-', ' ').replace('_', ' ')
        if page_context:
            return f"{clean_name} in {page_context}, Kutch Gujarat"
        return f"{clean_name}, Kutch Gujarat tourism"
    
    # If alt text exists but is too short or generic
    current_lower = current_alt.lower()
    
    # Check if it needs improvement
    needs_improvement = (
        len(current_alt) < 20 or
        'kutch' not in current_lower and 'gujarat' not in current_lower
    )
    
    if needs_improvement:
        # Try to enhance existing alt text
        for key, improved_text in ALT_TEXT_IMPROVEMENTS.items():
            if key in current_lower:
                return improved_text
        
        # Add location context if missing
        if 'kutch' not in current_lower:
            return f"{current_alt} in Kutch Gujarat"
    
    return current_alt

def get_page_context(file_path):
    """Extract context from page (destination name, etc.)"""
    file_name = file_path.stem.lower()
    
    if 'mandvi' in file_name:
        return 'Mandvi'
    elif 'bhuj' in file_name:
        return 'Bhuj'
    elif 'dhordo' in file_name or 'white-rann' in file_name:
        return 'White Rann'
    elif 'dholavira' in file_name:
        return 'Dholavira'
    elif 'kadia' in file_name:
        return 'Kadia Dhrow'
    
    return 'Kutch'

def process_html_file(file_path):
    """Process a single HTML file to update image alt tags"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        page_context = get_page_context(file_path)
        
        # Find all img tags
        images = soup.find_all('img')
        updated_count = 0
        
        for img in images:
            current_alt = img.get('alt', '')
            src = img.get('src', '')
            
            # Skip if no src
            if not src:
                continue
            
            # Improve alt text
            new_alt = improve_alt_text(current_alt, src, page_context)
            
            # Update if changed
            if new_alt != current_alt:
                img['alt'] = new_alt
                updated_count += 1
        
        # Only write if changes were made
        if updated_count > 0:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(str(soup))
            return True, f"{file_path.name} ({updated_count} images updated)"
        
        return True, f"{file_path.name} (no changes needed)"
    
    except Exception as e:
        return False, f"{file_path.name}: {str(e)}"

def main():
    """Main function to process all HTML files"""
    site_dir = Path('site')
    
    if not site_dir.exists():
        print("Error: 'site' directory not found!")
        return
    
    # Find all HTML files
    html_files = list(site_dir.rglob('*.html'))
    
    print(f"Found {len(html_files)} HTML files to process for image alt tags...")
    print("-" * 60)
    
    success_count = 0
    error_count = 0
    total_images_updated = 0
    
    for html_file in html_files:
        success, message = process_html_file(html_file)
        
        if success:
            success_count += 1
            # Extract number of images updated
            if 'images updated' in message:
                count = int(message.split('(')[1].split(' ')[0])
                total_images_updated += count
            print(f"✓ {message}")
        else:
            error_count += 1
            print(f"✗ {message}")
    
    print("-" * 60)
    print(f"\nProcessing complete!")
    print(f"Success: {success_count} files")
    print(f"Total images updated: {total_images_updated}")
    print(f"Errors: {error_count} files")

if __name__ == '__main__':
    main()
