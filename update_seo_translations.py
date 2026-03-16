#!/usr/bin/env python3
"""
Comprehensive Multilingual SEO Content for all pages and destinations
Translates and optimizes SEO metadata for all 6 languages
"""

import json
from pathlib import Path

# Comprehensive SEO translations for all languages
SEO_TRANSLATIONS = {
    'en': {
        'home': {
            'meta_title': 'Kutch Travel Guide 2026 | White Rann, Bhuj & Hidden Gems | MyKutch.org',
            'meta_desc': 'Complete Kutch travel guide. Explore White Rann desert, ancient Dholavira, Bhuj city, vibrant crafts, and hidden gems. Hotels, tours, and insider tips for visiting Kutch, Gujarat.',
            'meta_keywords': 'Kutch travel, travel to Kutch, Kutch tourism, Bhuj, Rann of Kutch, White Rann, Dholavira, Mandvi, Kadia Dhrow, road to heaven, Kutch hotels, Kutch attractions, visit Kutch',
        },
        'destinations_page': {
            'meta_title': 'Kutch Destinations & Attractions | Travel Guide to Places to Visit',
            'meta_desc': 'Discover all top Kutch destinations - White Rann, Bhuj, Mandvi, Dholavira, Kadia Dhrow, road to heaven, and 50+ hidden gems. Complete tourist guide to Kutch tourism.',
            'meta_keywords': 'Kutch destinations, places to visit in Kutch, Kutch attractions, Kutch tourism, Bhuj, Mandvi, Dholavira, Rann of Kutch',
        },
        'crafts_page': {
            'meta_title': 'Kutch Arts & Crafts | Ajrakh, Bandhani, Rogan Art & Heritage',
            'meta_desc': 'Explore the vibrant arts and crafts of Kutch. From Ajrakh block printing to Rogan art, Bandhani tie-dye, mirror work. Meet artisans in craft villages.',
            'meta_keywords': 'Kutch crafts, Kutch handicrafts, Ajrakh, Bandhani, Rogan art, mirror work, Kutch artisans, traditional crafts, handloom Kutch',
        },
        'hidden_gems_page': {
            'meta_title': 'Hidden Gems of Kutch | Offbeat & Unexplored Destinations',
            'meta_desc': 'Discover hidden gems and offbeat places in Kutch away from tourist crowds. Lesser-known attractions, secret beaches, and cultural sites.',
            'meta_keywords': 'hidden gems Kutch, offbeat Kutch, unexplored Kutch, secret places Kutch, lesser known attractions',
        },
        'history_page': {
            'meta_title': 'History of Kutch | Heritage, Kingdom & Cultural Timeline',
            'meta_desc': 'Explore the rich history of Kutch - from ancient Harappan civilization to medieval kingdoms. Understand Kutch\'s cultural heritage and historical significance.',
            'meta_keywords': 'Kutch history, Kutch heritage, Harappan civilization, Kutch kingdom, Kutch culture, Gujarat history',
        },
        'geography_page': {
            'meta_title': 'Geography of Kutch | Region, Climate, Terrain & Maps',
            'meta_desc': 'Learn about Kutch\'s unique geography - the Rann salt desert, Little Rann, diverse terrain, and geographical features that shape this unique region in Gujarat.',
            'meta_keywords': 'Kutch geography, Kutch district, Rann desert, Little Rann, Kutch landscape, Kutch terrain, Gujarat geography',
        },
        'bookings_page': {
            'meta_title': 'Kutch Hotels, Resorts & Tour Bookings | Travel Packages',
            'meta_desc': 'Book hotels and resorts in Kutch - Bhuj, White Rann, Mandvi. Find Kutch tour packages, accommodation options, and travel deals.',
            'meta_keywords': 'Kutch hotels, Kutch resorts, hotels in Bhuj, Kutch accommodation, Kutch tour packages, book Kutch tour',
        },
    },
    'hi': {
        'home': {
            'meta_title': 'कच्छ यात्रा गाइड 2026 | सफेद रण, भुज और छिपे हुए रत्न',
            'meta_desc': 'कच्छ की संपूर्ण यात्रा गाइड। सफेद रण रेगिस्तान, प्राचीन धोलावीरा, भुज शहर, जीवंत कला-कौशल खोजें। होटल, दौरे, और कच्छ की यात्रा के लिए टिप्स।',
            'meta_keywords': 'कच्छ यात्रा, कच्छ पर्यटन, भुज, रण of कच्छ, सफेद रण, धोलावीरा, मांडवी, कड़िया ढोरो, स्वर्ग का रास्ता',
        },
        'destinations_page': {
            'meta_title': 'कच्छ गंतव्य और आकर्षण | यात्रा गाइड',
            'meta_desc': 'कच्छ के सभी शीर्ष गंतव्य - सफेद रण, भुज, मांडवी, धोलावीरा, कड़िया ढोरो, और 50+ छिपे हुए रत्न खोजें।',
            'meta_keywords': 'कच्छ गंतव्य, कच्छ आकर्षण, कच्छ पर्यटन, भुज पर्यटन, मांडवी समुद्र तट, धोलावीरा',
        },
        'crafts_page': {
            'meta_title': 'कच्छ कला और हस्तशिल्प | अजरख, बांधनी, रोगन कला',
            'meta_desc': 'कच्छ की जीवंत कला और हस्तशिल्प खोजें। अजरख ब्लॉक प्रिंटिंग से रोगन कला, बांधनी, दर्पण कार्य तक। कारीगरों से मिलें।',
            'meta_keywords': 'कच्छ कला, कच्छ हस्तशिल्प, अजरख, बांधनी, रोगन कला, कच्छ कारीगर, पारंपरिक कला',
        },
        'hidden_gems_page': {
            'meta_title': 'कच्छ के छिपे हुए रत्न | अलग और अछूते गंतव्य',
            'meta_desc': 'कच्छ के छिपे हुए रत्न और पर्यटकों की भीड़ से दूर अलग जगहें खोजें। कम ज्ञात आकर्षण और सांस्कृतिक स्थल।',
            'meta_keywords': 'कच्छ छिपे हुए रत्न, अलग कच्छ, अछूता कच्छ, गुप्त स्थान कच्छ',
        },
        'history_page': {
            'meta_title': 'कच्छ का इतिहास | विरासत और सांस्कृतिक काल',
            'meta_desc': 'कच्छ के समृद्ध इतिहास की खोज करें - प्राचीन हड़प्पा सभ्यता से मध्यकालीन राज्यों तक। कच्छ की सांस्कृतिक विरासत को समझें।',
            'meta_keywords': 'कच्छ इतिहास, कच्छ विरासत, हड़प्पा सभ्यता, कच्छ राज्य, कच्छ संस्कृति',
        },
        'geography_page': {
            'meta_title': 'कच्छ का भूगोल | क्षेत्र, जलवायु और भू-दृश्य',
            'meta_desc': 'कच्छ के अद्वितीय भूगोल के बारे में जानें - रण नमक रेगिस्तान, छोटा रण, विविध भू-दृश्य जो इस क्षेत्र को आकार देते हैं।',
            'meta_keywords': 'कच्छ भूगोल, कच्छ जिला, रण रेगिस्तान, छोटा रण, कच्छ परिदृश्य, गुजरात भूगोल',
        },
        'bookings_page': {
            'meta_title': 'कच्छ होटल, रिसॉर्ट्स और टूर बुकिंग | यात्रा पैकेज',
            'meta_desc': 'कच्छ में होटल और रिसॉर्ट्स बुक करें - भुज, सफेद रण, मांडवी। कच्छ टूर पैकेज और आवास विकल्प खोजें।',
            'meta_keywords': 'कच्छ होटल, कच्छ रिसॉर्ट्स, भुज होटल, कच्छ आवास, कच्छ यात्रा पैकेज',
        },
    },
    'de': {
        'home': {
            'meta_title': 'Kutch Reiseführer 2026 | Weiße Rann, Bhuj & verborgene Schätze',
            'meta_desc': 'Kompletter Kutch Reiseführer. Erkunden Sie die weiße Rann Salzwüste, das antike Dholavira, die Stadt Bhuj und verborgene Schätze. Hotels, Touren und Insider-Tipps für Kutch.',
            'meta_keywords': 'Kutch Reisen, Kutch Tourismus, Bhuj, Rann von Kutch, Weiße Rann, Dholavira, Mandvi, Kadia Dhrow, Weg zum Himmel',
        },
        'destinations_page': {
            'meta_title': 'Kutch Destinationen & Attraktionen | Reiseführer',
            'meta_desc': 'Entdecken Sie alle Top-Destinationen in Kutch - Weiße Rann, Bhuj, Mandvi, Dholavira, Kadia Dhrow und 50+ verborgene Schätze.',
            'meta_keywords': 'Kutch Destinationen, Kutch Attraktionen, Kutch Tourismus, Bhuj, Mandvi, Dholavira',
        },
    },
    'fr': {
        'home': {
            'meta_title': 'Guide de Voyage Kutch 2026 | Rann Blanc, Bhuj & joyaux cachés',
            'meta_desc': 'Guide complet de voyage à Kutch. Explorez le désert de sel Rann Blanc, l\'ancien Dholavira, la ville de Bhuj et les joyaux cachés. Hôtels, visites guidées et conseils.',
            'meta_keywords': 'voyage Kutch, tourisme Kutch, Bhuj, Rann de Kutch, Rann Blanc, Dholavira, Mandvi',
        },
        'destinations_page': {
            'meta_title': 'Destinations et attractions de Kutch | Guide de voyage',
            'meta_desc': 'Découvrez les meilleures destinations de Kutch - Rann Blanc, Bhuj, Mandvi, Dholavira, Kadia Dhrow et 50+ joyaux cachés.',
            'meta_keywords': 'destinations Kutch, attractions Kutch, tourisme Kutch, Bhuj, Mandvi, Dholavira',
        },
    },
    'es': {
        'home': {
            'meta_title': 'Guía de Viajes a Kutch 2026 | Rann Blanco, Bhuj y gemas ocultas',
            'meta_desc': 'Guía completa de viajes a Kutch. Explora el desierto de sal Rann Blanco, el antiguo Dholavira, la ciudad de Bhuj y gemas ocultas. Hoteles, tours y consejos.',
            'meta_keywords': 'viajes Kutch, turismo Kutch, Bhuj, Rann de Kutch, Rann Blanco, Dholavira, Mandvi',
        },
        'destinations_page': {
            'meta_title': 'Destinos y atracciones de Kutch | Guía de viajes',
            'meta_desc': 'Descubre los mejores destinos de Kutch - Rann Blanco, Bhuj, Mandvi, Dholavira, Kadia Dhrow y 50+ gemas ocultas.',
            'meta_keywords': 'destinos Kutch, atracciones Kutch, turismo Kutch, Bhuj, Mandvi, Dholavira',
        },
    },
    'ru': {
        'home': {
            'meta_title': 'Путеводитель по Кач 2026 | Белая Ранн, Бхудж и скрытые сокровища',
            'meta_desc': 'Полный путеводитель по Кач. Исследуйте белую пустыню Ранн, древний Дхолавира, город Бхудж и скрытые сокровища. Отели, экскурсии и советы.',
            'meta_keywords': 'путешествие в Кач, туризм в Кач, Бхудж, Ранн в Кач, Белая Ранн, Дхолавира, Мандви',
        },
        'destinations_page': {
            'meta_title': 'Направления и достопримечательности Кач | Путеводитель',
            'meta_desc': 'Откройте лучшие направления Кач - Белую Ранн, Бхудж, Мандви, Дхолавира, Кадия Дхроу и 50+ скрытых сокровищ.',
            'meta_keywords': 'направления Кач, достопримечательности Кач, туризм Кач, Бхудж, Мандви, Дхолавира',
        },
    },
}

