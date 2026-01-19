#!/usr/bin/env python3
"""
Audit and add missing alt text to images
"""

import os
import re
from bs4 import BeautifulSoup

def audit_images_in_file(file_path):
    """Audit images and add missing alt text"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    soup = BeautifulSoup(content, 'html.parser')
    images = soup.find_all('img')
    
    if not images:
        return 0, 0
    
    total_images = len(images)
    missing_alt = 0
    fixed = 0
    
    for img in images:
        if not img.get('alt') or img.get('alt').strip() == '':
            missing_alt += 1
            
            # Try to generate alt text from src
            src = img.get('src', '')
            if src:
                # Extract filename without extension
                filename = os.path.basename(src)
                filename = os.path.splitext(filename)[0]
                
                # Convert to readable text
                alt_text = filename.replace('-', ' ').replace('_', ' ').title()
                
                # Add location context
                if 'kutch' not in alt_text.lower():
                    alt_text += ' - Kutch, Gujarat'
                
                img['alt'] = alt_text
                fixed += 1
    
    # Write back if changes were made
    if fixed > 0:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(str(soup))
    
    return total_images, missing_alt, fixed

def audit_all_pages():
    """Audit all HTML pages"""
    
    total_files = 0
    total_images_count = 0
    total_missing = 0
    total_fixed = 0
    
    # Walk through all HTML files
    for root, dirs, files in os.walk('site'):
        # Skip backup directories
        if 'backup' in root or '_backup' in root:
            continue
        
        for file in files:
            if file.endswith('.html') and not file.endswith('.bak'):
                # Skip template and google verification files
                if '_template' in file or 'google' in file:
                    continue
                
                file_path = os.path.join(root, file)
                total_files += 1
                
                images, missing, fixed = audit_images_in_file(file_path)
                total_images_count += images
                total_missing += missing
                total_fixed += fixed
                
                if missing > 0:
                    print(f"📄 {file_path}")
                    print(f"   Images: {images}, Missing alt: {missing}, Fixed: {fixed}")
    
    print("\n" + "=" * 60)
    print("📊 Summary:")
    print(f"   Files processed: {total_files}")
    print(f"   Total images: {total_images_count}")
    print(f"   Missing alt text: {total_missing}")
    print(f"   Fixed: {total_fixed}")
    print("=" * 60)

if __name__ == '__main__':
    print("=" * 60)
    print("Image Alt Text Audit & Fix Script")
    print("=" * 60)
    print()
    
    audit_all_pages()
    
    print("\n✅ Audit complete!")
