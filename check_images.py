import re
import os

with open('destinations.html', 'r', encoding='utf-8') as f:
    content = f.read()

images = re.findall(r'<img [^>]*src="([^"]+)"', content)
images += re.findall(r'background-image:\s*url\(\'([^\']+)\'\)', content)

for img in images:
    if os.path.exists(img):
        print(f"EXISTS: {img}")
    else:
        print(f"MISSING: {img}")
