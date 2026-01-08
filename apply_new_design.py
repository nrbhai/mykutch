
import os
import re

# Template based on the latest bhuj.html
# I have replaced specific Bhuj content with Placeholders
# and removed data-i18n attributes to allow for fresh re-keying later.

NEW_TEMPLATE = """<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{PAGE_TITLE}</title>
    <meta name="description" content="{META_DESC}">

    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link
        href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=Poppins:wght@400;500;600;700;800&display=swap"
        rel="stylesheet">

    <link rel="stylesheet" href="../css/style.css">

    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-5WQBTM9EPH"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag() { dataLayer.push(arguments); }
        gtag('js', new Date());

        gtag('config', 'G-5WQBTM9EPH');
    </script>

    <style>
        /* Local custom styles removed in favor of global style.css */

        /* Responsive adjustments */
        @media (max-width: 768px) {
            .section-header h2 {
                font-size: 1.5rem !important;
            }

            .lead-text {
                font-size: 1rem;
            }
        }

        .grid-2 {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
            gap: 2rem;
            text-align: left;
        }

        /* Modern Card Design */
        .attraction-card {
            background: white;
            border: none;
            border-radius: 1rem;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            height: 100%;
            display: flex;
            flex-direction: column;
            overflow: hidden;
            text-align: left;
        }

        .attraction-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 12px 30px rgba(0, 0, 0, 0.08);
        }

        .attraction-img-wrapper {
            overflow: hidden;
            aspect-ratio: 4/3;
        }

        .attraction-card img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: transform 1.2s ease;
        }

        .attraction-card:hover img {
            transform: scale(1.05);
        }

        .attraction-content {
            padding: 1.5rem;
            flex-grow: 1;
        }

        .attraction-title {
            font-family: var(--font-heading);
            font-size: 1.15rem;
            margin-bottom: 0.5rem;
            color: #00d26a;
            /* Bright Green */
            font-weight: 600;
            line-height: 1.3;
            border-bottom: 2px solid #FBC02D;
            /* Pale Yellow Underline */
            display: inline-block;
        }

        .attraction-desc {
            font-size: 0.95rem;
            opacity: 0.8;
            line-height: 1.6;
            color: var(--color-text);
        }

        /* Itinerary Grid */
        .itinerary-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 1.5rem;
            margin-top: 1.5rem;
        }

        .itinerary-box {
            background: white;
            padding: 1.5rem;
            border-radius: 1rem;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);
            border: 1px solid rgba(0, 0, 0, 0.03);
            text-align: left;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }

        .itinerary-box:hover {
            transform: translateY(-4px);
            box-shadow: 0 12px 24px rgba(0, 0, 0, 0.08);
            border-color: var(--color-primary);
        }

        .itinerary-box p {
            font-size: 0.95rem;
            line-height: 1.6;
            color: #555;
            margin: 0;
        }

        .day-header {
            font-family: var(--font-heading);
            font-size: 1.15rem;
            /* Unified Subheading Size */
            font-weight: 600;
            color: var(--color-primary);
            margin-bottom: 0.25rem;
            display: block;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        /* Modern Editorial Note */
        .editorial-note {
            background-color: #f8fafc;
            border-radius: 1.5rem;
            padding: 2.5rem;
            margin: 2rem 0;
            text-align: left;
            /* Align Left */
            border: 1px solid rgba(0, 0, 0, 0.03);
        }

        .tips-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 2rem;
            text-align: left;
        }

        .tip-item h4 {
            font-size: 1.15rem;
            /* Unified Subheading Size */
            margin-bottom: 0.5rem;
            color: var(--color-heading);
            font-weight: 600;
        }

        .tip-item p {
            font-size: 0.95rem;
            color: #555;
            line-height: 1.6;
        }

        .styled-list {
            padding-left: 1.2rem;
            margin-bottom: 1.5rem;
        }

        .styled-list li {
            font-size: 0.95rem;
            margin-bottom: 0.75rem;
            color: #444;
            line-height: 1.6;
        }

        .styled-list li strong {
            color: #333;
            border-bottom: 2px solid #E91E63;
            /* Attractive Rose/Pink Underline */
            display: inline-block;
            line-height: 1.2;
            margin-right: 0.3rem;
        }

        .gallery-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1rem;
            margin-top: 2rem;
        }

        .gallery-grid img {
            width: 100%;
            aspect-ratio: 4/3;
            height: auto;
            object-fit: cover;
            border-radius: 0.75rem;
            transition: opacity 0.3s;
        }

        /* Specific section header override if needed */
        .section-header,
        .section-header h2,
        .heading-bright-blue {
            text-align: left !important;
            align-items: flex-start !important;
        }

        .section-header {
            margin-bottom: 2.5rem !important;
            /* Uniform Gap globally */
            margin-top: 0 !important;
            display: flex;
            flex-direction: column;
            align-items: flex-start;
        }

        /* Ensure paragraph under header aligns left too */
        .section-header p {
            text-align: left !important;
            margin-left: 0 !important;
            margin-right: auto !important;
            margin-top: 0.5rem !important;
        }

        .section-header h2,
        .heading-bright-blue {
            font-size: 1.8rem !important;
            /* Lighter Gradient for better text visibility */
            background: linear-gradient(to right, #E1F5FE, #B3E5FC) !important;
            /* Very Dark Blue for high contrast */
            color: #014361 !important;
            padding: 0.5rem 2rem;
            display: inline-block;
            border-radius: 4px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
            margin-bottom: 0 !important;
            font-weight: 700 !important;
            border-right: none;
            /* Accent border on LEFT */
            border-left: 5px solid #0288D1;
            /* Ensure text is on top */
            position: relative;
            z-index: 1;
            /* OVERRIDE GLOBAL STYLE TO FIX VISIBILITY */
            -webkit-background-clip: border-box !important;
            background-clip: border-box !important;
            -webkit-text-fill-color: initial !important;
            animation: none !important;
        }

        /* Override any centering on body/main just in case (though unlikely) */
        main {
            text-align: left;
        }

        .hero-title-metallic-red {
            /* Dark Red Metallic Gradient */
            background: linear-gradient(
                to right,
                #450a0a 0%,   /* Very Dark Red */
                #7f1d1d 20%,  /* Dark Red */
                #fca5a5 50%,  /* Light Red Highlight (Metallic Shine) */
                #7f1d1d 80%,  /* Dark Red */
                #450a0a 100%  /* Very Dark Red */
            );
            background-size: 200% auto;
            color: auto; /* Fallback */
            -webkit-background-clip: text;
            background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: metallicRedShine 4s linear infinite;
            
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            font-size: 2.5rem;
            text-align: center;
            margin-top: 1.5rem;
            margin-bottom: 0;
            display: block;
            line-height: 1.2;
            /* Subtle shadow to lift it off white bg */
            filter: drop-shadow(0 2px 4px rgba(0,0,0,0.2));
        }

        @keyframes metallicRedShine {
            to {
                background-position: 200% center;
            }
        }

        .destination-hero::before {
            background: none !important;
            display: none !important;
        }

        .hero-text-bright {
            color: #ffffff;
            text-shadow: 0 4px 12px rgba(0, 0, 0, 0.6);
        }

        @media (max-width: 768px) {
            .editorial-container {
                padding: 0 1rem;
            }

            .editorial-note {
                padding: 2rem 1.5rem;
            }

            .grid-2 {
                gap: 1.5rem;
                padding-bottom: 1rem;
            }

            .hero-title-metallic-red {
                font-size: 1.4rem;
                /* Smaller for mobile */
                margin-top: 1rem;
                padding: 0 1rem;
            }
        }

        /* Lightbox Styles */
        #lightbox {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.95);
            display: none;
            justify-content: center;
            align-items: center;
            z-index: 10000;
            opacity: 0;
            transition: opacity 0.3s ease;
        }

        #lightbox.show {
            display: flex;
            opacity: 1;
        }

        #lightbox img {
            max-width: 90%;
            max-height: 90vh;
            border-radius: 4px;
            box-shadow: 0 0 30px rgba(0,0,0,0.5);
            transform: scale(0.95);
            transition: transform 0.3s ease;
        }

        #lightbox.show img {
            transform: scale(1);
        }

        .lightbox-close {
            position: absolute;
            top: 20px;
            right: 30px;
            font-size: 2.5rem;
            color: #fff;
            cursor: pointer;
            width: 50px;
            height: 50px;
            text-align: center;
            line-height: 50px;
            background: rgba(255,255,255,0.1);
            border-radius: 50%;
            transition: background 0.2s;
        }

        .lightbox-close:hover {
            background: rgba(255,255,255,0.2);
        }

        .gallery-grid img {
            cursor: pointer;
            transition: transform 0.3s, filter 0.3s;
        }
        
        .gallery-grid img:hover {
            transform: scale(1.02);
            filter: brightness(1.1);
        }
    </style>
</head>

<body>
    <nav>
        <div class="container nav-content">
            <a href="../index.html" class="logo"><img src="../assets/images/logo.png" alt="MyKutch"
                    class="nav-logo"></a>
            <button class="mobile-toggle">☰</button>
            <div class="nav-links">
                <a href="../index.html" data-i18n="nav.home">Home</a>
                <a href="../index.html#destinations" data-i18n="nav.destinations">Destinations</a>
                <a href="../hidden-gems.html" data-i18n="nav.hidden_gems">Hidden Gems</a>
                <a href="../blog.html" data-i18n="nav.blog">Blog</a>
                <a href="../history.html" data-i18n="nav.history">History</a>
                <a href="../landscapes.html" data-i18n="nav.landscapes">Landscapes</a>
                <a href="../bookings.html" data-i18n="nav.bookings">Bookings</a>
                <a href="../about.html" data-i18n="nav.about">About</a>
            </div>
        </div>
    </nav>

    <header class="destination-hero"
        style="background-image: url('../assets/images/{HERO_IMAGE_BASENAME}'); justify-content: center; text-align: center;">
        <div class="hero-content-inner reveal">
        </div>
    </header>

    <div class="container reveal">
        <h1 class="hero-title-metallic-red">{HERO_TITLE}</h1>
    </div>

    <main>
        <article class="editorial-container">
            <section class="guide-section reveal" style="margin-top: 4rem;">
                <p class="lead-text">{LEAD_TEXT}</p>
            </section>

            <div class="grid-2 reveal" style="margin-top: 4rem;">
                <section class="guide-section">
                    <div class="section-header">
                        <h2 class="heading-bright-blue">Who Should Visit</h2>
                    </div>
                    <!-- WHO_VISIT_LIST -->
                    <ul class="styled-list">
                        {WHO_VISIT_LIST}
                    </ul>
                </section>
                <section class="guide-section">
                    <div class="section-header">
                        <h2 class="heading-bright-blue">How to Reach</h2>
                    </div>
                    <!-- HOW_REACH_LIST -->
                    <ul class="styled-list">
                        {HOW_REACH_LIST}
                    </ul>
                </section>
            </div>

            <section class="guide-section reveal">
                <div class="section-header">
                    <h2 class="heading-bright-blue">Landmarks & Heritage</h2>
                    <p style="opacity: 0.6; margin-top: 0.5rem;">The defining monuments</p>
                </div>
                <!-- LANDMARKS_GRID -->
                <div class="grid-2">
                    {LANDMARKS_GRID}
                </div>
            </section>
            <section class="guide-section reveal">
                <div class="editorial-note">
                    <div class="section-header">
                        <h3 class="heading-bright-blue" style="font-family: var(--font-heading);">Curated Local Advice</h3>
                    </div>
                    <!-- TIPS_GRID -->
                    <div class="tips-grid">
                        {TIPS_GRID}
                    </div>
                </div>
            </section>


            <section class="guide-section reveal" style="margin-top: 4rem;">
                <div class="grid-2">
                    <div>
                        <div class="section-header">
                            <h3 class="heading-bright-blue" style="font-family: var(--font-heading);">Shopping & Bazaars</h3>
                        </div>
                        <!-- SHOPPING_LIST -->
                        <ul class="styled-list">
                            {SHOPPING_LIST}
                        </ul>
                    </div>
                    <div>
                        <div class="section-header">
                            <h3 class="heading-bright-blue" style="font-family: var(--font-heading);">Local Eats</h3>
                        </div>
                        <!-- EATS_LIST -->
                        <ul class="styled-list">
                            {EATS_LIST}
                        </ul>
                    </div>
                </div>
            </section>

            <section class="guide-section reveal"
                style="background: #fafafa; padding: 2rem; border-radius: 8px; margin-top: 4rem;">
                <div class="section-header">
                    <h3 class="heading-bright-blue" style="font-family: var(--font-heading);">When to Visit</h3>
                </div>
                <p>{WHEN_VISIT}</p>
            </section>

            <section class="guide-section reveal">
                <div class="section-header">
                    <h2 class="heading-bright-blue">Nearby Places to Visit</h2>
                </div>
                <!-- NEARBY_GRID -->
                <div class="grid-2">
                   {NEARBY_GRID}
                </div>
            </section>

            <section class="guide-section reveal" style="margin-top: 4rem;">
                <div class="section-header">
                    <h2 class="heading-bright-blue">Suggested Itinerary</h2>
                </div>
                <div class="itinerary-grid">
                    {ITINERARY_CONTENT}
                </div>
            </section>

            <section class="guide-section reveal">
                <div class="section-header">
                    <h2 class="heading-bright-blue">Location & Gallery</h2>
                </div>
                <div
                    style="height: 400px; border-radius: 4px; overflow: hidden; margin-bottom: 2rem; border: 1px solid #eee;">
                    {MAP_IFRAME}
                </div>
                <div class="gallery-grid">
                    {GALLERY_IMAGES}
                </div>
            </section>

        </article>
    </main>

    <footer class="footer-main"
        style="background: linear-gradient(135deg, #1e3a8a 0%, #172554 100%); color: white; padding: 4rem 1rem; margin-top: 4rem; position: relative; overflow: hidden;">
        <div class="footer-blob"
            style="position: absolute; width: 500px; height: 500px; background: rgba(30, 58, 138, 0.4); border-radius: 50%; top: -100px; right: -100px; filter: blur(80px); z-index: 1;">
        </div>
        <div class="container"
            style="max-width: 1200px; margin: 0 auto; position: relative; z-index: 5; text-align: left;">
            <div class="footer-grid"
                style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 3rem; align-items: start;">

                <!-- Bio / Brand -->
                <div class="footer-brand">
                    <img src="../assets/images/logo.png" alt="MyKutch Logo"
                        style="height: 60px; margin-bottom: 1.5rem; filter: brightness(100); opacity: 0.9;">
                    <p style="font-size: 0.95rem; opacity: 0.8; line-height: 1.6; margin-bottom: 1.5rem; color: #cbd5e1;"
                        data-i18n="footer.bio"></p>
                    <a href="mailto:contact@mykutch.org"
                        style="color: #60a5fa; font-weight: 600; text-decoration: none; border-bottom: 1px solid rgba(96, 165, 250, 0.3); padding-bottom: 2px;">contact@mykutch.org</a>
                </div>

                <!-- Quick Links -->
                <div class="footer-links">
                    <h4
                        style="font-family: var(--font-heading); font-size: 1.1rem; margin-bottom: 1.5rem; color: #f1f5f9;">
                        Explore</h4>
                    <ul style="list-style: none; padding: 0;">
                        <li style="margin-bottom: 0.8rem;"><a href="../index.html" class="footer-link"
                                style="color: #cbd5e1; text-decoration: none; transition: 0.3s;"
                                data-i18n="nav.home"></a></li>
                        <li style="margin-bottom: 0.8rem;"><a href="../index.html#destinations" class="footer-link"
                                style="color: #cbd5e1; text-decoration: none; transition: 0.3s;"
                                data-i18n="nav.destinations"></a></li>
                        <li style="margin-bottom: 0.8rem;"><a href="../hidden-gems.html" class="footer-link"
                                style="color: #cbd5e1; text-decoration: none; transition: 0.3s;"
                                data-i18n="nav.hidden_gems"></a></li>
                        <li style="margin-bottom: 0.8rem;"><a href="../blog.html" class="footer-link"
                                style="color: #cbd5e1; text-decoration: none; transition: 0.3s;"
                                data-i18n="nav.blog"></a></li>
                    </ul>
                </div>

                <!-- Legal / Credits -->
                <div class="footer-legal">
                    <h4
                        style="font-family: var(--font-heading); font-size: 1.1rem; margin-bottom: 1.5rem; color: #f1f5f9;">
                        Legal</h4>
                    <ul style="list-style: none; padding: 0;">
                        <li style="margin-bottom: 0.8rem;"><a href="#"
                                style="color: #cbd5e1; text-decoration: none; opacity: 0.7;">Privacy Policy</a></li>
                        <li style="margin-bottom: 0.8rem;"><a href="#"
                                style="color: #cbd5e1; text-decoration: none; opacity: 0.7;">Terms of Use</a></li>
                    </ul>
                    <p style="margin-top: 1.5rem; font-size: 0.85rem; opacity: 0.5;">&copy; 2026 MyKutch.org</p>
                </div>
            </div>

            <!-- Developer Credit -->
            <div class="footer-credit" style="margin-top: 4rem; border-top: 1px solid rgba(255,255,255,0.1); padding-top: 2rem; text-align: center;">
                <div style="display: inline-flex; align-items: center; gap: 0.5rem; opacity: 0.7; font-size: 0.9rem;">
                    <span>Created by</span>
                    <strong style="color: #93c5fd; font-weight: 600;">Niraj</strong>
                    <span style="font-size: 1.2rem;">👨‍💻</span>
                    <p data-i18n="footer.dev_credit"></p>
                </div>
            </div>
        </div>
    </footer>
    <!-- Lightbox Structure -->
    <div id="lightbox">
        <span class="lightbox-close">&times;</span>
        <img id="lightbox-img" src="" alt="Full Screen View">
    </div>

    <script src="../js/i18n.js"></script>
    <script src="../js/script.js"></script>
    <script>
        // Gallery Lightbox Logic
        document.addEventListener('DOMContentLoaded', () => {
             const galleryImages = document.querySelectorAll('.gallery-grid img');
             const lightbox = document.getElementById('lightbox');
             const lightboxImg = document.getElementById('lightbox-img');
             const closeBtn = document.querySelector('.lightbox-close');

             if(!lightbox || !galleryImages.length) return;

             // Open Lightbox
             galleryImages.forEach(img => {
                 img.addEventListener('click', () => {
                     lightboxImg.src = img.src;
                     lightboxImg.alt = img.alt || 'Gallery Image';
                     lightbox.classList.add('show');
                     document.body.style.overflow = 'hidden'; // Prevent scrolling
                 });
             });

             // Close Lightbox Function
             const closeLightbox = () => {
                 lightbox.classList.remove('show');
                 document.body.style.overflow = ''; // Restore scrolling
                 setTimeout(() => {
                     lightboxImg.src = ''; // Clear source after animation
                 }, 300);
             };

             // Close on X click
             closeBtn.addEventListener('click', closeLightbox);

             // Close on Background click
             lightbox.addEventListener('click', (e) => {
                 if(e.target === lightbox) closeLightbox();
             });

             // Close on Escape key
             document.addEventListener('keydown', (e) => {
                 if (e.key === 'Escape' && lightbox.classList.contains('show')) {
                     closeLightbox();
                 }
             });
        });
    </script>
</body>

</html>
"""

