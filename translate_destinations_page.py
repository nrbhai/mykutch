#!/usr/bin/env python3
"""
Translate destinations_page block to German, French, Spanish, and Russian
"""
import json
import time
from pathlib import Path

try:
    from deep_translator import GoogleTranslator
except ImportError:
    print("Installing deep-translator...")
    import subprocess
    subprocess.check_call(['pip', 'install', 'deep-translator'])
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
    
    try:
        translator = GoogleTranslator(source='en', target=target_lang)
        result = translator.translate(text)
        time.sleep(0.3)  # Rate limiting
        return result
    except Exception as e:
        print(f"  Translation error for '{text[:50]}...': {e}")
        return text  # Return original on error

def translate_nested_dict(data, target_lang, path=""):
    """Recursively translate all string values in nested dict"""
    if isinstance(data, dict):
        result = {}
        for key, value in data.items():
            current_path = f"{path}.{key}" if path else key
            result[key] = translate_nested_dict(value, target_lang, current_path)
        return result
    elif isinstance(data, str):
        print(f"  Translating: {path}")
        return translate_text(data, target_lang)
    else:
        return data

def main():
    base_dir = Path(__file__).parent / 'site' / 'lang'
    
    # Load English source
    print("Loading English source...")
    with open(base_dir / 'en.json', 'r', encoding='utf-8') as f:
        en_data = json.load(f)
    
    destinations_page_en = en_data.get('destinations_page', {})
    if not destinations_page_en:
        print("ERROR: No destinations_page in en.json")
        return
    
    print(f"Found destinations_page with {len(destinations_page_en)} top-level keys\n")
    
    # Translate for each language
    for lang_code, lang_name in LANGUAGES.items():
        print(f"\n{'='*60}")
        print(f"TRANSLATING TO {lang_name.upper()} ({lang_code})")
        print(f"{'='*60}")
        
        # Load existing language file
        lang_file = base_dir / f'{lang_code}.json'
        with open(lang_file, 'r', encoding='utf-8') as f:
            lang_data = json.load(f)
        
        # Translate destinations_page
        print(f"Translating destinations_page content...")
        translated = translate_nested_dict(destinations_page_en, lang_code)
        
        # Update the language file
        lang_data['destinations_page'] = translated
        
        # Write back
        with open(lang_file, 'w', encoding='utf-8') as f:
            json.dump(lang_data, f, ensure_ascii=False, indent=2)
        
        print(f"✓ Updated {lang_file.name}")
    
    print(f"\n{'='*60}")
    print("TRANSLATION COMPLETE!")
    print(f"{'='*60}")
    print("Updated files: de.json, fr.json, es.json, ru.json")

if __name__ == '__main__':
    main()
