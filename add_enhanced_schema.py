"""
Enhanced Structured Data Script for MyKutch.org
Adds comprehensive Place/TouristAttraction schema to destination pages
"""

import os
import json
import re
from pathlib import Path
from bs4 import BeautifulSoup

# Enhanced structured data for key destinations
DESTINATION_SCHEMAS = {
    'bhuj': {
        "@context": "https://schema.org",
        "@type": "City",
        "name": "Bhuj",
        "description": "Bhuj is the capital city of Kutch district in Gujarat, known for its historic palaces, museums, and vibrant crafts",
        "url": "https://www.mykutch.org/destinations/bhuj.html",
        "geo": {
            "@type": "GeoCoordinates",
            "latitude": "23.2420",
            "longitude": "69.6669"
        },
        "containedInPlace": {
            "@type": "AdministrativeArea",
            "name": "Kutch District, Gujarat, India"
        },
        "touristType": ["Cultural Tourism", "Heritage Tourism", "Shopping"],
        "keywords": "Bhuj, Bhuj city, Kutch capital, Aina Mahal, Prag Mahal, Bhuj tourism"
    },
    
    'mandvi': {
        "@context": "https://schema.org",
        "@type": "Beach",
        "name": "Mandvi Beach",
        "description": "Mandvi is Kutch's premier beach destination featuring Vijay Vilas Palace, pristine beaches, and traditional shipbuilding",
        "url": "https://www.mykutch.org/destinations/mandvi.html",
        "geo": {
            "@type": "GeoCoordinates",
            "latitude": "22.8288",
            "longitude": "69.3578"
        },
        "containedInPlace": {
            "@type": "AdministrativeArea",
            "name": "Kutch District, Gujarat, India"
        },
        "isAccessibleForFree": True,
        "keywords": "Mandvi beach, Mandvi Gujarat, Vijay Vilas Palace, Arabian Sea, beach in Kutch"
    },
    
    'dhordo-white-rann': {
        "@context": "https://schema.org",
        "@type": "TouristAttraction",
        "name": "White Rann of Kutch",
        "alternateName": ["Great Rann of Kutch", "Rann of Kutch", "White Desert"],
        "description": "The White Rann is a vast salt marsh in the Thar Desert, famous for the Rann Utsav festival and stunning white landscape",
        "url": "https://www.mykutch.org/destinations/dhordo-white-rann.html",
        "geo": {
            "@type": "GeoCoordinates",
            "latitude": "23.8333",
            "longitude": "69.6667"
        },
        "containedInPlace": {
            "@type": "AdministrativeArea",
            "name": "Kutch District, Gujarat, India"
        },
        "isAccessibleForFree": True,
        "touristType": ["Nature Tourism", "Cultural Tourism", "Photography"],
        "keywords": "White Rann, Rann of Kutch, Rann Utsav, salt desert, Dhordo, white desert India",
        "event": {
            "@type": "Festival",
            "name": "Rann Utsav",
            "description": "Annual cultural festival showcasing Kutchi culture, crafts, and traditions",
            "startDate": "2026-11-01",
            "endDate": "2027-02-28",
            "location": {
                "@type": "Place",
                "name": "Dhordo, White Rann of Kutch"
            }
        }
    },
    
    'dholavira': {
        "@context": "https://schema.org",
        "@type": "TouristAttraction",
        "name": "Dholavira",
        "description": "Dholavira is a 5,000-year-old Harappan archaeological site and UNESCO World Heritage Site",
        "url": "https://www.mykutch.org/destinations/dholavira.html",
        "geo": {
            "@type": "GeoCoordinates",
            "latitude": "23.8867",
            "longitude": "70.2167"
        },
        "containedInPlace": {
            "@type": "AdministrativeArea",
            "name": "Kutch District, Gujarat, India"
        },
        "touristType": ["Heritage Tourism", "Archaeological Tourism", "Educational Tourism"],
        "keywords": "Dholavira, Harappan site, Indus Valley Civilization, UNESCO World Heritage, archaeological site Kutch"
    },
    
    'kadia-dhrow': {
        "@context": "https://schema.org",
        "@type": "TouristAttraction",
        "name": "Kadia Dhrow",
        "alternateName": "Grand Canyon of India",
        "description": "Kadia Dhrow is a geological wonder featuring colorful layered rock formations, often called the Grand Canyon of India",
        "url": "https://www.mykutch.org/destinations/kadia-dhrow.html",
        "geo": {
            "@type": "GeoCoordinates",
            "latitude": "23.4500",
            "longitude": "69.8500"
        },
        "containedInPlace": {
            "@type": "AdministrativeArea",
            "name": "Kutch District, Gujarat, India"
        },
        "isAccessibleForFree": True,
        "touristType": ["Nature Tourism", "Photography", "Adventure Tourism"],
        "keywords": "Kadia Dhrow, Grand Canyon of India, Kutch canyon, geological wonder"
    }
}

def add_enhanced_schema(soup, page_name):
    """Add enhanced structured data to destination pages"""
    
    # Check if this page needs enhanced schema
    schema_data = None
    for key in DESTINATION_SCHEMAS:
        if key in page_name.lower():
            schema_data = DESTINATION_SCHEMAS[key]
            break
    
    if not schema_data:
        return False
    
    # Check if similar schema already exists
    existing_schemas = soup.find_all('script', attrs={'type': 'application/ld+json'})
    for script in existing_schemas:
        if script.string and schema_data.get('@type', '') in script.string:
            # Schema of this type already exists, skip
            return False
    
    # Add the new schema
    head = soup.find('head')
    if head:
        script = soup.new_tag('script', attrs={'type': 'application/ld+json'})
        script.string = '\n' + json.dumps(schema_data, indent=2, ensure_ascii=False) + '\n'
        head.append(script)
        return True
    
    return False

def process_html_file(file_path):
    """Process a single HTML file to add enhanced structured data"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        page_name = file_path.stem
        
        # Add enhanced schema
        schema_added = add_enhanced_schema(soup, page_name)
        
        if schema_added:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(str(soup))
            return True, f"{file_path.name} (enhanced schema added)"
        
        return True, f"{file_path.name} (no schema needed)"
    
    except Exception as e:
        return False, f"{file_path.name}: {str(e)}"

def main():
    """Main function to process destination HTML files"""
    site_dir = Path('site')
    
    if not site_dir.exists():
        print("Error: 'site' directory not found!")
        return
    
    # Find destination HTML files
    dest_dir = site_dir / 'destinations'
    if dest_dir.exists():
        html_files = list(dest_dir.glob('*.html'))
    else:
        html_files = []
    
    print(f"Found {len(html_files)} destination files to process...")
    print("-" * 60)
    
    success_count = 0
    error_count = 0
    schema_added_count = 0
    
    for html_file in html_files:
        success, message = process_html_file(html_file)
        
        if success:
            success_count += 1
            if 'schema added' in message:
                schema_added_count += 1
            print(f"✓ {message}")
        else:
            error_count += 1
            print(f"✗ {message}")
    
    print("-" * 60)
    print(f"\nProcessing complete!")
    print(f"Success: {success_count} files")
    print(f"Enhanced schemas added: {schema_added_count}")
    print(f"Errors: {error_count} files")

if __name__ == '__main__':
    main()
