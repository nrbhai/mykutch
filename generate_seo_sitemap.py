#!/usr/bin/env python3
"""
Generate comprehensive XML sitemap with language variants and hreflang tags
Includes all pages, destinations, crafts pages with multilingual support
"""

from pathlib import Path
from datetime import datetime
import xml.etree.ElementTree as ET

def generate_multilingual_sitemap():
    """Generate sitemap.xml with language alternates (hreflang)"""
    
    # Configuration
    base_url = 'https://www.mykutch.org'
    site_path = Path(__file__).parent / 'site'
    languages = ['en', 'hi', 'de', 'fr', 'es', 'ru']
    
    # Define all pages to include
    pages = {
        'index.html': {
            'path': '',
            'priority': '1.0',
            'changefreq': 'weekly',
        },
        'destinations.html': {
            'path': 'destinations.html',
            'priority': '0.9',
            'changefreq': 'monthly',
        },
        'crafts.html': {
            'path': 'crafts.html',
            'priority': '0.9',
            'changefreq': 'monthly',
        },
        'hidden-gems.html': {
            'path': 'hidden-gems.html',
            'priority': '0.8',
            'changefreq': 'monthly',
        },
        'history.html': {
            'path': 'history.html',
            'priority': '0.8',
            'changefreq': 'yearly',
        },
        'geography.html': {
            'path': 'geography.html',
            'priority': '0.8',
            'changefreq': 'yearly',
        },
        'landscapes.html': {
            'path': 'landscapes.html',
            'priority': '0.8',
            'changefreq': 'monthly',
        },
        'blog.html': {
            'path': 'blog.html',
            'priority': '0.7',
            'changefreq': 'weekly',
        },
        'bookings.html': {
            'path': 'bookings.html',
            'priority': '0.85',
            'changefreq': 'weekly',
        },
        'about.html': {
            'path': 'about.html',
            'priority': '0.6',
            'changefreq': 'yearly',
        },
        'distance-matrix.html': {
            'path': 'distance-matrix.html',
            'priority': '0.7',
            'changefreq': 'yearly',
        },
    }
    
    # Get all destination files
    destinations_path = site_path / 'destinations'
    destination_files = sorted([f for f in destinations_path.glob('*.html') 
                               if not f.name.startswith('_template') 
                               and f.name != 'destination-slug.html'])
    
    # Get all crafts files
    crafts_path = site_path / 'crafts'
    craft_files = sorted([f for f in crafts_path.glob('*.html')])
    
    print("📋 Generating Comprehensive XML Sitemap with Language Variants\n")
    print("=" * 70)
    
    # Create XML structure
    urlset = ET.Element('urlset')
    urlset.set('xmlns', 'http://www.sitemaps.org/schemas/sitemap/0.9')
    urlset.set('xmlns:xhtml', 'http://www.w3.org/1999/xhtml')
    
    total_urls = 0
    
    # Add main pages
    print("\n📄 Main Pages:")
    for filename, config in pages.items():
        path = config['path']
        
        # Create URL entry
        url_elem = ET.SubElement(urlset, 'url')
        
        # Add location for default language
        loc_elem = ET.SubElement(url_elem, 'loc')
        loc_elem.text = f"{base_url}/{path}" if path else base_url
        
        # Add lastmod
        lastmod_elem = ET.SubElement(url_elem, 'lastmod')
        lastmod_elem.text = datetime.now().strftime('%Y-%m-%d')
        
        # Add changefreq
        changefreq_elem = ET.SubElement(url_elem, 'changefreq')
        changefreq_elem.text = config.get('changefreq', 'monthly')
        
        # Add priority
        priority_elem = ET.SubElement(url_elem, 'priority')
        priority_elem.text = str(config.get('priority', '0.7'))
        
        # Add language alternates (hreflang)
        for lang in languages:
            xhtml_link = ET.SubElement(url_elem, '{http://www.w3.org/1999/xhtml}link')
            xhtml_link.set('rel', 'alternate')
            xhtml_link.set('hreflang', lang)
            xhtml_link.set('href', f"{base_url}/{path}?lang={lang}" if path else f"{base_url}?lang={lang}")
        
        # Add x-default alternate
        xhtml_default = ET.SubElement(url_elem, '{http://www.w3.org/1999/xhtml}link')
        xhtml_default.set('rel', 'alternate')
        xhtml_default.set('hreflang', 'x-default')
        xhtml_default.set('href', f"{base_url}/{path}" if path else base_url)
        
        total_urls += 1
        print(f"   ✓ {path if path else 'Index'}")
    
    # Add destination pages
    print(f"\n📍 Destination Pages ({len(destination_files)} locations):")
    for dest_file in destination_files:
        url_elem = ET.SubElement(urlset, 'url')
        
        # Location
        loc_elem = ET.SubElement(url_elem, 'loc')
        loc_elem.text = f"{base_url}/destinations/{dest_file.name}"
        
        # Last modified
        lastmod_elem = ET.SubElement(url_elem, 'lastmod')
        lastmod_elem.text = datetime.now().strftime('%Y-%m-%d')
        
        # Change frequency
        changefreq_elem = ET.SubElement(url_elem, 'changefreq')
        changefreq_elem.text = 'monthly'
        
        # Priority
        priority_elem = ET.SubElement(url_elem, 'priority')
        priority_elem.text = '0.8'
        
        # Language alternates
        for lang in languages:
            xhtml_link = ET.SubElement(url_elem, '{http://www.w3.org/1999/xhtml}link')
            xhtml_link.set('rel', 'alternate')
            xhtml_link.set('hreflang', lang)
            xhtml_link.set('href', f"{base_url}/destinations/{dest_file.name}?lang={lang}")
        
        xhtml_default = ET.SubElement(url_elem, '{http://www.w3.org/1999/xhtml}link')
        xhtml_default.set('rel', 'alternate')
        xhtml_default.set('hreflang', 'x-default')
        xhtml_default.set('href', f"{base_url}/destinations/{dest_file.name}")
        
        total_urls += 1
    
    print(f"   ✓ All {len(destination_files)} destination pages added")
    
    # Add craft pages
    print(f"\n🎨 Craft Pages ({len(craft_files)} crafts):")
    for craft_file in craft_files:
        url_elem = ET.SubElement(urlset, 'url')
        
        # Location
        loc_elem = ET.SubElement(url_elem, 'loc')
        loc_elem.text = f"{base_url}/crafts/{craft_file.name}"
        
        # Last modified
        lastmod_elem = ET.SubElement(url_elem, 'lastmod')
        lastmod_elem.text = datetime.now().strftime('%Y-%m-%d')
        
        # Change frequency
        changefreq_elem = ET.SubElement(url_elem, 'changefreq')
        changefreq_elem.text = 'monthly'
        
        # Priority
        priority_elem = ET.SubElement(url_elem, 'priority')
        priority_elem.text = '0.7'
        
        # Language alternates
        for lang in languages:
            xhtml_link = ET.SubElement(url_elem, '{http://www.w3.org/1999/xhtml}link')
            xhtml_link.set('rel', 'alternate')
            xhtml_link.set('hreflang', lang)
            xhtml_link.set('href', f"{base_url}/crafts/{craft_file.name}?lang={lang}")
        
        xhtml_default = ET.SubElement(url_elem, '{http://www.w3.org/1999/xhtml}link')
        xhtml_default.set('rel', 'alternate')
        xhtml_default.set('hreflang', 'x-default')
        xhtml_default.set('href', f"{base_url}/crafts/{craft_file.name}")
        
        total_urls += 1
    
    print(f"   ✓ All {len(craft_files)} craft pages added")
    
    # Pretty print and save sitemap
    tree_str = ET.tostring(urlset, encoding='unicode')
    pretty_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
{tree_str}"""
    
    sitemap_path = site_path / 'sitemap.xml'
    with open(sitemap_path, 'w', encoding='utf-8') as f:
        f.write(pretty_xml)
    
    print("\n" + "=" * 70)
    print(f"\n✨ Sitemap Generated Successfully!")
    print(f"\n📊 Sitemap Statistics:")
    print(f"   • Total URLs: {total_urls}")
    print(f"   • Main pages: {len(pages)}")
    print(f"   • Destination pages: {len(destination_files)}")
    print(f"   • Craft pages: {len(craft_files)}")
    print(f"   • Languages supported: {len(languages)}")
    print(f"   • File location: {sitemap_path}")
    
    print(f"\n🌐 Language Variants Included:")
    for lang in languages:
        print(f"   ✓ {lang}")
    
    print(f"\n📌 SEO Features:")
    print(f"   ✓ Hreflang tags for multilingual SEO")
    print(f"   ✓ x-default alternate for fallback language")
    print(f"   ✓ Priority levels for search ranking")
    print(f"   ✓ Change frequency indicators")
    print(f"   ✓ Last modified dates")

if __name__ == '__main__':
    generate_multilingual_sitemap()
