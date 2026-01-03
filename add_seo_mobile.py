"""
Script to add SEO meta tags and mobile improvements to all HTML pages
"""

import os
import re

# Define SEO metadata for each page
pages_seo = {
    "index.html": {
        "title": "MyKutch.org | Explore the Best of Kutch, Gujarat",
        "description": "Discover Kutch - India's largest district. Explore the White Rann, ancient temples, artisan villages, and pristine beaches. Your complete travel guide to Kutch, Gujarat.",
        "keywords": "Kutch, Gujarat, White Rann, Rann of Kutch, Bhuj, Mandvi, travel guide, India tourism",
        "og_type": "website"
    },
    "destinations.html": {
        "title": "All Destinations | Explore Every Corner of Kutch",
        "description": "Complete guide to all destinations in Kutch - from Bhuj to the White Rann, Mandvi beaches to Dholavira ruins. Plan your perfect Kutch adventure.",
        "keywords": "Kutch destinations, Bhuj, Mandvi, Dhordo, White Rann, Gandhidham, tourist places Kutch",
        "og_type": "website"
    },
    "hidden-gems.html": {
        "title": "Hidden Gems of Kutch | Secret Treasures Beyond Tourist Trail",
        "description": "Discover secret treasures of Kutch - from serene wetlands to ancient temples. Explore hidden gems known only to locals.",
        "keywords": "hidden gems Kutch, Chaari Dhand, Kotay temple, off-beat Kutch, secret places Gujarat",
        "og_type": "article"
    },
    "history.html": {
        "title": "History of Kutch | 5000 Years of Heritage & Culture",
        "description": "Explore the rich history of Kutch from Harappan civilization to Jadeja rulers. Discover the cultural heritage spanning 5000 years.",
        "keywords": "Kutch history, Jadeja dynasty, Dholavira, Harappan civilization, Gujarat heritage",
        "og_type": "article"
    },
    "geography.html": {
        "title": "Geography of Kutch | India's Largest District",
        "description": "Explore the geography of Kutch - India's largest district. Learn about the Great Rann, Little Rann, Banni Grasslands, climate, and terrain.",
        "keywords": "Kutch geography, Great Rann, Little Rann, Banni Grasslands, Kalo Dungar, salt desert India",
        "og_type": "article"
    },
    "crafts.html": {
        "title": "Kutch Crafts | Traditional Handicrafts & Artisan Villages",
        "description": "Discover the famous handicrafts of Kutch - Bandhani, Ajrakh, embroidery, and leather work. Visit artisan villages and learn about traditional crafts.",
        "keywords": "Kutch handicrafts, Bandhani, Ajrakh, embroidery, Bhujodi, Nirona, artisan villages",
        "og_type": "article"
    },
    "landscapes.html": {
        "title": "Landscapes of Kutch | Salt Deserts to Beaches",
        "description": "Experience the stunning visual diversity of Kutch - from white salt deserts to pristine beaches, rocky hills to grasslands.",
        "keywords": "Kutch landscapes, White Rann, Mandvi beach, Banni grasslands, desert landscape India",
        "og_type": "article"
    },
    "bookings.html": {
        "title": "Book Hotels & Travel | Kutch Travel Bookings",
        "description": "Book hotels, flights, and travel in Kutch. Find the best deals on accommodations in Bhuj, Mandvi, and Rann of Kutch.",
        "keywords": "Kutch hotels, Bhuj hotels, Rann Utsav booking, Mandvi resorts, travel booking Gujarat",
        "og_type": "website"
    },
    "about.html": {
        "title": "About MyKutch.org | Your Guide to Kutch",
        "description": "Learn about MyKutch.org - your comprehensive guide to exploring Kutch, Gujarat. Discover our mission to showcase the vibrant culture and heritage of Kutch.",
        "keywords": "MyKutch, about us, Kutch travel guide, Gujarat tourism",
        "og_type": "website"
    }
}

def add_seo_to_page(filepath, seo_data):
    """Add SEO meta tags to a single HTML page"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    filename = os.path.basename(filepath)
    
    # Check if OG tags already exist
    if 'og:title' in content:
        print(f"  Skipping {filename} - OG tags already exist")
        return
    
    # Build SEO meta tags
    seo_tags = f'''
    <!-- SEO Meta Tags -->
    <meta name="keywords" content="{seo_data['keywords']}">
    <meta name="author" content="MyKutch.org">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="https://mykutch.org/{filename}">
    
    <!-- Open Graph / Facebook -->
    <meta property="og:type" content="{seo_data['og_type']}">
    <meta property="og:url" content="https://mykutch.org/{filename}">
    <meta property="og:title" content="{seo_data['title']}">
    <meta property="og:description" content="{seo_data['description']}">
    <meta property="og:image" content="https://mykutch.org/assets/images/logo.png">
    <meta property="og:site_name" content="MyKutch.org">
    
    <!-- Twitter -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:url" content="https://mykutch.org/{filename}">
    <meta name="twitter:title" content="{seo_data['title']}">
    <meta name="twitter:description" content="{seo_data['description']}">
    <meta name="twitter:image" content="https://mykutch.org/assets/images/logo.png">
'''
    
    # Insert SEO tags after the description meta tag
    pattern = r'(<meta name="description"[^>]*>)'
    if re.search(pattern, content):
        content = re.sub(pattern, r'\1' + seo_tags, content)
    else:
        # If no description, insert after charset
        pattern = r'(<meta charset="UTF-8">)'
        content = re.sub(pattern, r'\1' + seo_tags, content)
    
    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"  ✓ Updated {filename}")

def add_mobile_css_improvements(filepath):
    """Add mobile CSS improvements if needed"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    filename = os.path.basename(filepath)
    
    # Check if mobile improvements already exist
    if '.stats-grid' in content and '@media' in content:
        # Check if stats-grid mobile CSS exists
        if 'grid-template-columns: repeat(2' not in content:
            # Add mobile CSS for stats grid
            mobile_css = '''
            .stats-grid {
                grid-template-columns: repeat(2, 1fr);
            }
            
            .grid-2[style*="repeat(3"] {
                grid-template-columns: 1fr !important;
            }'''
            
            # Find the @media block and add to it
            pattern = r'(@media \(max-width: 768px\) \{[^}]*)'
            if re.search(pattern, content):
                content = re.sub(pattern, r'\1' + mobile_css, content)
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"  ✓ Added mobile CSS to {filename}")

def main():
    site_dir = r"C:\website_project\mykutch\site"
    
    print("Adding SEO meta tags and mobile improvements...")
    print("-" * 50)
    
    for filename, seo_data in pages_seo.items():
        filepath = os.path.join(site_dir, filename)
        if os.path.exists(filepath):
            print(f"\nProcessing {filename}:")
            add_seo_to_page(filepath, seo_data)
            add_mobile_css_improvements(filepath)
        else:
            print(f"\n⚠ File not found: {filename}")
    
    print("\n" + "=" * 50)
    print("SEO and mobile improvements complete!")

if __name__ == "__main__":
    main()
