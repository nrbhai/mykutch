import os
import re

# Configuration
SITE_ROOT = r'c:\website_project\mykutch\site'
FOOTER_TEMPLATE = """<footer class="footer-main" style="margin-top: 2rem; background: linear-gradient(135deg, #F8FAFC, #E0F2FE, #BAE6FD); color: var(--color-heading); padding: 2.5rem 0; border-top: 1px solid rgba(0,0,0,0.05);">
    <div class="container">
        <div style="max-width: 900px; margin: 0 auto; text-align: center;">
            <img src="{ASSETS_PREFIX}assets/images/logo.png" alt="MyKutch Logo" style="height: 130px; margin-bottom: 1rem; opacity: 0.9;">
            <h3 style="color: var(--color-heading); font-family: var(--font-heading); margin-bottom: 0.5rem; font-size: 1.1rem; letter-spacing: 0.05em;">About MyKutch.org</h3>
            <p style="opacity: 0.8; line-height: 1.4; margin-bottom: 1rem; font-size: 0.9rem; max-width: 600px; margin-left: auto; margin-right: auto;">Showcasing the vibrant culture and heritage of Kutch. Providing authentic insights for every traveler.</p>
            <div style="display: flex; justify-content: center; gap: 1.5rem; margin-bottom: 1.5rem; flex-wrap: wrap;">
                <div style="font-size: 0.85rem;">
                    <span style="opacity: 0.7; margin-right: 0.3rem;">Contact:</span>
                    <a href="tel:9825034580" style="color: var(--color-primary); text-decoration: none; font-weight: 600;">+91 98250 34580</a>
                </div>
                <div style="font-size: 0.85rem;">
                    <span style="opacity: 0.7; margin-right: 0.3rem;">Email:</span>
                    <a href="mailto:info@mykutch.org" style="color: var(--color-primary); text-decoration: none; font-weight: 600;">info@mykutch.org</a>
                </div>
            </div>
            <div style="border-top: 1px solid rgba(0,0,0,0.05); padding-top: 1rem; font-size: 0.8rem; font-weight: 500; opacity: 0.6;">
                <p>Developed with Love for Kutch by MyKutch.org team</p>
            </div>
        </div>
    </div>
</footer>"""

def update_footers():
    count = 0
    print(f"Scanning {SITE_ROOT}...")
    
    for root, dirs, files in os.walk(SITE_ROOT):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                
                # Calculate relative path depth
                rel_path = os.path.relpath(root, SITE_ROOT)
                if rel_path == '.':
                    assets_prefix = ''
                else:
                    # e.g., 'destinations' -> 1 level -> '../'
                    depth = len(rel_path.split(os.sep))
                    assets_prefix = '../' * depth
                
                # Prepare replacement
                new_footer = FOOTER_TEMPLATE.replace('{ASSETS_PREFIX}', assets_prefix)
                
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Regex replace
                # This matches <footer class="footer-main" ... </footer> across multiple lines
                pattern = re.compile(r'<footer class="footer-main".*?</footer>', re.DOTALL | re.IGNORECASE)
                
                if pattern.search(content):
                    new_content = pattern.sub(new_footer, content)
                    if new_content != content:
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        print(f"Updated: {file} (Prefix: '{assets_prefix}')")
                        count += 1
                    else:
                        print(f"Skipped (No Change): {file}")
                else:
                    print(f"Skipped (No Footer Found): {file}")

    print(f"\nTotal files updated: {count}")

if __name__ == '__main__':
    update_footers()
