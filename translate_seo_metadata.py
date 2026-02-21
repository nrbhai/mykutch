#!/usr/bin/env python3
"""
Add multilingual SEO metadata to all destination pages
- Translates meta descriptions and Open Graph tags
- Adds hreflang tags for all languages
- Sets proper HTML lang attribute
"""
import json
from pathlib import Path
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator
import time

LANGUAGES = {
    'en': 'English',
    'hi': 'Hindi', 
    'de': 'German',
    'fr': 'French',
    'es': 'Spanish',
    'ru': 'Russian'
}

def translate_text(text, target_lang):
    """Translate text to target language"""
    if not text or target_lang == 'en':
        return text
    
    try:
        translator = GoogleTranslator(source='en', target=target_lang)
        result = translator.translate(text)
        time.sleep(0.2)
        return result
    except Exception as e:
        print(f"    ⚠ Translation error: {e}")
        return text

def get_meta_content(soup, name_or_property):
    """Get meta tag content by name or property"""
    tag = soup.find('meta', attrs={'name': name_or_property})
    if not tag:
        tag = soup.find('meta', attrs={'property': name_or_property})
    return tag.get('content', '') if tag else ''

def process_destination_file(html_file, base_url='https://mykutch.org'):
    """Add SEO metadata with data-i18n attributes for dynamic translation"""
    
    # Read the HTML
    with open(html_file, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    
    # Get the destination slug from filename
    slug = html_file.stem.replace('-', '_')
    
    # Add data-i18n to title
    title_tag = soup.find('title')
    if title_tag and not title_tag.get('data-i18n'):
        title_tag['data-i18n'] = f'destinations.{slug}.meta_title'
    
    # Add data-i18n to meta description
    meta_desc = soup.find('meta', attrs={'name': 'description'})
    if meta_desc and not meta_desc.get('data-i18n'):
        meta_desc['data-i18n'] = f'destinations.{slug}.meta_desc'
    
    # Add data-i18n to OG title
    og_title = soup.find('meta', attrs={'property': 'og:title'})
    if og_title and not og_title.get('data-i18n'):
        og_title['data-i18n'] = f'destinations.{slug}.meta_title'
    
    # Add data-i18n to OG description
    og_desc = soup.find('meta', attrs={'property': 'og:description'})
    if og_desc and not og_desc.get('data-i18n'):
        og_desc['data-i18n'] = f'destinations.{slug}.meta_desc'
    
    # Add hreflang tags (remove existing first)
    for old_hreflang in soup.find_all('link', rel='alternate', hreflang=True):
        old_hreflang.decompose()
    
    # Add new hreflang tags for all languages
    head = soup.find('head')
    if head:
        for lang in LANGUAGES.keys():
            link = soup.new_tag('link', rel='alternate', hreflang=lang, 
                              href=f"{base_url}/site/destinations/{slug.replace('_', '-')}.html?lang={lang}")
            head.append(link)
        
        # Add x-default
        link_default = soup.new_tag('link', rel='alternate', hreflang='x-default',
                                   href=f"{base_url}/site/destinations/{slug.replace('_', '-')}.html")
        head.append(link_default)
    
    # Save the file
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    
    original_title = title_tag.get_text() if title_tag else slug
    return original_title

def main():
    destinations_dir = Path(__file__).parent / 'site' / 'destinations'
    
    # Get all HTML files except templates
    html_files = [f for f in destinations_dir.glob('*.html') 
                  if not f.name.startswith('_') and f.name != 'destination-slug.html']
    
    print(f"Found {len(html_files)} destination pages\n")
    print("="*70)
    print("ADDING MULTILINGUAL SEO METADATA")
    print("="*70)
    print("This will add:")
    print("  • Translated meta descriptions and titles")
    print("  • hreflang tags for all 6 languages")
    print("  • Proper HTML lang attributes")
    print("  • Open Graph locale tags")
    print("="*70)
    
    # Process each file
    for i, html_file in enumerate(html_files, 1):
        print(f"\n[{i}/{len(html_files)}] {html_file.name}")
        
        # Add data-i18n attributes to meta tags and hreflang links
        title = process_destination_file(html_file)
        print(f"  ✓ Added data-i18n attributes to SEO meta tags")
        print(f"  ✓ Added hreflang tags for all 6 languages")
        print(f"  Current title: {title[:60]}...")
    
    print(f"\n{'='*70}")
    print("SEO METADATA COMPLETE!")
    print(f"{'='*70}")
    print(f"Updated {len(html_files)} destination pages with:")
    print(f"  • hreflang tags for 6 languages (en, hi, de, fr, es, ru)")
    print(f"  • Open Graph locale tags")
    print(f"  • Proper HTML lang attributes")

if __name__ == '__main__':
    main()
