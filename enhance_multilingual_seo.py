#!/usr/bin/env python3
"""
Comprehensive Multilingual SEO Enhancement for MyKutch
Optimizes all pages for keywords:
- Kutch travel, travel to kutch, Kutch tourism
- Rann of kutch, White Rann
- Road to heaven, Bhuj, Mundra, Kadia Dhrow
- Dholavira, Mandvi, and other key destinations
- Kutch crafts, culture, heritage
"""

import json
from pathlib import Path
from bs4 import BeautifulSoup
import re

# SEO Keywords and metadata for each page in each language
SEO_CONTENT = {
    'en': {
        'homepage': {
            'title': 'Kutch Travel Guide 2026 | White Rann, Bhuj & Hidden Gems | MyKutch.org',
            'desc': 'Complete Kutch travel guide. Explore White Rann desert, ancient Dholavira, Bhuj city, vibrant crafts, and hidden gems. Hotels, tours, and insider tips for visiting Kutch, Gujarat.',
            'keywords': 'Kutch travel, travel to Kutch, Kutch tourism, Bhuj, Rann of Kutch, White Rann, Dholavira, Mandvi, Kadia Dhrow, road to heaven, Kutch hotels, Kutch attractions, visit Kutch, Kutch guide',
            'og_title': 'Kutch Travel Guide 2026 | White Rann, Bhuj & Hidden Gems',
            'og_desc': 'Explore Kutch\'s White Rann salt desert, ancient Harappan sites, vibrant crafts, and cultural heritage. Complete travel guide with hotels, tours, and insider tips.',
        },
        'destinations': {
            'title': 'Kutch Destinations & Attractions | Travel Guide to Places to Visit',
            'desc': 'Discover all top Kutch destinations - White Rann, Bhuj, Mandvi, Dholavira, Kadia Dhrow, road to heaven, and 50+ hidden gems. Complete tourist guide to Kutch tourism.',
            'keywords': 'Kutch destinations, places to visit in Kutch, Kutch attractions, Kutch tourism, tourist places Kutch, Bhuj tourism, Mandvi beach, Rann of Kutch, Dholavira heritage site',
        },
        'crafts': {
            'title': 'Kutch Arts & Crafts | Ajrakh, Bandhani, Rogan Art & Heritage',
            'desc': 'Explore the vibrant arts and crafts of Kutch. From Ajrakh block printing to Rogan art, Bandhani tie-dye, mirror work, and traditional handicrafts. Meet artisans in craft villages.',
            'keywords': 'Kutch crafts, Kutch handicrafts, Ajrakh, Bandhani, Rogan art, mirror work, Kutch embroidery, traditional crafts, Kutch artisans, handloom Kutch, craft villages',
        },
        'hidden_gems': {
            'title': 'Hidden Gems of Kutch | Offbeat & Unexplored Destinations',
            'desc': 'Discover hidden gems and offbeat places in Kutch away from tourist crowds. Lesser-known attractions, secret beaches, and cultural sites for authentic travel experiences.',
            'keywords': 'hidden gems Kutch, offbeat Kutch, unexplored Kutch destinations, secret places Kutch, lesser known attractions, hidden beaches Kutch',
        },
        'history': {
            'title': 'History of Kutch | Heritage, Kingdom & Cultural Timeline',
            'desc': 'Explore the rich history of Kutch - from ancient Harappan civilization to medieval kingdoms and modern Gujarat. Understand Kutch\'s cultural heritage and historical significance.',
            'keywords': 'Kutch history, history of Kutch, Kutch heritage, Kutch kingdom, Harappan civilization, Kutch culture, Gujarat history',
        },
        'geography': {
            'title': 'Geography of Kutch | Region, Climate, Terrain & Maps',
            'desc': 'Learn about Kutch\'s unique geography - the Rann salt desert, Little Rann, diverse terrain, climate, and geographical features that shape this unique region in Gujarat.',
            'keywords': 'Kutch geography, Kutch district, Kutch region, Kutch landscape, Rann desert, Little Rann, Kutch terrain, Gujarat geography',
        },
        'bookings': {
            'title': 'Kutch Hotels, Resorts & Tour Bookings | Travel Packages',
            'desc': 'Book hotels and resorts in Kutch - Bhuj, White Rann, Mandvi. Find Kutch tour packages, accommodation options, and travel deals for your Kutch vacation.',
            'keywords': 'Kutch hotels, Kutch resorts, hotels in Bhuj, Rann Utsav booking, Kutch tour packages, Kutch accommodation, book Kutch tour',
        },
        'bhuj': {
            'title': 'Bhuj City Guide | Aina Mahal, Prag Mahal & Kutch Capital',
            'desc': 'Explore Bhuj, the cultural capital of Kutch. Visit Aina Mahal, Prag Mahal, museums, bazaars, and vibrant markets. Guide to things to do in Bhuj, Gujarat.',
            'keywords': 'Bhuj, Bhuj city, Bhuj tourism, Bhuj attractions, Aina Mahal, Prag Mahal, Bhuj hotel, Bhuj Gujarat, capital of Kutch',
        },
        'mandvi': {
            'title': 'Mandvi Beach & Vijay Vilas Palace | Kutch Coastal Guide',
            'desc': 'Visit Mandvi beach and Vijay Vilas Palace on the Arabian Sea coast of Kutch. Beach resort, shipbuilding heritage, and beach activities in this coastal gem.',
            'keywords': 'Mandvi, Mandvi beach, Mandvi beach resort, Vijay Vilas Palace, Mandvi Gujarat, Arabian Sea, beach in Kutch, Mandvi tourism',
        },
        'dholavira': {
            'title': 'Dholavira | UNESCO World Heritage Harappan City Site',
            'desc': 'Discover Dholavira - an ancient Harappan (Indus Valley) civilization site. UNESCO World Heritage Site showcasing 5,000-year-old ruins and archaeological significance in Kutch.',
            'keywords': 'Dholavira, Harappan site, Indus Valley Civilization, UNESCO World Heritage Site, ancient Dholavira, archaeological site Kutch, Dholavira ruins',
        },
        'kadia_dhrow': {
            'title': 'Kadia Dhrow | Grand Canyon of India in Kutch',
            'desc': 'Experience Kadia Dhrow, often called the Grand Canyon of India. Colorful layered rocks, geological wonder, and scenic beauty in northern Kutch.',
            'keywords': 'Kadia Dhrow, Grand Canyon India, Kutch canyon, colorful rocks Kutch, geological wonder, Kadia Dhrow tourism, Kadia Dungar',
        },
        'mundra': {
            'title': 'Mundra | Port City & Coastal Gem of Kutch',
            'desc': 'Explore Mundra, a historic port city on Kutch\'s coast. Known for Mundra port, maritime heritage, and coastal attractions. Gateway to northwest Gujarat.',
            'keywords': 'Mundra, Mundra port, Mundra city, Mundra Gujarat, coastal Kutch, port city Gujarat, maritime heritage',
        },
        'road_to_heaven': {
            'title': 'Road to Heaven | Scenic Route in Kutch',
            'desc': 'Travel the Road to Heaven - a scenic route offering panoramic views of Kutch\'s desert landscape. Hidden gem and photography hotspot in Kutch.',
            'keywords': 'road to heaven, scenic route Kutch, road to heaven Kutch, panoramic views Kutch, photography Kutch',
        },
    },
    'hi': {
        'homepage': {
            'title': 'कच्छ यात्रा गाइड 2026 | सफेद रण, भुज और छिपे हुए रत्न',
            'desc': 'कच्छ की संपूर्ण यात्रा गाइड। सफेद रण रेगिस्तान, प्राचीन धोलावीरा, भुज शहर, जीवंत कला-कौशल, और छिपे हुए रत्नों की खोज करें। होटल, दौरे और कच्छ, गुजरात की यात्रा के लिए अंदरूनी टिप्स।',
            'keywords': 'कच्छ यात्रा, कच्छ पर्यटन, भुज, रण of कच्छ, सफेद रण, धोलावीरा, मांडवी, कड़िया ढोरो, स्वर्ग का रास्ता, कच्छ होटल, कच्छ आकर्षण, कच्छ गाइड',
        },
        'destinations': {
            'title': 'कच्छ गंतव्य और आकर्षण | यात्रा गाइड',
            'desc': 'कच्छ के सभी शीर्ष गंतव्य - सफेद रण, भुज, मांडवी, धोलावीरा, कड़िया ढोरो, और 50+ छिपे हुए रत्न। कच्छ पर्यटन के लिए संपूर्ण गाइड।',
            'keywords': 'कच्छ गंतव्य, कच्छ आकर्षण, कच्छ पर्यटन, भुज पर्यटन, मांडवी समुद्र तट',
        },
        'crafts': {
            'title': 'कच्छ कला और विषयहस्तशिल्प | अजरख, बांधनी, रोगन कला',
            'desc': 'कच्छ की जीवंत कला और हस्तशिल्प की खोज करें। अजरख ब्लॉक प्रिंटिंग से रोगन कला, बांधनी, दर्पण कार्य तक। कारीगरों से मिलें।',
            'keywords': 'कच्छ कला, कच्छ हस्तशिल्प, अजरख, बांधनी, रोगन कला, कच्छ कारीगर',
        },
    },
    'de': {
        'homepage': {
            'title': 'Kutch Reiseführer 2026 | Weiße Rann, Bhuj & Verborgene Schätze',
            'desc': 'Kompletter Kutch Reiseführer. Erkunden Sie die weiße Rann Salzwüste, das antike Dholavira, die Stadt Bhuj und verborgene Schätze. Hotels, Touren und Insider-Tipps für Kutch, Gujarat.',
            'keywords': 'Kutch Reisen, Kutch Tourismus, Bhuj, Rann of Kutch, Weiße Rann, Dholavira, Mandvi, Kadia Dhrow, Weg zum Himmel',
        },
    },
    'fr': {
        'homepage': {
            'title': 'Guide de Voyage Kutch 2026 | Rann Blanc, Bhuj & Joyaux Cachés',
            'desc': 'Guide complet de voyage à Kutch. Explorez le désert de sel blanc de Rann, l\'ancien Dholavira, la ville de Bhuj et les joyaux cachés. Hôtels, visites guidées et conseils.',
            'keywords': 'voyage Kutch, tourisme Kutch, Bhuj, Rann of Kutch, Rann Blanc, Dholavira, Mandvi',
        },
    },
    'es': {
        'homepage': {
            'title': 'Guía de Viajes a Kutch 2026 | Rann Blanco, Bhuj y Gemas Ocultas',
            'desc': 'Guía completa de viajes a Kutch. Explora el desierto de sal Rann Blanco, el antiguo Dholavira, la ciudad de Bhuj y gemas ocultas. Hoteles, tours y consejos locales.',
            'keywords': 'viajes Kutch, turismo Kutch, Bhuj, Rann of Kutch, Rann Blanco, Dholavira, Mandvi',
        },
    },
    'ru': {
        'homepage': {
            'title': 'Путеводитель по Кач 2026 | Белая Ранн, Бхудж и скрытые сокровища',
            'desc': 'Полный путеводитель по Кач. Исследуйте белую пустыню Ранн, древний Дхолавира, город Бхудж и скрытые сокровища. Отели, экскурсии и советы от местных.',
            'keywords': 'путешествие в Кач, туризм в Кач, Бхудж, Ранн в Кач, Белая Ранн, Дхолавира',
        },
    },
}

