#!/usr/bin/env python3
"""
Translate only meta_title and meta_desc for all destinations
"""
import json
import time
from pathlib import Path
from deep_translator import GoogleTranslator

LANGUAGES = {
    'de': 'german',
    'fr': 'french',
    'es': 'spanish',
    'ru': 'russian'
}

def translate_text(text, target_lang):
    """Translate text to target language"""
    if not text:
        return text
    
    try:
        translator = GoogleTranslator(source='en', target=target_lang)
        result = translator.translate(text)
        time.sleep(0.2)
        return result
    except Exception as e:
        print(f"    ⚠ Error: {e}")
        return text

def main():
    base_dir = Path(__file__).parent / 'site' / 'lang'
    
    # Load English source
    with open(base_dir / 'en.json', 'r', encoding='utf-8') as f:
        en_data = json.load(f)
    
    destinations_en = en_data.get('destinations', {})
    
    print(f"Translating SEO metadata for {len(destinations_en)} destinations\n")
    
    for lang_code, lang_name in LANGUAGES.items():
        print(f"\n{'='*70}")
        print(f"TRANSLATING SEO TO {lang_name.upper()} ({lang_code})")
        print(f"{'='*70}\n")
        
        # Load language file
        lang_file = base_dir / f'{lang_code}.json'
        with open(lang_file, 'r', encoding='utf-8') as f:
            lang_data = json.load(f)
        
        if 'destinations' not in lang_data:
            lang_data['destinations'] = {}
        
        # Translate meta_title and meta_desc for each destination
        for i, (slug, content) in enumerate(destinations_en.items(), 1):
            meta_title = content.get('meta_title', '')
            meta_desc = content.get('meta_desc', '')
            
            if not meta_title and not meta_desc:
                continue
            
            print(f"  [{i}/{len(destinations_en)}] {slug}")
            
            if slug not in lang_data['destinations']:
                lang_data['destinations'][slug] = {}
            
            if meta_title:
                translated_title = translate_text(meta_title, lang_code)
                lang_data['destinations'][slug]['meta_title'] = translated_title
                print(f"      meta_title: {translated_title[:50]}...")
            
            if meta_desc:
                translated_desc = translate_text(meta_desc, lang_code)
                lang_data['destinations'][slug]['meta_desc'] = translated_desc
                print(f"      meta_desc: {translated_desc[:50]}...")
        
        # Save
        with open(lang_file, 'w', encoding='utf-8') as f:
            json.dump(lang_data, f, ensure_ascii=False, indent=2)
        
        print(f"\n  ✓ Updated {lang_file.name}")
    
    print(f"\n{'='*70}")
    print("SEO TRANSLATION COMPLETE!")
    print(f"{'='*70}")

if __name__ == '__main__':
    main()
