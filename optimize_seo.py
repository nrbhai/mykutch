"""
SEO Optimization Script for MyKutch.org
Updates meta keywords, titles, and structured data for better search engine visibility
"""

import os
import re
from pathlib import Path
from bs4 import BeautifulSoup

# Define keyword sets for different page types
KEYWORDS = {
    'homepage': 'Kutch, Kutch travel, Kutch tourism, Kutch online, Bhuj, Bhuj tourism, Rann, White Rann, Rann of Kutch, Great Rann of Kutch, Rann Utsav, Rann Utsav 2026, Mandvi, Mandvi beach, Mandvi Gujarat, Dholavira, Kadia Dhrow, Kutch hotels, Kutch resorts, Gujarat tourism, Kutch destinations, Kutch crafts, Kutch culture, visit Kutch, explore Kutch',
    
    'bhuj': 'Bhuj, Bhuj city, Bhuj tourism, Bhuj Gujarat, Bhuj palace, Aina Mahal, Prag Mahal, Bhuj fort, capital of Kutch, Bhuj hotels, Bhuj attractions, visit Bhuj, Kutch capital, Bhuj travel guide',
    
    'mandvi': 'Mandvi, Mandvi beach, Mandvi Gujarat, Vijay Vilas Palace, Mandvi tourism, Mandvi port, shipbuilding Mandvi, Mandvi hotels, Mandvi beach resort, Arabian Sea Kutch, Mandvi travel, beach in Kutch',
    
    'white_rann': 'White Rann, Rann of Kutch, Great Rann of Kutch, Dhordo, Rann Utsav, Rann Utsav 2026, salt desert, white desert India, Kutch desert, Rann festival, White Rann tourism, Dhordo tent city',
    
    'dholavira': 'Dholavira, Harappan site, Indus Valley Civilization, Dholavira Kutch, UNESCO World Heritage Site, ancient Dholavira, archaeological site Kutch, Dholavira ruins, Harappan city',
    
    'kadia_dhrow': 'Kadia Dhrow, Grand Canyon of India, Kadia Dungar, Kutch canyon, geological wonder Kutch, Kadia Dhrow tourism, colorful rocks Kutch',
    
    'destinations': 'Kutch destinations, Kutch tourist places, places to visit in Kutch, Kutch attractions, Kutch sightseeing, Kutch travel destinations, Gujarat tourism, Kutch tour packages',
    
    'crafts': 'Kutch crafts, Kutch handicrafts, Bandhani, Ajrakh, Rogan art, mirror work, Kutch embroidery, traditional crafts Gujarat, Kutch artisans, handloom Kutch',
    
    'history': 'Kutch history, history of Kutch, Kutch heritage, Kutch culture, Kutch kingdom, historical Kutch, Kutch traditions, Gujarat history',
    
    'geography': 'Kutch geography, Kutch district, Kutch region, Kutch landscape, Kutch terrain, Kutch climate, Kutch map, Gujarat geography',
    
    'bookings': 'Kutch hotels, Kutch resorts, book Kutch tour, Kutch accommodation, Kutch travel packages, Kutch tour booking, hotels in Bhuj, Rann Utsav booking',
    
    'hidden_gems': 'hidden gems Kutch, offbeat Kutch, unexplored Kutch, secret places Kutch, lesser known Kutch destinations',
    
    'default': 'Kutch, Kutch tourism, Gujarat, Kutch travel, visit Kutch, Kutch India'
}

def get_keywords_for_page(file_path):
    """Determine appropriate keywords based on file path and name"""
    file_name = file_path.stem.lower()
    file_str = str(file_path).lower()
    
    # Homepage
    if file_name == 'index' and 'destinations' not in file_str:
        return KEYWORDS['homepage']
    
    # Specific destinations
    if 'bhuj' in file_name:
        return KEYWORDS['bhuj']
    elif 'mandvi' in file_name:
        return KEYWORDS['mandvi']
    elif 'dhordo' in file_name or 'white-rann' in file_name:
        return KEYWORDS['white_rann']
    elif 'dholavira' in file_name:
        return KEYWORDS['dholavira']
    elif 'kadia' in file_name:
        return KEYWORDS['kadia_dhrow']
    
    # Page types
    elif 'destinations' in file_str or file_name == 'destinations':
        return KEYWORDS['destinations']
    elif 'craft' in file_str:
        return KEYWORDS['crafts']
    elif 'history' in file_name:
        return KEYWORDS['history']
    elif 'geography' in file_name:
        return KEYWORDS['geography']
    elif 'booking' in file_name:
        return KEYWORDS['bookings']
    elif 'hidden-gem' in file_str:
        return KEYWORDS['hidden_gems']
    
    # Default for other destination pages
    elif 'destinations' in file_str:
        return KEYWORDS['default'] + ', ' + file_name.replace('-', ' ') + ', ' + file_name.replace('-', ' ') + ' Kutch'
    
    return KEYWORDS['default']