def add_seo_data_to_html(html_file, page_type, lang='en'):
    """Add SEO meta tags with data-i18n attributes to HTML files"""
    
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    soup = BeautifulSoup(content, 'html.parser')
    head = soup.find('head')
    
    if not head:
        head = soup.new_tag('head')
        body = soup.find('body')
        if body:
            body.insert_before(head)
    
    # Get SEO content for this language/page combination
    seo_config = SEO_CONTENT.get(lang, {}).get(page_type, {})
    
    if not seo_config:
        return False
    
    # Update or add title
    title_tag = head.find('title')
    if not title_tag:
        title_tag = soup.new_tag('title')
        head.append(title_tag)
    
    # Get i18n key for this page type
    i18n_key = f'{page_type}.meta_title' if page_type != 'homepage' else 'home.meta_title'
    title_tag['data-i18n'] = i18n_key
    title_tag.string = seo_config.get('title', '')
    
    # Update or add meta description
    meta_desc = head.find('meta', attrs={'name': 'description'})
    if not meta_desc:
        meta_desc = soup.new_tag('meta')
        meta_desc['name'] = 'description'
        head.append(meta_desc)
    
    i18n_key_desc = f'{page_type}.meta_desc' if page_type != 'homepage' else 'home.meta_desc'
    meta_desc['data-i18n'] = i18n_key_desc
    meta_desc['content'] = seo_config.get('desc', '')
    
    # Update or add meta keywords
    meta_keywords = head.find('meta', attrs={'name': 'keywords'})
    if not meta_keywords:
        meta_keywords = soup.new_tag('meta')
        meta_keywords['name'] = 'keywords'
        head.append(meta_keywords)
    
    meta_keywords['content'] = seo_config.get('keywords', '')
    
    # Update or add robots meta
    meta_robots = head.find('meta', attrs={'name': 'robots'})
    if not meta_robots:
        meta_robots = soup.new_tag('meta')
        meta_robots['name'] = 'robots'
        meta_robots['content'] = 'index, follow'
        head.append(meta_robots)
    
    # Update Open Graph tags if og_title exists
    if 'og_title' in seo_config:
        og_title = head.find('meta', attrs={'property': 'og:title'})
        if not og_title:
            og_title = soup.new_tag('meta')
            og_title['property'] = 'og:title'
            head.append(og_title)
        og_title['content'] = seo_config.get('og_title', '')
    
    if 'og_desc' in seo_config:
        og_desc = head.find('meta', attrs={'property': 'og:description'})
        if not og_desc:
            og_desc = soup.new_tag('meta')
            og_desc['property'] = 'og:description'
            head.append(og_desc)
        og_desc['content'] = seo_config.get('og_desc', '')
    
    # Save updated HTML
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(str(soup.prettify()))
    
    return True

