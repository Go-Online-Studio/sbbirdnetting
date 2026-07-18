import os
import re

directory = r"c:\Users\Admin\Desktop\sbbirdnetting"

def process_html_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update social links in footer
    # Facebook
    content = re.sub(
        r'<a class="facebook" aria-label="Facebook" href="([^"]+)"><i class="([^"]+)"></i></a>',
        r'<a class="facebook" href="\1"><span class="visually-hidden">SB Bird Netting Facebook Page</span><i class="\2"></i></a>',
        content
    )
    # Instagram
    content = re.sub(
        r'<a class="instagram" aria-label="Instagram" href="([^"]+)"><i class="([^"]+)"></i></a>',
        r'<a class="instagram" href="\1"><span class="visually-hidden">SB Bird Netting Instagram Profile</span><i class="\2"></i></a>',
        content
    )
    # WhatsApp
    content = re.sub(
        r'<a class="whatsapp" aria-label="WhatsApp" href="([^"]+)"><i class="([^"]+)"></i></a>',
        r'<a class="whatsapp" href="\1"><span class="visually-hidden">Message SB Bird Netting on WhatsApp</span><i class="\2"></i></a>',
        content
    )

    # 2. Update FAB links to use visually-hidden instead of sr-only and provide descriptive text
    content = content.replace('<span class="sr-only">Whatsapp</span>', '<span class="visually-hidden">Message SB Bird Netting on WhatsApp</span>')
    content = content.replace('<span class="sr-only">Call</span>', '<span class="visually-hidden">Call SB Bird Netting Now</span>')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

for filename in os.listdir(directory):
    if filename.endswith('.html'):
        filepath = os.path.join(directory, filename)
        process_html_file(filepath)

print("Text replaced successfully.")
