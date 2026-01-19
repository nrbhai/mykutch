import os
import glob
from datetime import datetime

# Get all HTML files
html_files = []
for root, dirs, files in os.walk('site'):
    # Skip backup directories
    if 'backup' in root or '_backup' in root:
        continue
    for file in files:
        if file.endswith('.html') and not file.endswith('.bak'):
            # Skip template and google verification files
            if '_template' in file or 'google' in file:
                continue
            rel_path = os.path.join(root, file).replace('\\', '/')
            html_files.append(rel_path)

# Sort files
html_files.sort()

# Print all files
for f in html_files:
    print(f)
