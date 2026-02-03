import os
import re

def clean_styles(match):
    # This function takes a match object for an h1-h6 tag opening
    # e.g. <h3 class="..." style="color:red; margin:0">
    full_tag = match.group(0)
    
    def repl_style(style_match):
        style_content = style_match.group(1)
        # Remove color: ... ;?
        # We need to be careful not to remove background-color, border-color etc.
        # Regex: (?<!-)\bcolor:\s*[^;"]+;?
        # (?<!-) ensures we don't match background-color
        cleaned_style = re.sub(r'(?<!-)\bcolor:\s*[^;"]+;?', '', style_content)
        # Clean up double semicolons or trailing spaces if any left (optional polish)
        cleaned_style = cleaned_style.replace(';;', ';').strip()
        return f'style="{cleaned_style}"'

    new_tag = re.sub(r'style="([^"]*)"', repl_style, full_tag, flags=re.IGNORECASE)
    return new_tag

def process_files():
    files_modified = 0
    # Walk through site directory
    for root, dirs, files in os.walk('site'):
        for file in files:
            if file.endswith('.html'):
                path = os.path.join(root, file)
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Regex to match <h1 ... > taking into account possible newlines
                    # <h[1-6] followed by whitespace, then anything until >
                    # Using DOTALL so . matches newlines
                    pattern = r'<h[1-6]\s+[^>]*>'
                    
                    new_content = re.sub(pattern, clean_styles, content, flags=re.DOTALL | re.IGNORECASE)
                    
                    if new_content != content:
                        with open(path, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        print(f"Modified: {path}")
                        files_modified += 1
                except Exception as e:
                    print(f"Error processing {path}: {e}")
    
    print(f"Total files modified: {files_modified}")

if __name__ == "__main__":
    process_files()
