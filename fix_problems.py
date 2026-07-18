import os
import re

directory = r"c:\Users\Admin\Desktop\sbbirdnetting"

def process_html_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Revert span in navbar-brand and add aria-label to the anchor, and alt to image
    # The span was: <span class="visually-hidden">SB Bird Netting Solution Home</span>
    content = content.replace('<span class="visually-hidden">SB Bird Netting Solution Home</span>', '')
    
    # Add aria-label to navbar-brand anchor if not exists
    content = re.sub(
        r'(<a class="navbar-brand")(\s+href="[^"]*">)',
        r'\1 aria-label="SB Bird Netting Solution Home"\2',
        content
    )
    # Add alt text to the logo image inside navbar-brand
    content = content.replace('<img src="image/Brand_Logo.png" alt="">', '<img src="image/Brand_Logo.png" alt="SB Bird Netting Solution Logo">')

    # 2. Revert span in overlayLink and add aria-label
    # The span was: <span class="visually-hidden">View Gallery Image</span>
    content = content.replace('<span class="visually-hidden">View Gallery Image</span>', '')
    
    # Add aria-label to overlayLink anchor if not exists
    content = re.sub(
        r'(<a class="overlayLink")(\s+href="[^"]*">)',
        r'\1 aria-label="View Gallery Image"\2',
        content
    )
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

for filename in os.listdir(directory):
    if filename.endswith('.html'):
        filepath = os.path.join(directory, filename)
        process_html_file(filepath)

print("Problems fixed successfully.")