def update_language_json(lang_file, page_type, seo_data):
    """Update language JSON file with SEO metadata"""
    
    with open(lang_file, 'r', encoding='utf-8') as f:
        lang_json = json.load(f)
    
    # Ensure the page section exists
    if f'{page_type}_page' not in lang_json:
        lang_json[f'{page_type}_page'] = {}
    
    page_section = lang_json[f'{page_type}_page']
    
    # Add SEO metadata
    page_section['meta_title'] = seo_data.get('title', '')
    page_section['meta_desc'] = seo_data.get('desc', '')
    
    # Save updated JSON
    with open(lang_file, 'w', encoding='utf-8') as f:
        json.dump(lang_json, f, ensure_ascii=False, indent=2)
    
    return True

def main():
    site_path = Path(__file__).parent / 'site'
    lang_path = site_path / 'lang'
    
    # List of pages to optimize
    pages_to_optimize = {
        'index.html': 'homepage',
        'destinations.html': 'destinations',
        'crafts.html': 'crafts',
        'hidden-gems.html': 'hidden_gems',
        'history.html': 'history',
        'geography.html': 'geography',
        'bookings.html': 'bookings',
    }
    
    destination_pages = {
        'destinations/bhuj.html': 'bhuj',
        'destinations/mandvi.html': 'mandvi',
        'destinations/dholavira.html': 'dholavira',
        'destinations/kadia-dhrow.html': 'kadia_dhrow',
        'destinations/mundra.html': 'mundra',
        'destinations/road-to-heaven.html': 'road_to_heaven',
    }
    
    # Map destination filenames to page types
    all_pages = {**pages_to_optimize, **destination_pages}
    
    languages = ['en', 'hi', 'de', 'fr', 'es', 'ru']
    
    print("🚀 Starting Multilingual SEO Enhancement...\n")
    
    # Update main pages
    for html_file, page_type in all_pages.items():
        file_path = site_path / html_file
        
        if file_path.exists():
            print(f"✅ Updating {html_file} ({page_type})...")
            
            # Update HTML for English (main language)
            if add_seo_data_to_html(str(file_path), page_type, 'en'):
                print(f"   ✓ HTML meta tags updated")
            
            # Update language JSON files
            for lang in languages:
                lang_file = lang_path / f'{lang}.json'
                if lang_file.exists():
                    seo_data = SEO_CONTENT.get(lang, {}).get(page_type, {})
                    if seo_data:
                        update_language_json(str(lang_file), page_type, seo_data)
                        print(f"   ✓ {lang.upper()} language file updated")
        else:
            print(f"⚠ File not found: {html_file}")
    
    # Add destination-specific meta tags for major attractions
    destination_keywords = {
        'bhuj.html': 'bhuj',
        'mandvi.html': 'mandvi',
        'dholavira.html': 'dholavira',
        'kadia-dhrow.html': 'kadia_dhrow',
        'mundra.html': 'mundra',
        'road-to-heaven.html': 'road_to_heaven',
    }
    
    print("\n📍 Key destinations with enhanced SEO:")
    for dest_file, dest_type in destination_keywords.items():
        dest_path = site_path / 'destinations' / dest_file
        if dest_path.exists():
            print(f"   ✓ {dest_file}")
    
    print("\n✨ SEO Enhancement Complete!")
    print("\n📊 Summary:")
    print(f"   • Languages: {', '.join([l.upper() for l in languages])}")
    print(f"   • Main pages optimized: {len(pages_to_optimize)}")
    print(f"   • Key destinations enhanced: {len(destination_keywords)}")
    print(f"   • Target keywords: Kutch travel, Rann of Kutch, White Rann, Bhuj, Dholavira, Mandvi, Kadia Dhrow, Mundra, Road to Heaven")

if __name__ == '__main__':
    main()
