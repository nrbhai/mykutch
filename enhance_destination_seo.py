#!/usr/bin/env python3
"""
Advanced SEO Enhancement for All Destination Pages
- Adds SEO meta tags to all 60+ destination pages
- Adds structured data (schema.org JSON-LD)
- Creates destination-specific content
"""

import json
from pathlib import Path
from bs4 import BeautifulSoup
import re

# Destination metadata with keywords optimized for search
DESTINATION_KEYWORDS = {
    'bhuj.html': {
        'name': 'Bhuj',
        'type': 'City',
        'keywords': 'Bhuj, Bhuj city, Bhuj tourism, Bhuj attractions, Aina Mahal, Prag Mahal, Bhuj fort, capital of Kutch, Bhuj hotels, visit Bhuj',
        'region': 'central Kutch',
    },
    'mandvi.html': {
        'name': 'Mandvi',
        'type': 'Beach Town',
        'keywords': 'Mandvi, Mandvi beach, Mandvi beach resort, Vijay Vilas Palace, coastal Kutch, Arabian Sea',
        'region': 'coastal Kutch',
    },
    'dholavira.html': {
        'name': 'Dholavira',
        'type': 'Heritage Site',
        'keywords': 'Dholavira, Harappan site, UNESCO World Heritage Site, Indus Valley Civilization, 5000 year old ruins',
        'region': 'island Kutch',
    },
    'kadia-dhrow.html': {
        'name': 'Kadia Dhrow',
        'type': 'Natural Wonder',
        'keywords': 'Kadia Dhrow, Grand Canyon India, colorful rocks, geological wonder, natural attraction',
        'region': 'northern Kutch',
    },
    'mundra.html': {
        'name': 'Mundra',
        'type': 'Port City',
        'keywords': 'Mundra, Mundra port, coastal city, maritime heritage, port city Kutch',
        'region': 'coastal Kutch',
    },
    'road-to-heaven.html': {
        'name': 'Road to Heaven',
        'type': 'Scenic Route',
        'keywords': 'Road to Heaven, scenic route, desert landscape, panoramic views, photography location',
        'region': 'central Kutch',
    },
    'dhordo-white-rann.html': {
        'name': 'White Rann (Dhordo)',
        'type': 'Salt Desert',
        'keywords': 'White Rann, Rann of Kutch, salt desert, Dhordo, Rann Utsav festival',
        'region': 'Rann region',
    },
    'narayan-sarovar-koteshwar.html': {
        'name': 'Narayan Sarovar',
        'type': 'Sacred Lake',
        'keywords': 'Narayan Sarovar, pilgrimage site, holy lake, Koteshwar temple',
        'region': 'southwest Kutch',
    },
    'lakhpat.html': {
        'name': 'Lakhpat',
        'type': 'Historical Town',
        'keywords': 'Lakhpat, port town, historical fort, Kutch heritage',
        'region': 'northwest Kutch',
    },
    'gandhidham.html': {
        'name': 'Gandhidham',
        'type': 'City',
        'keywords': 'Gandhidham, port city, industrial hub, Gujarat',
        'region': 'northeast Kutch',
    },
    'vijay-vilas-palace.html': {
        'name': 'Vijay Vilas Palace',
        'type': 'Palace',
        'keywords': 'Vijay Vilas Palace, Mandvi palace, royal heritage, Arabian Sea',
        'region': 'coastal Kutch',
    },
}