def update_language_files():
    """Update all language JSON files with comprehensive SEO content"""
    
    site_path = Path(__file__).parent / 'site'
    lang_path = site_path / 'lang'
    
    print("🌐 Updating Language JSON Files with SEO Content\n")
    print("=" * 60)
    
    languages = ['en', 'hi', 'de', 'fr', 'es', 'ru']
    
    for lang in languages:
        lang_file = lang_path / f'{lang}.json'
        
        if not lang_file.exists():
            print(f"⚠ {lang.upper()}: File not found")
            continue
        
        try:
            with open(lang_file, 'r', encoding='utf-8') as f:
                lang_json = json.load(f)
            
            # Get SEO translations for this language
            seo_data = SEO_TRANSLATIONS.get(lang, {})
            
            if not seo_data:
                print(f"⊘ {lang.upper()}: No SEO translations available")
                continue
            
            # Update each section
            updated_sections = 0
            for section, content in seo_data.items():
                if section not in lang_json:
                    lang_json[section] = {}
                
                lang_json[section].update(content)
                updated_sections += 1
            
            # Save updated language file
            with open(lang_file, 'w', encoding='utf-8') as f:
                json.dump(lang_json, f, ensure_ascii=False, indent=2)
            
            print(f"✅ {lang.upper():5} - Updated {updated_sections} sections")
        
        except Exception as e:
            print(f"❌ {lang.upper()}: Error - {e}")
    
    print("=" * 60)
    print("\n✨ Language JSON files updated with SEO content!")

if __name__ == '__main__':
    update_language_files()
