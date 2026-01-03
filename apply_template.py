
import os
import re

DESTINATIONS_DIR = r"c:\website_project\mykutch\site\destinations"
TEMPLATE_FILE = os.path.join(DESTINATIONS_DIR, "bhuj.html")

def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def write_file(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def extract_content(html, patterns, default=""):
    for pattern in patterns:
        match = re.search(pattern, html, re.DOTALL | re.IGNORECASE)
        if match:
            return match.group(1).strip()
    return default

def get_landmarks_html(html):
    # Try to find the grid containing landmarks. 
    # In old files, look for "Landmarks & Heritage" then the grid-2 or similar div
    # Robust method: Find "attraction-card" divs and rebuild them if needed, 
    # but simpler is to extract the whole grid container content if poss.
    # Pattern: Look for section "Landmarks & Heritage" -> capture content until next section
    
    # Strategy 1: Find the Landmarks section
    section_match = re.search(r'(Landmarks.*?Heritage.*?)(<section)', html, re.DOTALL | re.IGNORECASE)
    if section_match:
        # Inside this section, find the grid-2
        section_content = section_match.group(1)
        grid_match = re.search(r'<div class="grid-2">(.*?)</div>\s*</section>', section_content, re.DOTALL)
        if not grid_match:
             # Try broader match for cards
             grid_match = re.search(r'<div class="grid-2">(.*?)</div>', section_content, re.DOTALL)
        
        if grid_match:
            # We have the cards HTML
            cards_html = grid_match.group(1)
            # CLEANUP: Remove old inline styles found in cards
            cards_html = re.sub(r'style="[^"]*"', '', cards_html) 
            # Re-add specific styles if we killed standard ones? 
            # Actually our template CSS handles .attraction-card well without inline styles.
            # But wait, image error handling might be inline. 
            # Let's try to preserve image tags carefully or just strip dangerous styles.
            
            # Remove height/color styles from anchor tags if any
            cards_html = re.sub(r'<a([^>]*)style="[^"]*"', r'<a\1', cards_html)
            
            return cards_html
            
    return "<!-- Landmarks content not found -->"

def main():
    if not os.path.exists(TEMPLATE_FILE):
        print(f"Error: Template file {TEMPLATE_FILE} not found.")
        return

    template_content = read_file(TEMPLATE_FILE)
    
    # ---------------------------------------------------------
    # ANALYZE TEMPLATE STRUCTURE
    # ---------------------------------------------------------
    # We will split template into chunks to inject variables
    
    # 1. Header (everything up to title)
    # Using specific markers in bhuj.html
    
    # Title Marker
    t_title_start = template_content.find("<title>") + 7
    t_title_end = template_content.find("</title>")
    
    # Desc Marker
    t_desc_start = template_content.find('content="', template_content.find('<meta name="description"')) + 9
    t_desc_end = template_content.find('">', t_desc_start)
    
    # Hero Image Marker
    t_hero_img_start = template_content.find("background-image: url('../assets/images/bhuj/bhuj1.webp')")
    # We will replace the whole style string or just the url
    
    # Hero Title (Subtitle is now Title)
    t_hero_title_marker = "Bhuj — The Cultural Heart of Kutch"
    
    # Lead Text
    t_lead_start = template_content.find('<p class="lead-text">') + 21
    t_lead_end = template_content.find('</p>', t_lead_start)
    
    # Who Should Visit List
    t_who_start = template_content.find('<ul class="styled-list">', template_content.find("Who Should Visit")) + 24
    t_who_end = template_content.find('</ul>', t_who_start)
    
    # How to Reach List
    t_reach_start = template_content.find('<ul class="styled-list">', template_content.find("How to Reach")) + 24
    t_reach_end = template_content.find('</ul>', t_reach_start)
    
    # Landmarks HTML (The whole grid content)
    # We need to recognize the Landmarks GRID to replace its inner HTML
    t_land_header_pos = template_content.find("Landmarks & Heritage")
    t_land_grid_start = template_content.find('<div class="grid-2">', t_land_header_pos) + 20
    t_land_grid_end = template_content.find('</div>', t_land_grid_start)
    # Ensure we capture closing div correctly (counting divs? No, structure is flattened in template usually)
    # For robust replacement, let's use the exact block string from bhuj if possible or Markers
    
    # We will assume standard indentation helps us or just regex the template too?
    # Let's use placeholders in a CLEAN template string for better safety.
    
    # Constructing a format string from the template
    # This is safer than string slicing
    
    new_template = template_content
    
    # Placeholders
    new_template = new_template.replace("Bhuj — Cultural Heart of Kutch | Kutch Travel Guide", "{PAGE_TITLE}")
    new_template = new_template.replace("Explore Bhuj — Cultural Heart of Kutch. Complete travel guide with attractions, itinerary, how to reach, and local tips.", "{META_DESC}")
    new_template = new_template.replace("bhuj/bhuj1.webp", "{HERO_IMAGE_BASENAME}") # e.g. mandvi/mandvi1.webp
    new_template = new_template.replace("Bhuj — The Cultural Heart of Kutch", "{HERO_TITLE}")
    
    # Lead Text
    # We need to be careful to match the exact string in file
    lead_text_content = """Bhuj is the cultural and logistical heart of Kutch, serving as the perfect base for exploring the
                    region. Blending 500 years of royal history with modern resilience, this city is a living museum of
                    palaces, bazaars, and narrow winding streets. From here, you can launch expeditions to the White
                    Rann, the northern craft villages, and the southern beaches. A typical visit requires 2 days to
                    fully appreciate its museums, palaces, and the nearby artisan hubs of Bhujodi and <a
                        href="../crafts/ajrakh.html">Ajrakhpur</a>."""
    # Normalize whitespace for matching
    # Actually, let's Regex replace the Lead Text block in the template object
    new_template = re.sub(r'<p class="lead-text">\s*(.*?)\s*</p>', r'<p class="lead-text">{LEAD_TEXT}</p>', new_template, flags=re.DOTALL)
    
    # Replaces Lists
    # Who Should Visit
    new_template = re.sub(r'(Who Should Visit.*?<ul class="styled-list">)(.*?)(</ul>)', r'\1{WHO_VISIT_LIST}\3', new_template, flags=re.DOTALL)
    
    # How to Reach
    new_template = re.sub(r'(How to Reach.*?<ul class="styled-list">)(.*?)(</ul>)', r'\1{HOW_REACH_LIST}\3', new_template, flags=re.DOTALL)
    
    # Landmarks
    # Replace content of grid-2 after Landmarks
    new_template = re.sub(r'(Landmarks & Heritage.*?<div class="grid-2">)(.*?)(</div>\s*</section>)', r'\1{LANDMARKS_GRID}\3', new_template, flags=re.DOTALL)
    
    # Editorial Advice (Tips Grid)
    new_template = re.sub(r'(Curated Local Advice.*?<div class="tips-grid">)(.*?)(</div>\s*</div>\s*</section>)', r'\1{TIPS_GRID}\3', new_template, flags=re.DOTALL)
    
    # Shopping
    new_template = re.sub(r'(Shopping & Bazaars.*?<ul class="styled-list">)(.*?)(</ul>)', r'\1{SHOPPING_LIST}\3', new_template, flags=re.DOTALL)
    
    # Eats
    new_template = re.sub(r'(Local Eats.*?<ul class="styled-list">)(.*?)(</ul>)', r'\1{EATS_LIST}\3', new_template, flags=re.DOTALL)
    
    # When to Visit
    # This is a P tag in a section
    new_template = re.sub(r'(When to Visit.*?</div>\s*<p>)(.*?)(</p>)', r'\1{WHEN_VISIT}\3', new_template, flags=re.DOTALL)
    
    # Nearby Places
    new_template = re.sub(r'(Nearby Places to Visit.*?<div class="grid-2">)(.*?)(</div>\s*</section>)', r'\1{NEARBY_GRID}\3', new_template, flags=re.DOTALL)
    
    # Itinerary
    # Replace the container content
    new_template = re.sub(r'(Suggested Itinerary.*?<div style="margin: 0; max-width: 800px;">)(.*?)(</div>\s*</section>)', r'\1{ITINERARY_CONTENT}\3', new_template, flags=re.DOTALL)
    
    # Map (Iframe src)
    new_template = re.sub(r'<iframe\s*src="([^"]+)"', r'<iframe src="{MAP_SRC}"', new_template)
    
    # Gallery
    # Capture the grid content
    new_template = re.sub(r'(Location & Gallery.*?<div class="gallery-grid">)(.*?)(</div>\s*</section>)', r'\1{GALLERY_IMAGES}\3', new_template, flags=re.DOTALL)
    
    # ---------------------------------------------------------
    # PROCESS FILES
    # ---------------------------------------------------------
    
    for filename in os.listdir(DESTINATIONS_DIR):
        if not filename.endswith(".html"): continue
        if filename == "bhuj.html": continue
        
        file_path = os.path.join(DESTINATIONS_DIR, filename)
        print(f"Processing {filename}...")
        
        original_html = read_file(file_path)
        
        # EXTRACT DATA
        
        # Title
        page_title = extract_content(original_html, [r'<title>(.*?)</title>'], "MyKutch Destination")
        
        # Meta Desc
        meta_desc = extract_content(original_html, [r'<meta name="description"\s+content="(.*?)">'], "")
        
        # Hero Image
        # Extract the full relative path e.g. ../assets/images/mandvi/mandvi1.webp
        hero_img_full = extract_content(original_html, [r"background-image: url\('([^']+)'\)"], "../assets/images/bhuj/bhuj1.webp")
        # We need to strip the prefix if it's there
        # Template expects "{HERO_IMAGE_BASENAME}" but wait, template has `.../assets/images/{HERO_IMAGE_BASENAME}`?
        # No, my replacement above was naive. 
        # In Bhuj it is: background-image: url('../assets/images/bhuj/bhuj1.webp')
        # If I replace "bhuj/bhuj1.webp" with the extracted "mandvi/mandvi1.webp", it should work IF extracted has that part.
        # But extracted might have "url('../assets/images/mandvi/mandvi1.webp')"
        # Let's extract just the part after images/
        match_img = re.search(r'images/([^"\')]+)', hero_img_full)
        hero_img_basename = match_img.group(1) if match_img else "bhuj/bhuj1.webp"
        
        # Hero Title (Subtitle + Title)
        # Old structure: h1 hero-text + p subtitle
        old_h1 = extract_content(original_html, [r'<h1 class="hero-text-bright">(.*?)</h1>'], "Destination")
        old_sub = extract_content(original_html, [r'<p class="hero-text-bright"[^>]*>(.*?)</p>'], "")
        # Remove extra whitespace/newlines
        old_h1 = " ".join(old_h1.split())
        old_sub = " ".join(old_sub.split())
        hero_title_combined = f"{old_h1}"
        if old_sub:
            hero_title_combined += f" — {old_sub}"
            
        # Lead Text
        lead_text = extract_content(original_html, [r'<p class="lead-text">\s*(.*?)\s*</p>'], "Explore this beautiful destination in Kutch.")
        
        # Who Should Visit
        who_visit = extract_content(original_html, [r'Who Should Visit.*?<ul class="styled-list">(.*?)</ul>'], "<li>Information coming soon...</li>")
        
        # How to Reach
        how_reach = extract_content(original_html, [r'How to Reach.*?<ul class="styled-list">(.*?)</ul>'], "<li>Check local transport options.</li>")
        
        # Landmarks (Complex)
        landmarks_grid = "<!-- Landmarks not found -->"
        l_match = re.search(r'(Landmarks & Heritage.*?<div class="grid-2">)(.*?)(</div>\s*</section>)', original_html, re.DOTALL | re.IGNORECASE)
        if not l_match:
             # Try without the strict section wrapper or different title
             # Try just finding the grid after "Landmarks"
             l_match = re.search(r'Landmarks.*?<div class="grid-2">(.*?)</div>', original_html, re.DOTALL | re.IGNORECASE)
             
        if l_match:
            raw_land = l_match.group(2) if len(l_match.groups()) > 1 else l_match.group(1)
            # CLEANUP required: Old mandvi.html has style=... in cards. Remove it.
            raw_land = re.sub(r'style="[^"]*"', '', raw_land)
            landmarks_grid = raw_land
            
        # Tips Grid
        tips_grid = extract_content(original_html, [r'<div class="tips-grid">(.*?)</div>', r'Curated Local Advice.*?<div class="grid-2">(.*?)</div>'], "<!-- Tips not found -->")
        
        # Shopping
        shopping_list = extract_content(original_html, [r'Shopping & Bazaars.*?<ul class="styled-list">(.*?)</ul>'], "<li>Local markets available.</li>")
        
        # Eats
        eats_list = extract_content(original_html, [r'Local Eats.*?<ul class="styled-list">(.*?)</ul>'], "<li>Local food options available.</li>")
        
        # When to Visit
        # Old: <section ...> <h3>...</h3> <p>CONTENT</p> </section>
        when_visit = extract_content(original_html, [r'When to Visit.*?<p>(.*?)</p>'], "Best time to visit is winter (Oct-Feb).")
        
        # Nearby Places
        # Old: <section ...> <h2>Nearby...</h2> <div class="grid-2">...</div> </section>
        nearby_grid = extract_content(original_html, [r'Nearby Places to Visit.*?<div class="grid-2">(.*?)</div>\s*</section>'], "<!-- No nearby places listed -->")
        # Cleanup inline styles from Nearby (old files def have them)
        nearby_grid = re.sub(r'style="[^"]*"', '', nearby_grid)
        
        # Itinerary
        # Old: <div class="itinerary-box">...</div> repeat
        # We need to capture the container inner html
        itinerary_content = "<!-- Itinerary coming soon -->"
        i_match = re.search(r'Suggested Itinerary.*?<div style="max-width: 600px; margin: 0 auto;">(.*?)</div>\s*</section>', original_html, re.DOTALL)
        if i_match:
            itinerary_content = i_match.group(1)
        
        # Map
        map_src = extract_content(original_html, [r'<iframe\s*src="([^"]+)"'], "")
        
        # Gallery
        gallery_images = extract_content(original_html, [r'<div class="gallery-grid">(.*?)</div>'], "")
        
        
        # FILL TEMPLATE
        output_html = new_template.replace("{PAGE_TITLE}", page_title)
        output_html = output_html.replace("{META_DESC}", meta_desc)
        output_html = output_html.replace("{HERO_IMAGE_BASENAME}", hero_img_basename)
        output_html = output_html.replace("{HERO_TITLE}", hero_title_combined)
        output_html = output_html.replace("{LEAD_TEXT}", lead_text)
        output_html = output_html.replace("{WHO_VISIT_LIST}", who_visit)
        output_html = output_html.replace("{HOW_REACH_LIST}", how_reach)
        output_html = output_html.replace("{LANDMARKS_GRID}", landmarks_grid)
        output_html = output_html.replace("{TIPS_GRID}", tips_grid)
        output_html = output_html.replace("{SHOPPING_LIST}", shopping_list)
        output_html = output_html.replace("{EATS_LIST}", eats_list)
        output_html = output_html.replace("{WHEN_VISIT}", when_visit)
        output_html = output_html.replace("{NEARBY_GRID}", nearby_grid)
        output_html = output_html.replace("{ITINERARY_CONTENT}", itinerary_content)
        output_html = output_html.replace("{MAP_SRC}", map_src)
        output_html = output_html.replace("{GALLERY_IMAGES}", gallery_images)
        
        write_file(file_path, output_html)
        print(f"Updated {filename}")

if __name__ == "__main__":
    main()
