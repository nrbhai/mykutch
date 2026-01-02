import os
import re

# Paths
SOURCE_DIR = r"c:\website_project\kutchtravel\app\destinations\data"
DEST_DIR = r"c:\website_project\newkutch\destinations"
ROOT_DIR = r"c:\website_project\newkutch"

# Compile Regex Patterns
RE_TITLE = re.compile(r'title:\s*["\']([^"\']+)["\']')
RE_SLUG = re.compile(r'slug:\s*["\']([^"\']+)["\']')
RE_HERO_IMAGE = re.compile(r'image:\s*["\']([^"\']+)["\']') 
RE_MAP = re.compile(r'mapUrl:\s*["\']([^"\']+)["\']')

def parse_list_robust(text):
    items = []
    current = []
    in_quote = False
    quote_char = None
    escape = False
    
    text = text.strip()
    if text.startswith('[') and text.endswith(']'):
        text = text[1:-1]
    
    for i, char in enumerate(text):
        if not in_quote:
            if char in ['"', "'"]:
                in_quote = True
                quote_char = char
            elif char == ',' and not current:
                continue 
        else:
            if escape:
                current.append(char)
                escape = False
            elif char == '\\':
                escape = True
            elif char == quote_char:
                in_quote = False
                quote_char = None
                items.append("".join(current))
                current = []
            else:
                current.append(char)
    return items

def extract_content(text):
    sections = []
    matches = list(re.finditer(r'heading:\s*["\']([^"\']+)["\']', text))
    
    for i, match in enumerate(matches):
        heading = match.group(1)
        start_pos = match.end()
        
        post_text = text[start_pos:]
        markers = []
        for marker in [r'heading:', r'facts:', r'mapUrl:', r'gallery:']:
             m = re.search(marker, post_text)
             if m:
                 markers.append(m.start())
        
        if markers:
            end_pos = start_pos + min(markers)
        else:
            end_pos = len(text)
            
        block = text[start_pos:end_pos]
        section_data = {'heading': heading}
        
        content_match = re.search(r'content:\s*(["\'])((?:\\\1|.)*?)\1', block, re.DOTALL)
        if content_match:
            raw_content = content_match.group(2)
            section_data['content'] = raw_content.replace('\\n', '<br>').replace('\n', ' ').replace('\\"', '"').replace("\\'", "'")

        list_match = re.search(r'list:\s*\[([\s\S]*?)\]', block)
        if list_match:
            raw_list = list_match.group(1)
            section_data['list'] = parse_list_robust(raw_list)

        img_match = re.search(r'src:\s*["\']([^"\']+)["\']', block)
        if img_match:
            section_data['image'] = img_match.group(1)
            
        sections.append(section_data)
        
    return sections

def extract_gallery(text):
    gallery_match = re.search(r'gallery:\s*\[([\s\S]*?)\]', text)
    if not gallery_match:
        return []
    
    gallery_block = gallery_match.group(1)
    images = []
    objects = gallery_block.split('{')
    for obj in objects:
        if not obj.strip(): continue
        src_m = re.search(r'src:\s*["\']([^"\']+)["\']', obj)
        cap_m = re.search(r'caption:\s*["\']([^"\']+)["\']', obj)
        if src_m:
            images.append({
                'src': src_m.group(1),
                'caption': cap_m.group(1) if cap_m else "Gallery Image"
            })
        
    return images

def clean_html(text):
    text = re.sub(r'<[^>]+>', '', text)
    return text.strip()

def format_list_item(text):
    if ':' in text:
        parts = text.split(':', 1)
        return f"<strong>{parts[0]}</strong>:{parts[1]}"
    return text