DESTINATIONS_DIR = r"c:\website_project\mykutch\site\destinations"

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
             # Cleanup extracted content? 
             # remove old style params
             content = match.group(1).strip()
             content = re.sub(r'style="[^"]*"', '', content)
             return content
    return default

def main():
    if not os.path.exists(DESTINATIONS_DIR):
        print("Directory not found")
        return

    for filename in os.listdir(DESTINATIONS_DIR):
        if not filename.endswith(".html"): continue
        if filename == "bhuj.html": continue # Skip the master template source
        
        file_path = os.path.join(DESTINATIONS_DIR, filename)
        print(f"Processing {filename}...")
        
        original_html = read_file(file_path)
        
        # EXTRACT DATA
        # Title
        page_title = extract_content(original_html, [r'<title>(.*?)</title>'], "MyKutch Destination")
        # Meta Desc
        meta_desc = extract_content(original_html, [r'<meta name="description"\s+content="(.*?)">'], "")
        # Hero Image Basename (e.g. bhuj/bhuj1.webp)
        hero_img_full = extract_content(original_html, [r"background-image: url\('([^']+)'\)"], "bhuj/bhuj1.webp")
        # Regex to capture content after 'images/'
        m_img = re.search(r'images/([^"\')]+)', hero_img_full)
        hero_img_basename = m_img.group(1) if m_img else "bhuj/bhuj1.webp"
        
        # Hero Title (Subtitle + Title if old format, or just H1)
        # Old H1 might have class hero-text-bright or hero-title
        # Let's try to grab whatever H1 is in the hero container
        old_h1 = extract_content(original_html, [r'<h1[^>]*>(.*?)</h1>'], "Destination")
        # Clean up tags inside H1 if any
        old_h1 = re.sub(r'<[^>]+>', '', old_h1).strip()
        
        # Lead Text
        lead_text = extract_content(original_html, [r'<p class="lead-text"[^>]*>\s*(.*?)\s*</p>'], "Explore this beautiful destination in Kutch.")
        
        # Lists (Who Visit, Reach, Shopping, Eats)
        # Content usually inside <ul class="styled-list">...</ul>
        # We need identifying headers.
        
        # Who Should Visit
        who_visit = extract_content(original_html, [r'Who Should Visit.*?<ul class="styled-list">(.*?)</ul>'], "<li>Information coming soon...</li>")
        
        # How to Reach
        how_reach = extract_content(original_html, [r'How to Reach.*?<ul class="styled-list">(.*?)</ul>'], "<li>Check local transport options.</li>")
        
        # Shopping
        shopping_list = extract_content(original_html, [r'Shopping & Bazaars.*?<ul class="styled-list">(.*?)</ul>'], "<li>Local markets available.</li>")
        
        # Eats
        eats_list = extract_content(original_html, [r'Local Eats.*?<ul class="styled-list">(.*?)</ul>'], "<li>Local food options available.</li>")
        
        # Landmarks Grid
        # Look for grid-2 after "Landmarks"
        landmarks_grid = extract_content(original_html, [r'Landmarks.*?<div class="grid-2">(.*?)</div>\s*(?:</section>|<section)'], "<!-- Landmarks not found -->")
        
        # Tips Grid
        tips_grid = extract_content(original_html, [r'Curated Local Advice.*?<div class="tips-grid">(.*?)</div>'], "<!-- Tips not found -->")
        
        # When to Visit (P tag)
        when_visit = extract_content(original_html, [r'When to Visit.*?<p[^>]*>(.*?)</p>'], "Best time to visit is winter (Oct-Feb).")
        
        # Nearby Grid
        nearby_grid = extract_content(original_html, [r'Nearby Places to Visit.*?<div class="grid-2">(.*?)</div>'], "<!-- No nearby places listed -->")
        
        # Itinerary Grid (Day columns)
        # Capture inner content of itinerary-grid
        itinerary_content = extract_content(original_html, [r'<div class="itinerary-grid">(.*?)</div>\s*</section>'], "<!-- Itinerary coming soon -->")
        
        # Map Iframe
        map_iframe = ""
        map_src = extract_content(original_html, [r'<iframe\s*src="([^"]+)"'], "")
        if map_src:
            map_iframe = f'<iframe src="{map_src}" width="100%" height="100%" style="border:0;" allowfullscreen="" loading="lazy"></iframe>'
        
        # Gallery Grid
        gallery_images = extract_content(original_html, [r'<div class="gallery-grid">(.*?)</div>'], "")
        
        
        # GENERATE HTML
        html = NEW_TEMPLATE.replace("{PAGE_TITLE}", page_title)
        html = html.replace("{META_DESC}", meta_desc)
        html = html.replace("{HERO_IMAGE_BASENAME}", hero_img_basename)
        html = html.replace("{HERO_TITLE}", old_h1)
        html = html.replace("{LEAD_TEXT}", lead_text)
        html = html.replace("{WHO_VISIT_LIST}", who_visit)
        html = html.replace("{HOW_REACH_LIST}", how_reach)
        html = html.replace("{LANDMARKS_GRID}", landmarks_grid)
        html = html.replace("{TIPS_GRID}", tips_grid)
        html = html.replace("{SHOPPING_LIST}", shopping_list)
        html = html.replace("{EATS_LIST}", eats_list)
        html = html.replace("{WHEN_VISIT}", when_visit)
        html = html.replace("{NEARBY_GRID}", nearby_grid)
        html = html.replace("{ITINERARY_CONTENT}", itinerary_content)
        html = html.replace("{MAP_IFRAME}", map_iframe)
        html = html.replace("{GALLERY_IMAGES}", gallery_images)
        
        write_file(file_path, html)
        print(f"Updated {filename}")

if __name__ == "__main__":
    main()
