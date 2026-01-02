import os
import re

# Source Data Directory (Original React Project)
SOURCE_DIR = r"c:\website_project\kutchtravel\app\crafts"
OUTPUT_DIR = r"crafts"
ASSETS_PREFIX = "../assets"

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# Template for Craft Pages
TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | Kutch Travel Guide</title>
    <meta name="description" content="{seo_description}">
    
    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=Poppins:wght@400;500;600;700&display=swap" rel="stylesheet">
    
    <link rel="stylesheet" href="../css/style.css">
    <style>
        body {{ font-family: 'Inter', sans-serif; }}
        h1, h2, h3, h4, .logo {{ font-family: 'Poppins', sans-serif; }}
        
        .craft-hero {{
            position: relative;
            height: 70vh;
            min-height: 500px;
            background-size: cover;
            background-position: center;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            text-align: center;
        }}
        .craft-hero::before {{
            content: '';
            position: absolute;
            inset: 0;
            background: rgba(0,0,0,0.4);
        }}
        .hero-content-inner {{
            position: relative;
            z-index: 2;
            padding: 0 1rem;
            max-width: 900px;
        }}
        .hero-content-inner h1 {{
            font-size: clamp(2.5rem, 6vw, 5rem);
            margin-bottom: 1rem;
            text-shadow: 0 4px 20px rgba(0,0,0,0.3);
        }}
        .subtitle {{
            font-size: 1.5rem;
            opacity: 0.9;
            font-weight: 300;
            letter-spacing: 0.05em;
        }}

        .craft-section {{
            padding: 6rem 0;
            display: flex;
            align-items: center;
            gap: 4rem;
        }}
        .craft-section:nth-child(even) {{
            flex-direction: row-reverse;
        }}
        .craft-text {{ flex: 1; }}
        .craft-image {{ flex: 1; }}
        
        .craft-image img {{
            width: 100%;
            height: 400px;
            object-fit: cover;
            border-radius: 1rem;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        }}

        .section-heading {{
            font-size: 2.5rem;
            margin-bottom: 1.5rem;
            color: var(--color-heading);
            position: relative;
            display: inline-block;
        }}
        .section-heading::after {{
            content: '';
            display: block;
            width: 60px;
            height: 3px;
            background: var(--color-primary);
            margin-top: 0.5rem;
        }}

        .facts-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 2rem;
            background: #fff;
            padding: 4rem;
            border-radius: 2rem;
            box-shadow: 0 10px 30px rgba(0,0,0,0.05);
            margin: 4rem 0;
        }}
        .fact-card {{
            display: flex;
            gap: 1rem;
            align-items: center;
        }}
        .fact-icon {{ font-size: 2rem; }}

        @media (max-width: 900px) {{
            .craft-section {{ flex-direction: column !important; gap: 2rem; padding: 4rem 0; }}
            .craft-image img {{ height: 300px; }}
            .facts-grid {{ padding: 2rem; }}
        }}
    </style>
</head>
<body>
    <nav class="scrolled">
        <div class="container nav-content">
            <a href="../index.html" class="logo">KUTCH TRAVEL</a>
            <div class="nav-links">
                <a href="../index.html">Home</a>
                <a href="../index.html#destinations">Destinations</a>
                <a href="../index.html#crafts">Crafts</a>
            </div>
        </div>
    </nav>

    <header class="craft-hero" style="background-image: url('{heroImage}')">
        <div class="hero-content-inner reveal">
            <h1>{title}</h1>
            <div class="subtitle">{subtitle}</div>
        </div>
    </header>

    <main class="container">
        
        {sections_html}

        <div class="reveal">
            <div class="facts-grid">
                <div style="grid-column: 1/-1; text-align: center; margin-bottom: 2rem;">
                    <h2 class="section-heading" style="font-size: 2rem;">Did You Know?</h2>
                </div>
                {facts_html}
            </div>
        </div>

        <div class="section reveal">
            <h2 class="section-heading text-center" style="display: block; text-align: center; margin-bottom: 3rem;">Gallery</h2>
            <div class="gallery-grid" style="display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 1.5rem;">
                {gallery_html}
            </div>
        </div>

    </main>

    <footer class="footer-main" style="margin-top: 0;">
        <div class="container" style="text-align: center; padding: 2rem 0;">
            <p style="opacity: 0.6; font-size: 0.9rem;">&copy; 2026 Kutch Travel Guide. Designed with ❤️.</p>
        </div>
    </footer>

    <script src="../js/script.js"></script>
