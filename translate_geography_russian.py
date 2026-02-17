"""
Script to translate geography page to Russian only
"""

import json
import time
from deep_translator import GoogleTranslator

def translate_text(text, max_retries=3):
    """Translate text to Russian with retry logic"""
    try:
        if not text or text.strip() == '':
            return text
        
        if text.strip().startswith('http') or text in ['→', '☀️', '🌧️', '❄️', '🌍']:
            return text
        
        # Skip long intro texts that were already skipped
        if len(text) > 300:
            print(f"  Skipping long text: {text[:60]}...")
            return text
        
        # Skip numeric values
        if any(x in text for x in ['45,674', '23,310', '462m', '924', '356mm', '2°C - 50°C', 
                                     'MyKutch.org', 'www.', 'http', '.html']):
            print(f"  Skipping: {text[:60]}")
            return text
        
        for attempt in range(max_retries):
            try:
                translator = GoogleTranslator(source='en', target='ru')
                translated = translator.translate(text)
                time.sleep(0.3)
                return translated
            except Exception as e:
                if attempt < max_retries - 1:
                    print(f"    Retry {attempt + 1}/{max_retries}...")
                    time.sleep(3)
                else:
                    raise e
        
        return text
    except Exception as e:
        print(f"    Error: {e}, keeping original")
        return text

def translate_nested(data, path=""):
    """Recursively translate nested structures"""
    if isinstance(data, dict):
        translated = {}
        for key, value in data.items():
            current_path = f"{path}.{key}" if path else key
            print(f"  Processing: {current_path}")
            translated[key] = translate_nested(value, current_path)
        return translated
    elif isinstance(data, str):
        print(f"    Translating: {data[:60]}...")
        return translate_text(data)
    else:
        return data

def main():
    print("Loading files...")
    
    with open('site/lang/en.json', 'r', encoding='utf-8') as f:
        en_data = json.load(f)
    
    with open('site/lang/ru.json', 'r', encoding='utf-8') as f:
        ru_data = json.load(f)
    
    print("\nTranslating geography_page to Russian...")
    geography_en = en_data.get('geography_page', {})
    
    geography_ru = translate_nested(geography_en)
    
    ru_data['geography_page'] = geography_ru
    
    print("\nSaving to site/lang/ru.json...")
    with open('site/lang/ru.json', 'w', encoding='utf-8') as f:
        json.dump(ru_data, f, ensure_ascii=False, indent=2)
    
    print("✓ Russian translation complete!")

if __name__ == '__main__':
    main()
