import os
import re

file_path = r'c:\website_project\mykutch\site\index.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

imgs = re.findall(r'src=["\'](.*?)["\']', content)
# Also check for background-image in style
bg_imgs = re.findall(r'url\(["\']?(.*?)["\']?\)', content)
for img in imgs + bg_imgs:
    if img.startswith('http'): continue
    full_path = os.path.join(r'c:\website_project\mykutch\site', img.replace('/', os.sep))
    if not os.path.exists(full_path):
        print(f"Missing: {img}")
    else:
        print(f"OK: {img}")