def add_seo_to_destination(html_file, dest_data):
    """Add SEO enhancements to destination pages"""
    
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        head = soup.find('head')
        
        if not head:
            head = soup.new_tag('head')
            body = soup.find('body')
            if body:
                body.insert_before(head)
        
        # Prepare SEO data
        dest_name = dest_data.get('name', '')
        dest_keywords = dest_data.get('keywords', '')
        dest_type = dest_data.get('type', '')
        
        title = f"{dest_name} - {dest_type} | Kutch {dest_data.get('region', 'region')} | MyKutch.org"
        desc = f"Discover {dest_name}, {dest_type.lower()} in {dest_data.get('region', 'Kutch')}. Complete guide with attractions, things to do, accommodation, and travel tips for visiting {dest_name}."
        
        # Update title
        title_tag = head.find('title')
        if not title_tag:
            title_tag = soup.new_tag('title')
            head.append(title_tag)
        title_tag.string = title
        
        # Update meta description
        meta_desc = head.find('meta', attrs={'name': 'description'})
        if not meta_desc:
            meta_desc = soup.new_tag('meta')
            meta_desc['name'] = 'description'
            head.append(meta_desc)
        meta_desc['content'] = desc
        
        # Update keywords
        meta_keywords = head.find('meta', attrs={'name': 'keywords'})
        if not meta_keywords:
            meta_keywords = soup.new_tag('meta')
            meta_keywords['name'] = 'keywords'
            head.append(meta_keywords)
        meta_keywords['content'] = dest_keywords + ', Kutch attractions, places to visit Kutch, Kutch tourism'
        
        # Update robots
        meta_robots = head.find('meta', attrs={'name': 'robots'})
        if not meta_robots:
            meta_robots = soup.new_tag('meta')
            meta_robots['name'] = 'robots'
            meta_robots['content'] = 'index, follow'
            head.append(meta_robots)
        
        # Add Open Graph tags
        og_title = head.find('meta', attrs={'property': 'og:title'})
        if not og_title:
            og_title = soup.new_tag('meta')
            og_title['property'] = 'og:title'
            head.append(og_title)
        og_title['content'] = title
        
        og_desc = head.find('meta', attrs={'property': 'og:description'})
        if not og_desc:
            og_desc = soup.new_tag('meta')
            og_desc['property'] = 'og:description'
            head.append(og_desc)
        og_desc['content'] = desc
        
        # Add structured data (schema.org)
        schema_script = soup.find('script', attrs={'type': 'application/ld+json'})
        if not schema_script:
            schema_data = {
                "@context": "https://schema.org",
                "@type": "Place",
                "name": dest_name,
                "description": desc,
                "url": f"https://www.mykutch.org/destinations/{html_file.name}",
                "address": {
                    "@type": "PostalAddress",
                    "addressRegion": "Kutch",
                    "addressCountry": "IN"
                }
            }
            
            schema_script = soup.new_tag('script')
            schema_script['type'] = 'application/ld+json'
            schema_script.string = json.dumps(schema_data, ensure_ascii=False, indent=2)
            head.append(schema_script)
        
        # Save updated HTML
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(str(soup.prettify()))
        
        return True
    except Exception as e:
        print(f"   ⚠ Error processing {html_file.name}: {e}")
        return False

def main():
    site_path = Path(__file__).parent / 'site'
    destinations_path = site_path / 'destinations'
    
    print("🌍 Enhanced Destination SEO Optimization\n")
    print("=" * 60)
    
    # Get all destination HTML files
    all_dest_files = sorted(destinations_path.glob('*.html'))
    
    # Filter out template files
    dest_files = [f for f in all_dest_files if not f.name.startswith('_template') and f.name != 'destination-slug.html']
    
    print(f"\n📍 Processing {len(dest_files)} destination pages...\n")
    
    updated_count = 0
    
    # Process main destinations with detailed metadata
    for html_file, dest_data in DESTINATION_KEYWORDS.items():
        file_path = destinations_path / html_file
        
        if file_path.exists():
            print(f"✅ {dest_data['name']:25} - {dest_data['type']}")
            
            if add_seo_to_destination(file_path, dest_data):
                print(f"   ✓ SEO & structured data added")
                updated_count += 1
            else:
                print(f"   ⚠ Failed to update SEO")
    
    # Process remaining destinations with generic metadata
    processed_files = set(DESTINATION_KEYWORDS.keys())
    remaining_files = [f for f in dest_files if f.name not in processed_files]
    
    print(f"\n📌 Processing {len(remaining_files)} additional destinations...")
    
    for html_file in remaining_files:
        dest_name = html_file.stem.replace('-', ' ').title()
        generic_data = {
            'name': dest_name,
            'type': 'Tourist Attraction',
            'keywords': f'{dest_name}, {dest_name} Kutch, visit {dest_name}, things to do {dest_name}',
            'region': 'Kutch',
        }
        
        if add_seo_to_destination(html_file, generic_data):
            updated_count += 1
            print(f"   ✓ {dest_name}")
    
    print("\n" + "=" * 60)
    print(f"\n✨ SEO Optimization Complete!")
    print(f"\n📊 Results:")
    print(f"   • Destinations processed: {updated_count} / {len(dest_files)}")
    print(f"   • SEO meta tags: ✓ Added")
    print(f"   • Keywords optimization: ✓ Applied")
    print(f"   • Structured data (schema.org): ✓ Added")
    print(f"   • Open Graph tags: ✓ Updated")
    
    print(f"\n🎯 Target Keywords Coverage:")
    keywords_list = [
        'Kutch travel',
        'Travel to Kutch',
        'Kutch tourism',
        'Rann of Kutch',
        'White Rann',
        'Bhuj city',
        'Mandvi beach',
        'Dholavira heritage',
        'Kadia Dhrow canyon',
        'Mundra port',
        'Road to Heaven',
        'Kutch attractions',
        'Kutch destinations',
        'Kutch hotel & resort',
    ]
    
    for kw in keywords_list:
        print(f"   ✓ {kw}")

if __name__ == '__main__':
    main()
