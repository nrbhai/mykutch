#!/usr/bin/env python3
"""
Generate sitemap.xml for MyKutch website
"""

import os
from datetime import datetime
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom

def generate_sitemap():
    # Base URL
    base_url = "https://www.mykutch.org"
    
    # Current date for lastmod
    current_date = datetime.now().strftime('%Y-%m-%d')
    
    # Define pages with their priorities and change frequencies
    pages = [
        # Homepage - highest priority
        ('', 1.0, 'weekly'),
        
        # Main pages
        ('about.html', 0.8, 'monthly'),
        ('blog.html', 0.8, 'weekly'),
        ('bookings.html', 0.9, 'weekly'),
        ('crafts.html', 0.8, 'weekly'),
        ('destinations.html', 0.9, 'weekly'),
        ('distance-matrix.html', 0.7, 'monthly'),
        ('geography.html', 0.7, 'monthly'),
        ('hidden-gems.html', 0.8, 'weekly'),
        ('history.html', 0.7, 'monthly'),
        ('landscapes.html', 0.7, 'weekly'),
        
        # Craft pages
        ('crafts/ajrakh.html', 0.7, 'monthly'),
        ('crafts/bandhani.html', 0.7, 'monthly'),
        ('crafts/leather-craft.html', 0.7, 'monthly'),
        ('crafts/mirror-work.html', 0.7, 'monthly'),
        ('crafts/pottery.html', 0.7, 'monthly'),
        ('crafts/rogan-art.html', 0.7, 'monthly'),
        ('crafts/sudi-chappu.html', 0.7, 'monthly'),
        ('crafts/weaving.html', 0.7, 'monthly'),
        
        # Destination pages - high priority
        ('destinations/72-jinalaya.html', 0.6, 'monthly'),
        ('destinations/abjibapa-chatardi.html', 0.6, 'monthly'),
        ('destinations/adipur.html', 0.6, 'monthly'),
        ('destinations/anjar.html', 0.6, 'monthly'),
        ('destinations/asar-mata-beach.html', 0.6, 'monthly'),
        ('destinations/bhadreshwar.html', 0.6, 'monthly'),
        ('destinations/bhuj.html', 0.8, 'weekly'),
        ('destinations/bhujodi.html', 0.7, 'monthly'),
        ('destinations/dholavira.html', 0.8, 'weekly'),
        ('destinations/dhordo-white-rann.html', 0.9, 'weekly'),
        ('destinations/dhrang-mekan-dada.html', 0.6, 'monthly'),
        ('destinations/gandhidham.html', 0.6, 'monthly'),
        ('destinations/gangeshwar-mahadev.html', 0.6, 'monthly'),
        ('destinations/haji-pir.html', 0.6, 'monthly'),
        ('destinations/hanuman-tekri-kodki.html', 0.6, 'monthly'),
        ('destinations/hiralaxmi-memorial-park.html', 0.6, 'monthly'),
        ('destinations/jadura.html', 0.6, 'monthly'),
        ('destinations/jakhau.html', 0.6, 'monthly'),
        ('destinations/kadia-dhrow.html', 0.8, 'weekly'),
        ('destinations/kalo-dungar.html', 0.7, 'monthly'),
        ('destinations/kandla.html', 0.6, 'monthly'),
        ('destinations/kashi-vishwanath-beach.html', 0.6, 'monthly'),
        ('destinations/kotay-surya-mandir.html', 0.6, 'monthly'),
        ('destinations/lakhpat.html', 0.7, 'monthly'),
        ('destinations/madhapar.html', 0.6, 'monthly'),
        ('destinations/mandvi.html', 0.8, 'weekly'),
        ('destinations/mata-na-madh.html', 0.6, 'monthly'),
        ('destinations/matang-matiya-dev.html', 0.6, 'monthly'),
        ('destinations/mundra.html', 0.6, 'monthly'),
        ('destinations/narayan-sarovar-koteshwar.html', 0.7, 'monthly'),
        ('destinations/nirona.html', 0.7, 'monthly'),
        ('destinations/road-to-heaven.html', 0.7, 'weekly'),
        ('destinations/rudramata-dam.html', 0.6, 'monthly'),
        
        # Hidden gems
        ('hidden-gems/chaari-dhand.html', 0.6, 'monthly'),
    ]
    
    # Create XML structure
    urlset = Element('urlset')
    urlset.set('xmlns', 'http://www.sitemaps.org/schemas/sitemap/0.9')
    urlset.set('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
    urlset.set('xsi:schemaLocation', 'http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd')
    
    # Add each page
    for page, priority, changefreq in pages:
        url = SubElement(urlset, 'url')
        
        # Location
        loc = SubElement(url, 'loc')
        if page:
            loc.text = f"{base_url}/{page}"
        else:
            loc.text = f"{base_url}/"
        
        # Last modified
        lastmod = SubElement(url, 'lastmod')
        lastmod.text = current_date
        
        # Change frequency
        freq = SubElement(url, 'changefreq')
        freq.text = changefreq
        
        # Priority
        prio = SubElement(url, 'priority')
        prio.text = str(priority)
    
    # Pretty print XML
    xml_str = minidom.parseString(tostring(urlset)).toprettyxml(indent="  ")
    
    # Remove extra blank lines
    xml_str = '\n'.join([line for line in xml_str.split('\n') if line.strip()])
    
    # Write to file
    with open('site/sitemap.xml', 'w', encoding='utf-8') as f:
        f.write(xml_str)
    
    print(f"✓ Sitemap generated successfully with {len(pages)} pages")
    print(f"✓ Saved to: site/sitemap.xml")

if __name__ == '__main__':
    generate_sitemap()
