import os
import re
import json

directory = r"c:\Users\Admin\Desktop\sbbirdnetting"

def process_html_file(filepath, filename):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Fix Canonical URL
    if filename == 'index.html':
        canonical_url = "https://www.sbbirdnetting.com/"
    else:
        canonical_url = f"https://www.sbbirdnetting.com/{filename}"
    
    # Replace existing canonical
    content = re.sub(r'<link\s+rel="canonical"\s+href="[^"]*"\s*/?>', f'<link rel="canonical" href="{canonical_url}" />', content)

    # 2. Fix H1s in index.html
    if filename == 'index.html':
        # Change slider h1s to h2s specifically in the banner
        content = content.replace('<h1 class="display-3">\n                    <a href="invisibleGrills.html">Invisible Grills</a>\n                    </h1>', '<h2 class="display-3">\n                    <a href="invisibleGrills.html">Invisible Grills</a>\n                    </h2>')
        content = content.replace('<h1 class="display-3">\n                    <a href="birdNet_Spikes.html">Bird Net / Spikes</a>\n                    </h1>', '<h2 class="display-3">\n                    <a href="birdNet_Spikes.html">Bird Net / Spikes</a>\n                    </h2>')
        
        # Change specific h2 to h1
        content = content.replace('<h2 class="secH">\n      Building Trust In Our Services Since <strong>2007</strong>\n      </h2>', '<h1 class="secH" style="font-size: 32px;">\n      Building Trust In Our Services Since <strong>2007</strong>\n      </h1>')

    # 3. Add aria-labels to social links
    content = content.replace('<a class="facebook" href', '<a class="facebook" aria-label="Facebook" href')
    content = content.replace('<a class="instagram" href', '<a class="instagram" aria-label="Instagram" href')
    content = content.replace('<a class="whatsapp" href', '<a class="whatsapp" aria-label="WhatsApp" href')

    # 4. Lazy load images (exclude Brand_Logo)
    # Simple regex to add loading="lazy" if not present
    def lazy_load_replacer(match):
        img_tag = match.group(0)
        if 'loading=' in img_tag or 'Brand_Logo' in img_tag or 'Favicon' in img_tag or 'Banner' in img_tag or 'BrandLogoFooter' in img_tag:
            return img_tag
        if img_tag.endswith('/>'):
            return img_tag[:-2] + ' loading="lazy" />'
        elif img_tag.endswith('>'):
            return img_tag[:-1] + ' loading="lazy" >'
        return img_tag

    content = re.sub(r'<img\s+[^>]+>', lazy_load_replacer, content)
    
    # 5. Fix JSON-LD in index.html
    if filename == 'index.html' and '"@type": "LocalBusiness"' in content:
        # We will inject opening hours and geo
        geo_hours = """,
      "geo": {
        "@type": "GeoCoordinates",
        "latitude": 22.3072,
        "longitude": 73.1812
      },
      "openingHoursSpecification": {
        "@type": "OpeningHoursSpecification",
        "dayOfWeek": [
          "Monday",
          "Tuesday",
          "Wednesday",
          "Thursday",
          "Friday",
          "Saturday"
        ],
        "opens": "09:00",
        "closes": "19:00"
      }"""
        content = content.replace('"url": "https://www.sbbirdnetting.com/"\n    }', '"url": "https://www.sbbirdnetting.com/"' + geo_hours + '\n    }')

    # 6. Add Schema Breadcrumbs to subpages
    if filename not in ['index.html']:
        # if not already containing schema
        if '<script type="application/ld+json">' not in content:
            # We insert breadcrumb before </head>
            title_match = re.search(r'<title>(.*?)</title>', content)
            title = title_match.group(1).split('|')[0].strip() if title_match else filename.replace('.html', '')
            breadcrumb_schema = f"""
    <!-- JSON-LD Breadcrumbs -->
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "BreadcrumbList",
      "itemListElement": [
        {{
          "@type": "ListItem",
          "position": 1,
          "name": "Home",
          "item": "https://www.sbbirdnetting.com/"
        }},
        {{
          "@type": "ListItem",
          "position": 2,
          "name": "{title}",
          "item": "{canonical_url}"
        }}
      ]
    }}
    </script>"""
            content = content.replace('</head>', breadcrumb_schema + '\n  </head>')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)


for filename in os.listdir(directory):
    if filename.endswith('.html'):
        filepath = os.path.join(directory, filename)
        process_html_file(filepath, filename)

print("HTML files processed successfully.")
