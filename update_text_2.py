import os
import re

directory = r"c:\Users\Admin\Desktop\sbbirdnetting"

def process_html_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Add visually hidden text to a.navbar-brand
    # We will insert it right after <a class="navbar-brand" href="...">
    content = re.sub(
        r'(<a class="navbar-brand" href="[^"]*">)(?!\s*<span)',
        r'\1<span class="visually-hidden">SB Bird Netting Solution Home</span>',
        content
    )

    # Add visually hidden text to a.overlayLink
    content = re.sub(
        r'(<a class="overlayLink" href="[^"]*">)(?!\s*<span)',
        r'\1<span class="visually-hidden">View Gallery Image</span>',
        content
    )
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

for filename in os.listdir(directory):
    if filename.endswith('.html'):
        filepath = os.path.join(directory, filename)
        process_html_file(filepath)

print("Text replaced successfully.")
