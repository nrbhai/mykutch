#!/usr/bin/env python3
"""
Add TouristAttraction structured data to destination pages
"""

import os
import re
from bs4 import BeautifulSoup

def add_structured_data_to_destination(file_path):
    """Add TouristAttraction and BreadcrumbList structured data"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    soup = BeautifulSoup(content, 'html.parser')
    head = soup.find('head')
    
    if not head:
        return False
    
    # Check if structured data already exists
    existing_schema = head.find('script', {'type': 'application/ld+json'})
    if existing_schema:
        print(f"  ⚠️  Structured data already exists, skipping")
        return False
    
    # Extract page info
    page_name = os.path.basename(file_path).replace('.html', '').replace('-', ' ').title()
    base_url = "https://www.mykutch.org"
    rel_path = file_path.replace('site/', '').replace('site\\', '').replace('\\', '/')
    page_url = f"{base_url}/{rel_path}"
    
    # Get title and description
    title_tag = head.find('title')
    desc_tag = head.find('meta', {'name': 'description'})
    
    title_text = title_tag.string if title_tag and title_tag.string else page_name
    desc_text = desc_tag.get('content', '') if desc_tag else f"Explore {page_name} in Kutch, Gujarat"
    
    # Get image if available
    og_image = head.find('meta', {'property': 'og:image'})
    image_url = og_image.get('content', f"{base_url}/assets/images/hero.webp") if og_image else f"{base_url}/assets/images/hero.webp"
    
    # Create TouristAttraction structured data
    tourist_attraction_schema = f'''
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "TouristAttraction",
      "name": "{title_text}",
      "description": "{desc_text}",
      "url": "{page_url}",
      "image": "{image_url}",
      "touristType": ["Cultural Tourism", "Heritage Tourism", "Nature Tourism"],
      "isAccessibleForFree": true,
      "address": {{
        "@type": "PostalAddress",
        "addressRegion": "Kutch",
        "addressCountry": "IN"
      }}
    }}
    </script>'''
    
    # Create BreadcrumbList structured data
    breadcrumb_schema = f'''
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "BreadcrumbList",
      "itemListElement": [
        {{
          "@type": "ListItem",
          "position": 1,
          "name": "Home",
          "item": "{base_url}/"
        }},
        {{
          "@type": "ListItem",
          "position": 2,
          "name": "Destinations",
          "item": "{base_url}/destinations.html"
        }},
        {{
          "@type": "ListItem",
          "position": 3,
          "name": "{page_name}",
          "item": "{page_url}"
        }}
      ]
    }}
    </script>'''
    
    # Insert before closing head tag
    head_closing = content.rfind('</head>')
    if head_closing != -1:
        new_content = (
            content[:head_closing] +
            tourist_attraction_schema + '\n' +
            breadcrumb_schema + '\n' +
            content[head_closing:]
        )
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"  ✓ Added TouristAttraction and BreadcrumbList structured data")
        return True
    
    return False

def process_all_destinations():
    """Process all destination pages"""
    dest_dir = 'site/destinations'
    
    if not os.path.exists(dest_dir):
        print(f"❌ Directory not found: {dest_dir}")
        return
    
    files = [f for f in os.listdir(dest_dir) if f.endswith('.html') and not f.endswith('.bak')]
    files = [f for f in files if '_template' not in f and 'google' not in f]
    
    print(f"\n📄 Adding structured data to {len(files)} destination pages...\n")
    
    count = 0
    for filename in sorted(files):
        file_path = os.path.join(dest_dir, filename)
        print(f"Processing: {filename}")
        if add_structured_data_to_destination(file_path):
            count += 1
        print()
    
    print(f"✅ Added structured data to {count} pages")

if __name__ == '__main__':
    print("=" * 60)
    print("Structured Data Enhancement Script")
    print("=" * 60)
    
    process_all_destinations()
    
    print("=" * 60)
    print("✅ Complete!")
    print("=" * 60)
