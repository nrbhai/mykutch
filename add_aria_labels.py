#!/usr/bin/env python3
"""
Add ARIA labels and accessibility improvements
"""

import os
from bs4 import BeautifulSoup

def add_aria_labels(file_path):
    """Add ARIA labels to navigation and interactive elements"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    soup = BeautifulSoup(content, 'html.parser')
    changes = 0
    
    # Add aria-label to mobile toggle buttons
    mobile_toggles = soup.find_all('button', class_='mobile-toggle')
    for btn in mobile_toggles:
        if not btn.get('aria-label'):
            btn['aria-label'] = 'Toggle navigation menu'
            changes += 1
    
    # Add aria-label to dark mode toggle
    dark_mode_toggles = soup.find_all('button', id='darkModeToggle')
    for btn in dark_mode_toggles:
        if not btn.get('aria-label'):
            # Already has aria-label in the HTML, skip
            pass
    
    # Add aria-label to navigation links without text
    nav_links = soup.find_all('a', class_='logo')
    for link in nav_links:
        if not link.get('aria-label'):
            link['aria-label'] = 'MyKutch Home'
            changes += 1
    
    # Add role="navigation" to nav elements without it
    navs = soup.find_all('nav')
    for nav in navs:
        if not nav.get('role'):
            nav['role'] = 'navigation'
            nav['aria-label'] = 'Main navigation'
            changes += 1
    
    # Add role="main" to main elements
    mains = soup.find_all('main')
    for main in mains:
        if not main.get('role'):
            main['role'] = 'main'
            changes += 1
    
    # Add role="contentinfo" to footer
    footers = soup.find_all('footer')
    for footer in footers:
        if not footer.get('role'):
            footer['role'] = 'contentinfo'
            changes += 1
    
    # Write back if changes were made
    if changes > 0:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        return changes
    
    return 0

def process_all_pages():
    """Process all HTML pages"""
    
    total_files = 0
    total_changes = 0
    
    # Walk through all HTML files
    for root, dirs, files in os.walk('site'):
        # Skip backup directories
        if 'backup' in root or '_backup' in root:
            continue
        
        for file in files:
            if file.endswith('.html') and not file.endswith('.bak'):
                # Skip template and google verification files
                if '_template' in file or 'google' in file:
                    continue
                
                file_path = os.path.join(root, file)
                total_files += 1
                
                changes = add_aria_labels(file_path)
                total_changes += changes
                
                if changes > 0:
                    print(f"✓ {file}: {changes} ARIA improvements")
    
    print("\n" + "=" * 60)
    print("📊 Summary:")
    print(f"   Files processed: {total_files}")
    print(f"   Total ARIA improvements: {total_changes}")
    print("=" * 60)

if __name__ == '__main__':
    print("=" * 60)
    print("ARIA Labels & Accessibility Enhancement Script")
    print("=" * 60)
    print()
    
    process_all_pages()
    
    print("\n✅ Accessibility enhancements complete!")
