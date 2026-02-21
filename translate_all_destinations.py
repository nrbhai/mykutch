#!/usr/bin/env python3
"""
Translate all individual destination blocks (destinations.*) to German, French, Spanish, and Russian
"""
import json
import time
from pathlib import Path
from deep_translator import GoogleTranslator

# Language mapping
LANGUAGES = {
    'de': 'german',
    'fr': 'french',
    'es': 'spanish',
    'ru': 'russian'
}

def translate_text(text, target_lang):
    """Translate text to target language with retry"""
    if not text or not isinstance(text, str):
        return text
    
    # Skip if already translated (contains non-ASCII characters)
    if not text.isascii() and target_lang in ['de', 'fr', 'es', 'ru']:
        return text
    
    try:
        translator = GoogleTranslator(source='en', target=target_lang)
        result = translator.translate(text)
        time.sleep(0.2)  # Rate limiting
        return result
    except Exception as e:
        print(f"  ⚠ Translation error: {e}")
        return text  # Return original on error

def translate_nested_dict(data, target_lang, path="", depth=0):
    """Recursively translate all string values in nested dict"""
    if isinstance(data, dict):
        result = {}
        for key, value in data.items():
            current_path = f"{path}.{key}" if path else key
            result[key] = translate_nested_dict(value, target_lang, current_path, depth+1)
        return result
    elif isinstance(data, str):
        if depth > 0 and len(data) > 3:  # Only print for actual content, not keys
            print(f"    {path}")
        return translate_text(data, target_lang)
    else:
        return data

def main():
    base_dir = Path(__file__).parent / 'site' / 'lang'
    
    # Load English source
    print("Loading English source...")
    with open(base_dir / 'en.json', 'r', encoding='utf-8') as f:
        en_data = json.load(f)
    
    destinations_en = en_data.get('destinations', {})
    if not destinations_en:
        print("ERROR: No destinations block in en.json")
        return
    
    destination_count = len(destinations_en)
    print(f"Found {destination_count} destinations to translate\n")
    
    # Translate for each language
    for lang_code, lang_name in LANGUAGES.items():
        print(f"\n{'='*70}")
        print(f"TRANSLATING TO {lang_name.upper()} ({lang_code})")
        print(f"{'='*70}\n")
        
        # Load existing language file
        lang_file = base_dir / f'{lang_code}.json'
        with open(lang_file, 'r', encoding='utf-8') as f:
            lang_data = json.load(f)
        
        # Translate each destination
        for i, (dest_slug, dest_content) in enumerate(destinations_en.items(), 1):
            print(f"  [{i}/{destination_count}] {dest_slug}")
            translated = translate_nested_dict(dest_content, lang_code, f"destinations.{dest_slug}")
            
            # Update the language file
            if 'destinations' not in lang_data:
                lang_data['destinations'] = {}
            lang_data['destinations'][dest_slug] = translated
        
        # Write back
        with open(lang_file, 'w', encoding='utf-8') as f:
            json.dump(lang_data, f, ensure_ascii=False, indent=2)
        
        print(f"\n  ✓ Updated {lang_file.name}")
    
    print(f"\n{'='*70}")
    print(f"TRANSLATION COMPLETE!")
    print(f"{'='*70}")
    print(f"Translated {destination_count} destinations to 4 languages")
    print("Updated files: de.json, fr.json, es.json, ru.json")

if __name__ == '__main__':
    main()
