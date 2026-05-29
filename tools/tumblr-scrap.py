import os
import re
import argparse
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from markdownify import markdownify as md
from pathlib import Path
import json

def convert_soup_to_jekyll(soup, url):
    # 0. Setup Paths
    script_path = Path(__file__).resolve()
    posts_path = Path(script_path.parent.parent / "_posts").resolve()
    images_path = Path(script_path.parent.parent / "assets/images").resolve()
    images_path.mkdir(parents=True, exist_ok=True)

    # 1. Extract Title
    # Tumblr titles are often in <h1 class="title"> or inferred from content
    title_element = soup.find('h1', class_='title') or soup.find('h2', class_='title')
    if title_element:
        raw_title = title_element.get_text(strip=True)
    else:
        # Fallback to OpenGraph title or a default
        og_title = soup.find('meta', property='og:title')
        raw_title = og_title['content'] if og_title else "Untitled Tumblr Post"

    # 2. Extract Date
    # Tumblr often has date in <meta property="og:updated_time"> or script tags.
    # For simplicity in this scrap script, we'll try to find common Tumblr date patterns 
    # or use current date as fallback if not found in meta.
    date_meta = soup.find('meta', property='article:published_time')
    if date_meta:
        # Format usually: 2024-04-26T...
        dt_obj = datetime.fromisoformat(date_meta['content'].replace('Z', '+00:00'))
        date_str = dt_obj.strftime("%Y-%m-%d")
        time_str = dt_obj.strftime("%H:%M:%S")
    else:
        ldjson_script = soup.find('script', type='application/ld+json')
        datePublished = json.loads(ldjson_script.string)['datePublished']

    if datePublished:
        # Format usually: 2024-04-26T...
        dt_obj = datetime.fromisoformat(datePublished.replace('Z', '+00:00'))
        date_str = dt_obj.strftime("%Y-%m-%d")
        time_str = dt_obj.strftime("%H:%M:%S")
    else:
        date_str = datetime.now().strftime("%Y-%m-%d")
        time_str = datetime.now().strftime("%H:%M:%S")

    # 3. Extract Content
    # Main content in Tumblr is often in <div class="post">, <div class="body">, or <article>
    content_div = soup.find('article') or soup.find('div', class_='post') or soup.find('div', class_='body')
    
    if content_div:
        # Clean up unwanted elements (like date/type paragraphs that might be redundant)
        for p_tag in content_div.find_all('p', class_=('date', 'type')):
            p_tag.decompose()

        # Remove anchor links from <h2> tags but keep the text
        for h2_tag in content_div.find_all('h2'):
            for a_tag in h2_tag.find_all('a'):
                a_tag.unwrap()
        
        # Download and replace images
        for img in content_div.find_all('img'):
            img_src = img.get('src')
            if img_src and ('tumblr.com' in img_src or 'static.tumblr.com' in img_src):
                try:
                    # Generate a name based on the URL to avoid collisions
                    img_name = os.path.basename(img_src.split('?')[0])
                    if not img_name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
                        img_name += ".jpg" # Default extension
                        
                    local_img_path = images_path / img_name
                    
                    if not local_img_path.exists():
                        img_data = requests.get(img_src, headers={'User-Agent': 'Mozilla/5.0'}, stream=True)
                        img_data.raise_for_status()
                        with open(local_img_path, 'wb') as handler:
                            for chunk in img_data.iter_content(chunk_size=8192):
                                handler.write(chunk)
                        print(f"Downloaded image: {local_img_path}")
                    
                    img.attrs['src'] = f"/assets/images/{img_name}"
                except Exception as e:
                    print(f"Error downloading image {img_src}: {e}")

        markdown_body = md(str(content_div), heading_style="ATX").strip()
    else:
        markdown_body = "No content found."

    # 4. Generate Filename
    slug = re.sub(r'[^a-z0-9]+', '-', raw_title.lower()).strip('-')
    if not slug:
        slug = "tumblr-post"
    filename = f"{posts_path}/{date_str}-{slug}.md"

    # 5. Construct Jekyll Output
    jekyll_content = f"""---
layout: post
title: "{raw_title}"
date: {date_str} {time_str} -0800
---

{markdown_body}
"""

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(jekyll_content)

    print(f"Converted: {filename}")

def convert_url_to_jekyll(url):
    # Validation for Tumblr URL
    if not re.match(r"^https://[a-zA-Z0-9-]+\.tumblr\.com/post/\d+.*$", url):
        print(f"Error: URL '{url}' does not match the required Tumblr post pattern.")
        return

    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        convert_soup_to_jekyll(soup, url)
    except Exception as e:
        print(f"Error fetching {url}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert Tumblr post to Jekyll post.")
    parser.add_argument("url", help="The Tumblr post URL to convert.")
    args = parser.parse_args()

    convert_url_to_jekyll(args.url)
