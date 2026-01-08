import os
import re
from urllib.parse import unquote

SITE_ROOT = r'c:\website_project\mykutch\site'
REPORT_FILE = r'c:\website_project\mykutch\missing_images_report.txt'

def find_html_files(root_dir):
    html_files = []
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
    return html_files

def extract_image_paths(html_content):
    paths = []
    # Find <img src="...">
    img_tags = re.finditer(r'<img[^>]+src=["\']([^"\']+)["\']', html_content, re.IGNORECASE)
    for match in img_tags:
        paths.append({'type': 'img', 'url': match.group(1), 'context': '<img> tag'})
    
    # Find background-image: url(...)
    bg_images = re.finditer(r'url\([\'"]?([^\'"\)]+)[\'"]?\)', html_content, re.IGNORECASE)
    for match in bg_images:
        path = match.group(1)
        # Skip data URIs or external links if needed (though we mostly care about local)
        if not path.startswith('data:') and not path.startswith('http'):
             paths.append({'type': 'bg', 'url': path, 'context': 'background-image'})

    # Find <link rel="preload" as="image" href="...">
    preloads = re.finditer(r'<link[^>]+rel=["\']preload["\'][^>]+as=["\']image["\'][^>]+href=["\']([^"\']+)["\']', html_content, re.IGNORECASE)
    for match in preloads:
        paths.append({'type': 'preload', 'url': match.group(1), 'context': 'preload link'})
        
    # Also check reversed order attributes for preload
    preloads_rev = re.finditer(r'<link[^>]+href=["\']([^"\']+)["\'][^>]+rel=["\']preload["\'][^>]+as=["\']image["\']', html_content, re.IGNORECASE)
    for match in preloads_rev:
         paths.append({'type': 'preload', 'url': match.group(1), 'context': 'preload link'})

    return paths

def resolve_path(html_file_path, image_url):
    # Ignore external links
    if image_url.startswith('http') or image_url.startswith('//'):
        return None

    # Decode URL (e.g. %20 -> space)
    image_url = unquote(image_url)
    
    # Remove query params or anchors
    image_url = image_url.split('?')[0].split('#')[0]

    absolute_path = ''
    if image_url.startswith('/'):
        # Root relative
        absolute_path = os.path.join(SITE_ROOT, image_url.lstrip('/'))
    else:
        # Relative to current file
        absolute_path = os.path.join(os.path.dirname(html_file_path), image_url)
    
    return os.path.normpath(absolute_path)

def main():
    print(f"Scanning for missing images in {SITE_ROOT}...")
    html_files = find_html_files(SITE_ROOT)
    missing_images = []

    for file_path in html_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            images = extract_image_paths(content)
            
            for img in images:
                resolved_path = resolve_path(file_path, img['url'])
                if resolved_path:
                    if not os.path.exists(resolved_path):
                         # Get relative path for report
                         rel_html = os.path.relpath(file_path, SITE_ROOT)
                         missing_images.append({
                             'page': rel_html,
                             'url': img['url'],
                             'expected_loc': resolved_path,
                             'context': img['context']
                         })
        except Exception as e:
            print(f"Error reading {file_path}: {e}")

    # Write Report
    with open(REPORT_FILE, 'w', encoding='utf-8') as f:
        f.write("MISSING IMAGES REPORT\n")
        f.write("=====================\n\n")
        
        if not missing_images:
            f.write("No missing images found! Great job.")
        else:
            current_page = None
            for item in missing_images:
                if item['page'] != current_page:
                    f.write(f"\nPAGE: {item['page']}\n")
                    f.write("-" * (len(item['page']) + 6) + "\n")
                    current_page = item['page']
                
                f.write(f"  [MISSING] {item['url']}\n")
                f.write(f"    Context: {item['context']}\n")
                f.write(f"    Expected at: {item['expected_loc']}\n")

    print(f"Scan complete. Found {len(missing_images)} missing references.")
    print(f"Report saved to {REPORT_FILE}")

if __name__ == "__main__":
    main()
