import re
import os

def check_file(filename):
    print(f"--- Checking {filename} ---")
    if not os.path.exists(filename):
        print(f"FILE NOT FOUND: {filename}")
        return

    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    images = re.findall(r'<img [^>]*src="([^"]+)"', content)
    images += re.findall(r'background-image:\s*url\(\'([^\']+)\'\)', content)
    images += re.findall(r'url\("([^"]+)"\)', content)

    for img in set(images):
        # skip external URLs and template placeholders like ${item.src}
        if img.startswith('http') or img.startswith('//') or '${' in img:
            continue
        if os.path.exists(img):
            pass
        else:
            print(f"MISSING: {img}")

check_file('index.html')
check_file('destinations.html')
check_file('about.html')
check_file('history.html')
check_file('landscapes.html')
