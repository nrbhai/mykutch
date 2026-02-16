#!/usr/bin/env python3
"""
Translate history_page content to German, French, Spanish, Russian, and Hindi
"""
import json
import time
from pathlib import Path
from deep_translator import GoogleTranslator

# Language mapping - only ru and hi remaining
LANGUAGES = {
    'ru': 'russian',
    'hi': 'hindi'
}

def translate_text(text, target_lang):
    """Translate text to target language with retry"""
    if not text or not isinstance(text, str):
        return text
    
    # Skip translation for certain strings
    skip_patterns = ['MyKutch', 'Kutch', 'Dholavira', 'Bhuj', 'Mandvi', 'Khengarji', 'Pragmalji',
                     'Jadeja', 'Samma', 'Chavda', 'Rajput', 'Kanthkot', 'Rann', 'Gujarat',
                     'UNESCO', 'Aina Mahal', 'Prag Mahal', 'Vijay Vilas', 'Kandla', 'Mundra',
                     'Rann Utsav', 'Aabhir', 'Sindh', 'Mesopotamia', 'Khadir Bet', 'Harappan',
                     'Indus Valley', 'Mughal', 'Kutch Kori', 'Maharao']
    
    # Retry logic with exponential backoff
    max_retries = 5
    for attempt in range(max_retries):
        try:
            translator = GoogleTranslator(source='en', target=target_lang)
            result = translator.translate(text)
            time.sleep(1.0)  # Longer delay to avoid rate limiting
            return result
        except KeyboardInterrupt:
            raise  # Allow user to cancel
        except Exception as e:
            if attempt < max_retries - 1:
                wait_time = (attempt + 1) * 3  # Exponential backoff
                print(f"  ⚠ Retry {attempt + 1}/{max_retries}: {str(e)[:50]}, waiting {wait_time}s")
                time.sleep(wait_time)
            else:
                print(f"  ⚠ Translation failed after {max_retries} attempts: {str(e)[:50]}")
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
    
    history_page_en = en_data.get('history_page', {})
    if not history_page_en:
        print("ERROR: No history_page block in en.json")
        return
    
    print(f"Found history_page content to translate\n")
    
    # Translate for each language
    for lang_code, lang_name in LANGUAGES.items():
        print(f"\n{'='*70}")
        print(f"TRANSLATING TO {lang_name.upper()} ({lang_code})")
        print(f"{'='*70}\n")
        
        # Load existing language file
        lang_file = base_dir / f'{lang_code}.json'
        with open(lang_file, 'r', encoding='utf-8') as f:
            lang_data = json.load(f)
        
        # Translate history_page
        print(f"  Translating history_page...")
        translated_content = translate_nested_dict(history_page_en, lang_code, "history_page")
        
        # Update language file
        lang_data['history_page'] = translated_content
        
        # Save updated language file
        with open(lang_file, 'w', encoding='utf-8') as f:
            json.dump(lang_data, f, ensure_ascii=False, indent=2)
        
        print(f"  ✓ Saved to {lang_file.name}")
    
    print("\n" + "="*70)
    print("TRANSLATION COMPLETE!")
    print("="*70)

if __name__ == '__main__':
    main()
