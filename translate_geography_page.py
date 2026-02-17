"""
Script to translate geography page content into multiple languages
Uses Google Translate API via deep-translator library
"""

import json
import time
from deep_translator import GoogleTranslator

# Language configurations
LANGUAGES = {
    'de': 'German',
    'es': 'Spanish',
    'fr': 'French',
    'ru': 'Russian'
}

def translate_text(text, target_lang, source_lang='en', max_retries=3):
    """Translate text using Google Translate with retry logic"""
    try:
        # Handle empty strings
        if not text or text.strip() == '':
            return text
        
        # Don't translate HTML tags and special formatting
        if text.strip().startswith('http') or text in ['→', '☀️', '🌧️', '❄️', '🌍']:
            return text
        
        # Retry logic for network errors
        for attempt in range(max_retries):
            try:
                translator = GoogleTranslator(source=source_lang, target=target_lang)
                translated = translator.translate(text)
                time.sleep(0.2)  # Increased rate limiting
                return translated
            except Exception as e:
                if attempt < max_retries - 1:
                    print(f"    Retry {attempt + 1}/{max_retries} after error...")
                    time.sleep(2)  # Wait before retry
                else:
                    raise e
        
        return text
    except Exception as e:
        print(f"    Error translating '{text[:50]}...': {e}")
        return text  # Return original if translation fails

def translate_geography_nested(data, target_lang, path=""):
    """Recursively translate nested dictionary structures"""
    if isinstance(data, dict):
        translated = {}
        for key, value in data.items():
            current_path = f"{path}.{key}" if path else key
            translated[key] = translate_geography_nested(value, target_lang, current_path)
        return translated
    elif isinstance(data, str):
        # Don't translate these specific keys or values
        if any(x in data for x in ['45,674', '23,310', '462m', '924', '356mm', '2°C - 50°C', 
                                     'MyKutch.org', 'www.', 'http', '.html', 'data-i18n']):
            print(f"  Skipping: {data[:60]}")
            return data
        
        print(f"  Translating: {data[:60]}...")
        return translate_text(data, target_lang)
    else:
        return data

def main():
    """Main translation function"""
    
    # Load English source
    print("Loading English source file...")
    with open('site/lang/en.json', 'r', encoding='utf-8') as f:
        en_data = json.load(f)
    
    geography_en = en_data.get('geography_page', {})
    
    if not geography_en:
        print("ERROR: geography_page not found in en.json")
        return
    
    # Translate for each target language
    for lang_code, lang_name in LANGUAGES.items():
        print(f"\n{'='*60}")
        print(f"Translating to {lang_name} ({lang_code})...")
        print(f"{'='*60}")
        
        # Load target language file
        lang_file = f'site/lang/{lang_code}.json'
        try:
            with open(lang_file, 'r', encoding='utf-8') as f:
                lang_data = json.load(f)
        except FileNotFoundError:
            print(f"WARNING: {lang_file} not found, skipping...")
            continue
        
        # Translate geography section
        print(f"\nTranslating geography_page section...")
        geography_translated = translate_geography_nested(geography_en, lang_code)
        
        # Update the language file
        lang_data['geography_page'] = geography_translated
        
        # Save updated file
        print(f"\nSaving to {lang_file}...")
        with open(lang_file, 'w', encoding='utf-8') as f:
            json.dump(lang_data, f, ensure_ascii=False, indent=2)
        
        print(f"✓ {lang_name} translation complete!")
        
        # Wait between languages to avoid rate limiting
        if lang_code != list(LANGUAGES.keys())[-1]:
            print("\nWaiting 2 seconds before next language...")
            time.sleep(2)
    
    print(f"\n{'='*60}")
    print("All translations complete!")
    print(f"{'='*60}")

if __name__ == '__main__':
    main()