def create_html(slug, title, hero_image, map_url, sections, gallery):
    # Logic for individual destination pages
    overview = next((s for s in sections if "Overview" in s.get('heading', '')), None)
    who_visit = next((s for s in sections if "Who Should Visit" in s.get('heading', '')), None)
    how_reach = next((s for s in sections if "How to Reach" in s.get('heading', '')), None)
    attractions = next((s for s in sections if "Famous Spots" in s.get('heading', '') or "Attractions" in s.get('heading', '') or "Top Things" in s.get('heading', '')), None)
    markets = next((s for s in sections if "Bazaars" in s.get('heading', '') or "Shopping" in s.get('heading', '')), None)
    food = next((s for s in sections if "Food" in s.get('heading', '')), None)
    itinerary = next((s for s in sections if "Itinerary" in s.get('heading', '')), None)
    tips = next((s for s in sections if "Tips" in s.get('heading', '') or "Mistakes" in s.get('heading', '')), None)
    best_time = next((s for s in sections if "Best Time" in s.get('heading', '')), None)
    nearby = next((s for s in sections if "Nearby" in s.get('heading', '')), None)

    attractions_html = ""
    if attractions and 'list' in attractions:
        attractions_html = '<section class="guide-section reveal"><div class="section-header"><h2>Landmarks & Heritage</h2><p style="opacity: 0.6; margin-top: 0.5rem;">The defining monuments</p></div><div class="grid-2">'
        for item in attractions['list']:
            clean_item = clean_html(item)
            parts = clean_item.split(':', 1)
            title_text = parts[0].strip()
            desc_text = parts[1].strip() if len(parts) > 1 else ""
            attractions_html += f"""
                    <div class="attraction-card">
                        <div class="attraction-img-wrapper">
                             <img src="../assets/images/{slug}/{slug}1.webp" onerror="this.style.display='none';this.parentElement.style.backgroundColor='#eee';this.parentElement.innerHTML='<div style=\\'display:flex;align-items:center;justify-content:center;height:100%;color:#888\\'>Image</div>'" alt="{title_text}">
                        </div>
                        <div class="attraction-content">
                            <h3 class="attraction-title">{title_text}</h3>
                            <p class="attraction-desc">{desc_text}</p>
                        </div>
                    </div>"""
        attractions_html += '</div></section>'

    nearby_html = ""
    if nearby and 'list' in nearby:
        nearby_html = '<section class="guide-section reveal"><div class="section-header"><h2>Nearby Places to Visit</h2></div><div class="grid-2">'
        for item in nearby['list']:
            clean_item = clean_html(item)
            parts = clean_item.split(':', 1)
            title_text = parts[0].strip()
            desc_text = parts[1].strip() if len(parts) > 1 else ""
            nearby_html += f"""
                    <a href="#" class="attraction-card" style="text-decoration: none; color: inherit; height: auto;">
                        <div class="attraction-content" style="padding: 1.5rem;">
                            <h3 class="attraction-title" style="font-size: 1.1rem;">{title_text}</h3>
                            <p style="font-size: 0.9rem;">{desc_text}</p>
                        </div>
                    </a>"""
        nearby_html += '</div></section>'

    tips_html = ""
    if tips and 'list' in tips:
        tips_html = '<section class="guide-section reveal"><div class="editorial-note"><h3>Curated Local Advice</h3><div class="tips-grid">'
        for item in tips['list']:
            clean_item = clean_html(item)
            parts = clean_item.split(':', 1)
            title_text = parts[0].strip()
            desc_text = parts[1].strip() if len(parts) > 1 else clean_item
            tips_html += f"""
                        <div class="tip-item">
                            <h4>{title_text}</h4>
                            <p>{desc_text}</p>
                        </div>"""
        tips_html += '</div></div></section>'

    itinerary_html = ""
    if itinerary and 'list' in itinerary:
        itinerary_html = '<section class="guide-section reveal"><div class="section-header"><h2>Suggested Itinerary</h2></div><div style="max-width: 600px; margin: 0 auto;">'
        for item in itinerary['list']:
            clean_item = clean_html(item)
            parts = clean_item.split(':', 1)
            title_text = parts[0].strip()
            desc_text = parts[1].strip() if len(parts) > 1 else clean_item
            itinerary_html += f"""
                     <div class="itinerary-box">
                        <div class="timeline-dot"></div>
                        <span class="day-header">{title_text}</span>
                        <p>{desc_text}</p>
                    </div>"""
        itinerary_html += '</div></section>'
        
    if markets and 'list' in markets: markets['list'] = [format_list_item(clean_html(i)) for i in markets['list']]
    if food and 'list' in food: food['list'] = [format_list_item(clean_html(i)) for i in food['list']]
    if who_visit and 'list' in who_visit: who_visit['list'] = [format_list_item(clean_html(i)) for i in who_visit['list']]
    if how_reach and 'list' in how_reach: how_reach['list'] = [format_list_item(clean_html(i)) for i in how_reach['list']]


    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | Kutch Travel Guide</title>
    <meta name="description" content="Explore {title}. Complete travel guide with attractions, itinerary, how to reach, and local tips.">
    
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=Poppins:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    
    <link rel="stylesheet" href="../css/style.css">
    <style>
        .editorial-container {{ max-width: 900px; margin: 0 auto; padding: 0 1.5rem; }}
        .section-header {{ text-align: center; margin-bottom: 3rem; margin-top: 5rem; }}
        .section-header h2 {{ font-size: 2.5rem; color: var(--color-heading); margin-bottom: 1rem; position: relative; display: inline-block; }}
        .section-header h2::after {{ content: ''; display: block; width: 40px; height: 2px; background: var(--color-primary); margin: 1rem auto 0; }}
        .guide-section {{ margin-bottom: 4rem; }}
        .lead-text {{ font-size: 1.25rem; line-height: 1.8; color: #444; font-weight: 300; }}
        .lead-text::first-letter {{ font-size: 3.5rem; float: left; line-height: 0.8; margin-right: 0.5rem; margin-top: 0.2rem; font-family: var(--font-heading); color: var(--color-primary); }}
        .styled-list {{ list-style: none; padding: 0; display: grid; gap: 1.5rem; }}
        .styled-list li {{ position: relative; padding-left: 1.5rem; font-size: 1.1rem; color: var(--color-text); border-left: 2px solid rgba(0,0,0,0.1); padding-left: 1.5rem; transition: border-color 0.3s; }}
        .styled-list li:hover {{ border-left-color: var(--color-primary); }}
        .styled-list strong, .styled-list b {{ color: var(--color-heading); font-weight: 600; display: block; margin-bottom: 0.25rem; font-family: var(--font-heading); letter-spacing: 0.02em; }}
        .styled-list li:nth-child(4n+1) strong {{ color: #C2410C; }}
        .styled-list li:nth-child(4n+2) strong {{ color: #059669; }}
        .styled-list li:nth-child(4n+3) strong {{ color: #0891B2; }}
        .styled-list li:nth-child(4n+4) strong {{ color: #B45309; }}
        .styled-list li:nth-child(4n+4) strong {{ color: #B45309; }}
        
        /* Heading Cycle */
        .editorial-container section:nth-of-type(4n+1) h2, .editorial-container section:nth-of-type(4n+1) h3 {{ color: #C2410C !important; }}
        .editorial-container section:nth-of-type(4n+2) h2, .editorial-container section:nth-of-type(4n+2) h3 {{ color: #059669 !important; }}
        .editorial-container section:nth-of-type(4n+3) h2, .editorial-container section:nth-of-type(4n+3) h3 {{ color: #0891B2 !important; }}
        .editorial-container section:nth-of-type(4n+4) h2, .editorial-container section:nth-of-type(4n+4) h3 {{ color: #B45309 !important; }}
        .section-header h2::after {{ background: currentColor !important; opacity: 0.5; }}
        .day-header {{ color: inherit !important; }}
        .itinerary-box:nth-child(4n+1) .day-header {{ color: #C2410C !important; }}
        .itinerary-box:nth-child(4n+2) .day-header {{ color: #059669 !important; }}
        .itinerary-box:nth-child(4n+3) .day-header {{ color: #0891B2 !important; }}
        .itinerary-box:nth-child(4n+4) .day-header {{ color: #B45309 !important; }}

        .grid-2 {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 2rem; }}
        .attraction-card {{ background: white; border: 1px solid rgba(0,0,0,0.05); transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.4s ease; height: 100%; display: flex; flex-direction: column; }}
        .attraction-card:hover {{ transform: translateY(-5px); box-shadow: 0 20px 40px rgba(0,0,0,0.06); border-color: rgba(0,0,0,0.0); }}
        .attraction-img-wrapper {{ overflow: hidden; aspect-ratio: 4/3; }}
        .attraction-card img {{ width: 100%; height: 100%; object-fit: cover; transition: transform 1.2s ease; }}
        .attraction-card:hover img {{ transform: scale(1.05); }}
        .attraction-content {{ padding: 2rem; flex-grow: 1; }}
        .attraction-title {{ font-family: var(--font-heading); font-size: 1.3rem; margin-bottom: 0.75rem; color: var(--color-heading); }}
        .attraction-desc {{ font-size: 0.95rem; opacity: 0.8; line-height: 1.6; }}
        .itinerary-box {{ border-left: 1px solid #ddd; margin-left: 1rem; padding: 0 0 2rem 2.5rem; position: relative; }}
        .itinerary-box:last-child {{ padding-bottom: 0; border: none; padding-left: 2.6rem; }}
        .timeline-dot {{ position: absolute; left: -6px; top: 0; width: 11px; height: 11px; background: var(--color-primary); border-radius: 50%; box-shadow: 0 0 0 4px white; }}
        .day-header {{ font-family: var(--font-heading); font-size: 1.2rem; font-weight: 700; color: var(--color-heading); margin-bottom: 0.5rem; display: block; text-transform: uppercase; letter-spacing: 0.1em; color: var(--color-primary); }}
        .editorial-note {{ background-color: #F9F9F9; border-top: 1px solid #000; border-bottom: 1px solid #000; padding: 3rem; margin: 2rem 0; text-align: center; }}
        .editorial-note h3 {{ font-family: var(--font-heading); text-transform: uppercase; letter-spacing: 0.15em; font-size: 0.9rem; margin-bottom: 2rem; color: #888; }}
        .tips-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 2rem; text-align: left; }}
        .tip-item h4 {{ font-size: 1rem; margin-bottom: 0.5rem; color: var(--color-heading); }}
        .tip-item p {{ font-size: 0.9rem; color: #666; }}
        .gallery-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem; margin-top: 2rem; }}
        .gallery-grid img {{ width: 100%; aspect-ratio: 4/3; height: auto; object-fit: cover; transition: opacity 0.3s; }}
        .gallery-grid img:hover {{ opacity: 0.9; }}
        
        .hero-text-bright {{ color: #ffffff; text-shadow: 0 4px 12px rgba(0,0,0,0.6); }}

        @media (max-width: 768px) {{
            .section-header h2 {{ font-size: 2rem; }}
            .lead-text {{ font-size: 1.1rem; }}
            .editorial-container {{ padding: 0 1rem; }}
            .editorial-note {{ padding: 2rem 1rem; }}
        }}
    </style>
</head>
<body>
    <nav>
        <div class="container nav-content">
            <a href="../index.html" class="logo"><img src="../assets/images/logo.png" alt="MyKutch" class="nav-logo"></a>
            <button class="mobile-toggle">☰</button>
            <div class="nav-links">
                <a href="../index.html">Home</a>
                <a href="../index.html#destinations">Destinations</a>
                <a href="../hidden-gems.html">Hidden Gems</a>
                <a href="../blog.html">Blog</a>
                <a href="../history.html">History</a>
                <a href="../landscapes.html">Landscapes</a>
                <a href="../bookings.html">Bookings</a>
                <a href="../about.html">About</a>
            </div>
        </div>
    </nav>

    <header class="destination-hero" style="background-image: url('..{hero_image}'); justify-content: center; text-align: center;">
        <div class="hero-content-inner reveal">
            <h1 class="hero-text-bright">{title.split('—')[0].strip()}</h1>
            <p class="hero-text-bright" style="font-size: 1.2rem; letter-spacing: 0.3em; text-transform: uppercase; font-weight: 500;">{title.split('—')[1].strip() if '—' in title else 'Explore the Unseen'}</p>
        </div>
    </header>

    <main>
        <article class="editorial-container">
            <section class="guide-section reveal" style="margin-top: 4rem;">
                <p class="lead-text">
                    {overview['content'] if overview else 'Overview content unavailable.'}
                </p>
            </section>
            
            <div class="grid-2 reveal">
                <section class="guide-section">
                    <div class="section-header" style="margin-top: 0; margin-bottom: 2rem; text-align: left;"><h2>Who Should Visit</h2></div>
                    <ul class="styled-list">{ "".join([f"<li>{item}</li>" for item in who_visit['list']]) if who_visit and 'list' in who_visit else "<li>Information unavailable</li>" }</ul>
                </section>
                <section class="guide-section">
                    <div class="section-header" style="margin-top: 0; margin-bottom: 2rem; text-align: left;"><h2>How to Reach</h2></div>
                    <ul class="styled-list">{ "".join([f"<li>{item}</li>" for item in how_reach['list']]) if how_reach and 'list' in how_reach else "<li>Information unavailable</li>" }</ul>
                </section>
            </div>

            {attractions_html}
            {tips_html}
            {itinerary_html}

            <section class="guide-section reveal">
                <div class="grid-2">
                    <div>
                         <h3 style="font-size: 1.5rem; margin-bottom: 1.5rem; font-family: var(--font-heading); text-decoration: underline;">Shopping & Bazaars</h3>
                         <ul class="styled-list">{ "".join([f"<li>{item}</li>" for item in markets['list']]) if markets and 'list' in markets else "<li>Check local guides for shopping.</li>" }</ul>
                    </div>
                    <div>
                         <h3 style="font-size: 1.5rem; margin-bottom: 1.5rem; font-family: var(--font-heading); text-decoration: underline;">Local Eats</h3>
                         <ul class="styled-list">{ "".join([f"<li>{item}</li>" for item in food['list']]) if food and 'list' in food else "<li>Check local guides for food.</li>" }</ul>
                    </div>
                </div>
            </section>
            
             { f'''<section class="guide-section reveal" style="background: #fafafa; padding: 2rem; border-radius: 8px;">
                <h3 style="font-family: var(--font-heading); font-size: 1.2rem; margin-bottom: 1rem;">When to Visit</h3>
                <p>{best_time['content']}</p>
            </section>''' if best_time and 'content' in best_time else "" }

            {nearby_html}

            <section class="guide-section reveal">
                 <div class="section-header"><h2>Location & Gallery</h2></div>
                <div style="height: 400px; border-radius: 4px; overflow: hidden; margin-bottom: 2rem; border: 1px solid #eee;">
                    <iframe src="{map_url}" width="100%" height="100%" style="border:0;" allowfullscreen="" loading="lazy"></iframe>
                </div>
                <div class="gallery-grid">
                    { "".join([f'<img src="..{img["src"]}" alt="{img["caption"]}">' for img in gallery]) }
                </div>
            </section>

        </article>
    </main>

    <footer class="footer-main" style="margin-top: 4rem; background: linear-gradient(135deg, #C2410C, #B45309, #059669, #0891B2); color: white; padding: 2.5rem 0;">
        <div class="container">
            <div style="max-width: 900px; margin: 0 auto; text-align: center;">
                <h3 style="color: white; font-family: var(--font-heading); margin-bottom: 0.75rem; font-size: 1.2rem;">About MyKutch.org</h3>
                <p style="opacity: 0.9; line-height: 1.6; margin-bottom: 1.5rem; font-size: 0.9rem;">Showcasing the vibrant culture and heritage of Kutch. Providing authentic insights for every traveler.</p>
                <div style="display: flex; justify-content: center; gap: 2rem; margin-bottom: 1.5rem; flex-wrap: wrap;">
                    <div style="font-size: 0.9rem;">
                        <span style="opacity: 0.8; margin-right: 0.5rem;">Contact:</span>
                        <a href="tel:9825034580" style="color: white; text-decoration: none; font-weight: 500;">+91 98250 34580</a>
                    </div>
                    <div style="font-size: 0.9rem;">
                        <span style="opacity: 0.8; margin-right: 0.5rem;">Email:</span>
                        <a href="mailto:rachh.niraj@gmail.com" style="color: white; text-decoration: none; font-weight: 500;">rachh.niraj@gmail.com</a>
                    </div>
                </div>
                <div style="border-top: 1px solid rgba(255,255,255,0.2); padding-top: 1rem; font-size: 0.85rem; font-weight: 500;">
                    <p>Developed with Love for Kutch by MyKutch.org team</p>
                </div>
            </div>
        </div>
    </footer>
    <script src="../js/script.js"></script>
</body>
</html>
"""
    return html

def create_index_page(destinations):
    # Generates destinations.html in root
    cards_html = ""
    for d in destinations:
        title = d['title'].split('—')[0].strip()
        desc = d['desc']
        slug = d['slug']
        # Remove ../ from hero path for root based page
        img_src = d['image'].replace('../', '') if d['image'].startswith('..') else d['image'].strip()
        # If image starts with /, remove it for relative?
        if img_src.startswith('/'): img_src = img_src[1:]
        
        cards_html += f"""
        <article class="card reveal">
            <div class="card-img-wrapper">
                <img src="{img_src}" alt="{title}">
            </div>
            <div class="card-content">
                <h3>{title}</h3>
                <p style="display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden;">{desc}</p>
                 <div style="margin-top: 1.5rem;">
                    <a href="destinations/{slug}.html" class="btn-text">Explore</a>
                </div>
            </div>
        </article>
        """

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>All Destinations | Kutch Travel</title>
    <link rel="stylesheet" href="css/style.css">
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
    .page-hero {{ 
        height: 50vh; background-image: url('assets/images/overview.webp'); 
        background-size: cover; background-position: center; display: flex; 
        align-items: center; justify-content: center; position: relative; color: white; 
    }}
    .page-hero::before {{ content: ''; position: absolute; inset: 0; background: rgba(0,0,0,0.4); }}
    .hero-title {{ position: relative; z-index: 2; text-align: center; }}
    .hero-title h1 {{ font-size: 3.5rem; margin-bottom: 0.5rem; }}
    </style>
</head>
<body>
    <nav>
        <div class="container nav-content">
            <a href="index.html" class="logo"><img src="assets/images/logo.png" alt="MyKutch" class="nav-logo"></a>
            <div class="nav-links">
                <a href="index.html">Home</a>
                <a href="index.html#destinations">Destinations</a>
                <a href="hidden-gems.html">Hidden Gems</a>
                <a href="blog.html">Blog</a>
                <a href="history.html">History</a>
                <a href="landscapes.html">Landscapes</a>
                <a href="bookings.html">Bookings</a>
                <a href="about.html">About</a>
            </div>
        </div>
    </nav>

    <header class="page-hero">
        <div class="hero-title reveal">
            <h1>All Destinations</h1>
            <p>Explore every corner of Kutch</p>
        </div>
    </header>

    <main class="container">
        <section class="section">
            <div class="grid-3">
                {cards_html}
            </div>
        </section>
    </main>

    <footer class="footer-main" style="margin-top: 5rem; background: linear-gradient(135deg, #C2410C, #B45309, #059669, #0891B2); color: white; padding: 2.5rem 0;">
        <div class="container">
            <div style="max-width: 900px; margin: 0 auto; text-align: center;">
                <h3 style="color: white; font-family: var(--font-heading); margin-bottom: 0.75rem; font-size: 1.2rem;">About MyKutch.org</h3>
                <p style="opacity: 0.9; line-height: 1.6; margin-bottom: 1.5rem; font-size: 0.9rem;">Showcasing the vibrant culture and heritage of Kutch. Providing authentic insights for every traveler.</p>
                <div style="display: flex; justify-content: center; gap: 2rem; margin-bottom: 1.5rem; flex-wrap: wrap;">
                    <div style="font-size: 0.9rem;">
                        <span style="opacity: 0.8; margin-right: 0.5rem;">Contact:</span>
                        <a href="tel:9825034580" style="color: white; text-decoration: none; font-weight: 500;">+91 98250 34580</a>
                    </div>
                    <div style="font-size: 0.9rem;">
                        <span style="opacity: 0.8; margin-right: 0.5rem;">Email:</span>
                        <a href="mailto:rachh.niraj@gmail.com" style="color: white; text-decoration: none; font-weight: 500;">rachh.niraj@gmail.com</a>
                    </div>
                </div>
                <div style="border-top: 1px solid rgba(255,255,255,0.2); padding-top: 1rem; font-size: 0.85rem; font-weight: 500;">
                    <p>Developed with Love for Kutch by MyKutch.org team</p>
                </div>
            </div>
        </div>
    </footer>
    <script src="js/script.js"></script>
</body>
</html>
"""
    with open(os.path.join(ROOT_DIR, "destinations.html"), 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Created {os.path.join(ROOT_DIR, 'destinations.html')}")

def process_file(ts_filename):
    if ts_filename.startswith('_') or ts_filename == 'index.ts': return None
    
    print(f"Processing {ts_filename}...")
    try:
        with open(os.path.join(SOURCE_DIR, ts_filename), 'r', encoding='utf-8') as f:
            content = f.read()
            
        slug_m = RE_SLUG.search(content)
        slug = slug_m.group(1) if slug_m else ts_filename.replace('.ts', '')
        
        title_m = RE_TITLE.search(content)
        title = title_m.group(1) if title_m else slug.title()
        
        hero_m = RE_HERO_IMAGE.search(content)
        hero_raw = hero_m.group(1) if hero_m else ''
        hero = hero_raw.replace('/images/', '/assets/images/') if hero_raw else '../assets/images/default.webp'
        
        map_m = RE_MAP.search(content)
        map_url = map_m.group(1) if map_m else ''
        
        sections = extract_content(content)
        gallery = extract_gallery(content)
        for img in gallery:
            img['src'] = img['src'].replace('/images/', '/assets/images/')

        html = create_html(slug, title, hero, map_url, sections, gallery)
        
        dest_path = os.path.join(DEST_DIR, f"{slug}.html")
        with open(dest_path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"Written {dest_path}")
        
        # Return summary for index page
        overview_sec = next((s for s in sections if "Overview" in s.get('heading', '')), None)
        overview_text = clean_html(overview_sec['content']) if overview_sec and 'content' in overview_sec else "Explore this beautiful destination in Kutch."
        return {
            'title': title,
            'slug': slug,
            'image': hero,
            'desc': overview_text
        }
        
    except Exception as e:
        print(f"Failed to process {ts_filename}: {e}")
        return None

def main():
    if not os.path.exists(DEST_DIR):
        os.makedirs(DEST_DIR)
        
    files = os.listdir(SOURCE_DIR)
    all_destinations = []
    for file in files:
        if file.endswith('.ts'):
            data = process_file(file)
            if data:
                all_destinations.append(data)
                
    create_index_page(all_destinations)

if __name__ == "__main__":
    main()