</body>
</html>
"""

def extract_field(content, field):
    match = re.search(f"{field}:\\s*[\"'](.*?)[\"']", content)
    if match: return match.group(1).strip()
    return ""

def extract_array(content, array_name):
    # Extract content inside array brackets
    match = re.search(f"{array_name}:\\s*\[(.*?)\]", content, re.DOTALL)
    if not match: return []
    raw = match.group(1)
    # Simple split might break if strings contain commas, but sufficient for this data structure
    items = re.findall(r"[\"'](.*?)[\"']", raw)
    return items

def extract_obj_array(content, array_name):
    # Extract array of objects string
    match = re.search(f"{array_name}:\\s*\[(.*?)\]\s*,", content, re.DOTALL)
    if not match: 
        # try end of file
        match = re.search(f"{array_name}:\\s*\[(.*?)\]", content, re.DOTALL)
        if not match: return []
    
    raw = match.group(1)
    # extract objects
    objs = re.findall(r"\{(.*?)\}", raw, re.DOTALL)
    return objs

def get_image_path(path):
    if path.startswith("/"):
        return ASSETS_PREFIX + path
    return path

def process_craft(dirname):
    page_path = os.path.join(SOURCE_DIR, dirname, "page.tsx")
    if not os.path.exists(page_path):
        return

    with open(page_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract Main Info
    title = extract_field(content, "title")
    subtitle = extract_field(content, "subtitle")
    heroImage = get_image_path(extract_field(content, "image"))
    slug = extract_field(content, "slug")
    if not slug: slug = dirname

    # Extract Sections
    section_objs = extract_obj_array(content, "sections")
    sections_html = ""
    
    # We need a fallback image if a section doesn't have one, or just alternate
    default_img = heroImage

    for i, section in enumerate(section_objs):
        heading = extract_field(section, "heading")
        text = extract_field(section, "content")
        
        # Check for list
        if not text:
            list_match = re.search(r"list:\s*\[(.*?)\]", section, re.DOTALL)
            if list_match:
                list_items = re.findall(r"[\"'](.*?)[\"']", list_match.group(1))
                text = "<ul style='list-style: none; padding: 0;'><li style='margin-bottom:0.5rem; display:flex; gap:0.5rem; align-items:center;'><span style='color:var(--color-primary);'>•</span>" + "</li><li style='margin-bottom:0.5rem; display:flex; gap:0.5rem; align-items:center;'><span style='color:var(--color-primary);'>•</span>".join(list_items) + "</li></ul>"
        
        # Try to find an image for this section
        # The regex is tricky for nested objects in the same string block
        # Simple heuristic: Look for src: "..." inside the section block
        img_match = re.search(r"src:\s*[\"'](.*?)[\"']", section)
        sec_img = get_image_path(img_match.group(1)) if img_match else default_img
        
        if heading:
            sections_html += f"""
            <div class="craft-section reveal">
                <div class="craft-text">
                    <h2 class="section-heading">{heading}</h2>
                    <div class="article-text" style="font-size: 1.1rem; line-height: 1.8; color: #555;">{text}</div>
                </div>
                <div class="craft-image">
                    <img src="{sec_img}" alt="{heading}">
                </div>
            </div>
            """

    # Extract Facts
    facts = extract_array(content, "facts")
    facts_html = ""
    for fact in facts:
        facts_html += f'<div class="fact-card"><span class="fact-icon">✨</span><p>{fact}</p></div>'

    # Extract Gallery
    gallery_objs = extract_obj_array(content, "gallery")
    gallery_html = ""
    for obj in gallery_objs:
        src = get_image_path(extract_field(obj, "src"))
        cap = extract_field(obj, "caption")
        gallery_html += f'<div class="reveal"><img src="{src}" alt="{cap}" style="width:100%; height:300px; object-fit:cover; border-radius:1rem;"></div>'

    # SEO Description
    seo_desc = f"Discover the art of {title} in Kutch. {subtitle}."

    output_html = TEMPLATE.format(
        title=title,
        subtitle=subtitle,
        seo_description=seo_desc,
        heroImage=heroImage,
        sections_html=sections_html,
        facts_html=facts_html,
        gallery_html=gallery_html
    )

    with open(os.path.join(OUTPUT_DIR, f"{slug}.html"), 'w', encoding='utf-8') as f:
        f.write(output_html)
    print(f"Generated crafts/{slug}.html")

if __name__ == "__main__":
    if os.path.exists(SOURCE_DIR):
        print(f"Reading crafts from {SOURCE_DIR}...")
        for item in os.listdir(SOURCE_DIR):
            if os.path.isdir(os.path.join(SOURCE_DIR, item)):
                try:
                    process_craft(item)
                except Exception as e:
                    print(f"Error processing {item}: {e}")
    else:
        print(f"Source directory {SOURCE_DIR} not found.")
