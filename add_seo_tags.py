#!/usr/bin/env python3
"""
Add comprehensive SEO meta tags to all HTML pages
"""

import os
import re
from bs4 import BeautifulSoup

def add_seo_tags_to_destination(file_path):
    """Add SEO tags to destination pages"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    soup = BeautifulSoup(content, 'html.parser')
    head = soup.find('head')
    
    if not head:
        print(f"⚠️  No <head> found in {file_path}")
        return False
    
    # Extract page name from file path
    page_name = os.path.basename(file_path).replace('.html', '').replace('-', ' ').title()
    base_url = "https://www.mykutch.org"
    rel_path = file_path.replace('site/', '').replace('site\\', '').replace('\\', '/')
    page_url = f"{base_url}/{rel_path}"
    
    # Check if canonical exists
    canonical = head.find('link', {'rel': 'canonical'})
    if not canonical:
        canonical_tag = soup.new_tag('link', rel='canonical', href=page_url)
        # Insert after viewport meta
        viewport = head.find('meta', {'name': 'viewport'})
        if viewport:
            viewport.insert_after(soup.new_tag('string', text='\n    '))
            viewport.insert_after(canonical_tag)
        else:
            head.append(canonical_tag)
        print(f"  ✓ Added canonical URL")
    
    # Check if keywords meta exists
    keywords = head.find('meta', {'name': 'keywords'})
    if not keywords:
        keywords_tag = soup.new_tag('meta', attrs={'name': 'keywords', 'content': f'{page_name}, Kutch, Gujarat, tourism, travel guide'})
        description = head.find('meta', {'name': 'description'})
        if description:
            description.insert_after(soup.new_tag('string', text='\n    '))
            description.insert_after(keywords_tag)
        print(f"  ✓ Added keywords meta tag")
    
    # Check if robots meta exists
    robots = head.find('meta', {'name': 'robots'})
    if not robots:
        robots_tag = soup.new_tag('meta', attrs={'name': 'robots', 'content': 'index, follow'})
        head.append(soup.new_tag('string', text='\n    '))
        head.append(robots_tag)
        print(f"  ✓ Added robots meta tag")
    
    # Check if author meta exists
    author = head.find('meta', {'name': 'author'})
    if not author:
        author_tag = soup.new_tag('meta', attrs={'name': 'author', 'content': 'MyKutch.org'})
        head.append(soup.new_tag('string', text='\n    '))
        head.append(author_tag)
        print(f"  ✓ Added author meta tag")
    
    # Add Open Graph tags if missing
    og_type = head.find('meta', {'property': 'og:type'})
    if not og_type:
        print(f"  ✓ Adding Open Graph tags...")
        
        # Get title and description
        title_tag = head.find('title')
        desc_tag = head.find('meta', {'name': 'description'})
        
        title_text = title_tag.string if title_tag else page_name
        desc_text = desc_tag.get('content', '') if desc_tag else f"Explore {page_name} in Kutch, Gujarat"
        
        # Create OG tags
        og_tags = [
            ('og:type', 'article'),
            ('og:url', page_url),
            ('og:title', title_text),
            ('og:description', desc_text),
            ('og:site_name', 'MyKutch.org'),
            ('og:locale', 'en_US'),
        ]
        
        # Add OG tags
        for prop, content_val in og_tags:
            tag = soup.new_tag('meta', attrs={'property': prop, 'content': content_val})
            head.append(soup.new_tag('string', text='\n    '))
            head.append(tag)
    
    # Add Twitter Card tags if missing
    twitter_card = head.find('meta', {'name': 'twitter:card'}) or head.find('meta', {'property': 'twitter:card'})
    if not twitter_card:
        print(f"  ✓ Adding Twitter Card tags...")
        
        title_tag = head.find('title')
        desc_tag = head.find('meta', {'name': 'description'})
        
        title_text = title_tag.string if title_tag else page_name
        desc_text = desc_tag.get('content', '') if desc_tag else f"Explore {page_name} in Kutch, Gujarat"
        
        twitter_tags = [
            ('twitter:card', 'summary_large_image'),
            ('twitter:url', page_url),
            ('twitter:title', title_text),
            ('twitter:description', desc_text),
        ]
        
        for name, content_val in twitter_tags:
            tag = soup.new_tag('meta', attrs={'property': name, 'content': content_val})
            head.append(soup.new_tag('string', text='\n    '))
            head.append(tag)
    
    # Write back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    
    return True

def process_all_destinations():
    """Process all destination pages"""
    dest_dir = 'site/destinations'
    
    if not os.path.exists(dest_dir):
        print(f"❌ Directory not found: {dest_dir}")
        return
    
    files = [f for f in os.listdir(dest_dir) if f.endswith('.html') and not f.endswith('.bak')]
    files = [f for f in files if '_template' not in f and 'google' not in f]
    
    print(f"\n📄 Processing {len(files)} destination pages...\n")
    
    for filename in sorted(files):
        file_path = os.path.join(dest_dir, filename)
        print(f"Processing: {filename}")
        add_seo_tags_to_destination(file_path)
        print()

def process_all_crafts():
    """Process all craft pages"""
    craft_dir = 'site/crafts'
    
    if not os.path.exists(craft_dir):
        print(f"❌ Directory not found: {craft_dir}")
        return
    
    files = [f for f in os.listdir(craft_dir) if f.endswith('.html') and not f.endswith('.bak')]
    
    print(f"\n🎨 Processing {len(files)} craft pages...\n")
    
    for filename in sorted(files):
        file_path = os.path.join(craft_dir, filename)
        print(f"Processing: {filename}")
        add_seo_tags_to_destination(file_path)
        print()

def process_main_pages():
    """Process main pages"""
    main_pages = [
        'site/about.html',
        'site/blog.html',
        'site/bookings.html',
        'site/destinations.html',
        'site/distance-matrix.html',
        'site/geography.html',
        'site/hidden-gems.html',
        'site/history.html',
        'site/landscapes.html',
    ]
    
    print(f"\n📋 Processing {len(main_pages)} main pages...\n")
    
    for file_path in main_pages:
        if os.path.exists(file_path):
            print(f"Processing: {os.path.basename(file_path)}")
            add_seo_tags_to_destination(file_path)
            print()
        else:
            print(f"⚠️  File not found: {file_path}\n")

if __name__ == '__main__':
    print("=" * 60)
    print("SEO Meta Tags Enhancement Script")
    print("=" * 60)
    
    process_all_destinations()
    process_all_crafts()
    process_main_pages()
    
    print("=" * 60)
    print("✅ SEO enhancement complete!")
    print("=" * 60)
