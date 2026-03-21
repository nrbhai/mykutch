#!/usr/bin/env python3
"""
Generate sitemap.xml for MyKutch website dynamically
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
    
    site_dir = 'site'
    pages = []
    
    # Walk the site directory
    for root, dirs, files in os.walk(site_dir):
        # Exclude directories
        if 'assets' in dirs:
            dirs.remove('assets')
        if 'destinations_backup' in dirs:
            dirs.remove('destinations_backup')
        # Also remove any other backup dirs just in case
        dirs[:] = [d for d in dirs if not d.endswith('_backup')]
            
        for file in files:
            if file.endswith('.html') and not file.startswith('_') and not file.startswith('google'):
                # Get the relative path from 'site' directory
                rel_path = os.path.relpath(os.path.join(root, file), site_dir)
                
                # Convert backslashes to forward slashes for URLs
                url_path = rel_path.replace('\\', '/')
                
                # Assign default priorities and change frequencies
                priority = 0.6
                changefreq = 'monthly'
                
                if url_path == 'index.html':
                    url_path = ''
                    priority = 1.0
                    changefreq = 'weekly'
                elif url_path in ['about.html', 'blog.html', 'bookings.html', 'crafts.html', 'destinations.html', 'hidden-gems.html']:
                    priority = 0.8
                    changefreq = 'weekly'
                elif url_path.startswith('destinations/'):
                    # Some important destinations
                    if file in ['bhuj.html', 'dholavira.html', 'dhordo-white-rann.html', 'mandvi.html']:
                        priority = 0.8
                        changefreq = 'weekly'
                    else:
                        priority = 0.7
                        changefreq = 'monthly'
                elif url_path.startswith('crafts/'):
                    priority = 0.7
                    changefreq = 'monthly'
                
                pages.append((url_path, priority, changefreq))
    
    # Sort pages to have empty (homepage) first, then alphabetical
    pages.sort(key=lambda x: (x[0] != '', x[0]))

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
