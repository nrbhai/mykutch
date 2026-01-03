import re

FILE_PATH = r'c:\website_project\mykutch\site\destinations.html'

def process_html():
    with open(FILE_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    # Pattern to match the whole article card
    # We capture:
    # 1. Everything before the link
    # 2. The URL
    # 3. Everything after the link
    pattern = re.compile(
        r'<article class="card reveal">(.*?)<a href="([^"]+)" class="btn-text stretched-link">Explore</a>(.*?)</article>',
        re.DOTALL
    )

    def replacer(match):
        pre_link_content = match.group(1)
        url = match.group(2)
        post_link_content = match.group(3)
        
        # Construct new HTML
        # Change article -> a
        # Add styles to remove default link styling
        # Change inner a -> span (preserve class btn-text for styling)
        
        new_card = f'<a href="{url}" class="card reveal" style="text-decoration: none; color: inherit;">'
        new_card += pre_link_content
        new_card += '<span class="btn-text">Explore</span>'
        new_card += post_link_content
        new_card += '</a>'
        return new_card

    new_content, count = pattern.subn(replacer, content)

    if count > 0:
        with open(FILE_PATH, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Successfully converted {count} destination cards.")
    else:
        print("No cards matched the pattern. Check regex.")

if __name__ == '__main__':
    process_html()