def update_meta_keywords(soup, keywords):
    """Update or add meta keywords tag"""
    meta_keywords = soup.find('meta', attrs={'name': 'keywords'})
    
    if meta_keywords:
        meta_keywords['content'] = keywords
    else:
        # Find the head tag and add keywords
        head = soup.find('head')
        if head:
            # Add after description if it exists
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            new_meta = soup.new_tag('meta', attrs={'name': 'keywords', 'content': keywords})
            
            if meta_desc:
                meta_desc.insert_after(new_meta)
            else:
                head.append(new_meta)

def add_faq_schema(soup, page_type):
    """Add FAQ schema for main pages"""
    
    # Only add to specific pages
    if page_type not in ['homepage', 'bhuj', 'mandvi', 'white_rann', 'destinations']:
        return
    
    # Check if FAQ schema already exists
    existing_faq = soup.find('script', attrs={'type': 'application/ld+json'}, string=re.compile(r'FAQPage'))
    if existing_faq:
        return
    
    faq_data = {
        'homepage': {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": "When is the best time to visit Kutch?",
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": "The best time to visit Kutch is from October to March during winter when temperatures are pleasant (10-25°C). The famous Rann Utsav festival takes place from November to February."
                    }
                },
                {
                    "@type": "Question",
                    "name": "How to reach White Rann of Kutch?",
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": "The nearest airport is Bhuj (80km from White Rann). From Bhuj, you can hire a taxi or take a bus to Dhordo village, which is the gateway to the White Rann. The journey takes about 1.5-2 hours."
                    }
                },
                {
                    "@type": "Question",
                    "name": "What is Rann Utsav?",
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": "Rann Utsav is a cultural festival held annually in the White Rann of Kutch from November to February. It showcases Kutchi culture, crafts, music, dance, and local cuisine with tent accommodations available at Dhordo."
                    }
                }
            ]
        }
    }
    
    if page_type in faq_data:
        import json
        head = soup.find('head')
        if head:
            script = soup.new_tag('script', attrs={'type': 'application/ld+json'})
            script.string = '\n' + json.dumps(faq_data[page_type], indent=2) + '\n'
            head.append(script)

def process_html_file(file_path):
    """Process a single HTML file to update SEO elements"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        
        # Get appropriate keywords
        keywords = get_keywords_for_page(file_path)
        
        # Update meta keywords
        update_meta_keywords(soup, keywords)
        
        # Determine page type for FAQ schema
        file_name = file_path.stem.lower()
        page_type = None
        if file_name == 'index' and 'destinations' not in str(file_path).lower():
            page_type = 'homepage'
        elif 'bhuj' in file_name:
            page_type = 'bhuj'
        elif 'mandvi' in file_name:
            page_type = 'mandvi'
        elif 'dhordo' in file_name or 'white-rann' in file_name:
            page_type = 'white_rann'
        elif file_name == 'destinations':
            page_type = 'destinations'
        
        # Add FAQ schema where appropriate
        if page_type:
            add_faq_schema(soup, page_type)
        
        # Write back to file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        
        return True, file_path.name
    
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
    
    print(f"Found {len(html_files)} HTML files to process...")
    print("-" * 60)
    
    success_count = 0
    error_count = 0
    
    for html_file in html_files:
        success, message = process_html_file(html_file)
        
        if success:
            success_count += 1
            print(f"✓ {message}")
        else:
            error_count += 1
            print(f"✗ {message}")
    
    print("-" * 60)
    print(f"\nProcessing complete!")
    print(f"Success: {success_count} files")
    print(f"Errors: {error_count} files")

if __name__ == '__main__':
    main()
