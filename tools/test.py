import os
import re
import sys
import argparse
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from markdownify import markdownify as md

def convert_soup_to_jekyll(soup):
    # 0. Get the full path to the script file
    from pathlib import Path
    script_path = Path(__file__).resolve()
    posts_path = Path(os.path.dirname(script_path) + "/../_posts").resolve()
    # 1. Extract Title
    # The title is within <h3 class="title">, but often includes category links
    title_element = soup.find('h3', class_='title')
    if title_element:
        # Get text only, ignoring nested <a> tags for categories
        raw_title = title_element.get_text(strip=True).split('::')[-1].strip()
    else:
        raw_title = "Untitled Post"

    # 2. Extract Date from <span class="posted">
    # Format in HTML: "By mjhsieh at December 10, 2002 04:28 PM"
    posted_span = soup.find('span', class_='posted')
    date_str = "2002-12-10" # Default fallback
    time_str = "00:00:00"

    if posted_span:
        match = re.search(r'([A-Za-z]+ {1,2}\d{1,2}, \d{4}) (\d{2}:\d{2} [APM]{2})', posted_span.text)
        if match:
            date_raw = match.group(1)
            time_raw = match.group(2)
            dt_obj = datetime.strptime(f"{date_raw} {time_raw}", "%B %d, %Y %I:%M %p")
            date_str = dt_obj.strftime("%Y-%m-%d")
            time_str = dt_obj.strftime("%H:%M:%S")

    # 3. Extract Content
    # The main text is in <div class="blogbody">
    content_div = soup.find('div', class_='blogbody')
    if content_div:
        # Strip out the title and footer span so they don't appear in the body
        if content_div.find('h3', class_='title'):
            content_div.find('h3', class_='title').decompose()
        if content_div.find('span', class_='posted'):
            content_div.find('span', class_='posted').decompose()

        # Download and replace image URLs
        for img in content_div.find_all('img'):
            img_src = img.get('src')
            archive_image_url_pattern = re.compile(r"^/web/\d{14}im_/http://apple\.sysbio\.info/~mjhsieh/.*$")
            if img_src and archive_image_url_pattern.match(img_src):
                try:
                    img_name = os.path.basename(img_src.split('/')[-1].split('?')[0])
                    local_img_path = images_path / img_name

                    if not local_img_path.exists():
                        img_data = requests.get(f"https://web.archive.org{img_src}", headers={'User-Agent': 'Mozilla/5.0'}, stream=True)
                        img_data.raise_for_status()
                        with open(local_img_path, 'wb') as handler:
                            for chunk in img_data.iter_content(chunk_size=8192):
                                handler.write(chunk)
                        print(f"Downloaded image: {local_img_path}")

                    img.attrs['src'] = f"/assets/images/{img_name}" # Update src to local path
                except requests.exceptions.RequestException as e:
                    print(f"Error downloading image {img_src}: {e}")
                except Exception as e:
                    print(f"An unexpected error occurred while processing image {img_src}: {e}")
            else:
                print(f"Skipping {img_src}")

        markdown_body = md(str(content_div), heading_style="ATX").strip()
    else:
        markdown_body = "No content found."

    # 4. Generate Filename
    slug = re.sub(r'[^a-z0-9]+', '-', raw_title.lower()).strip('-')
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

def convert_local_html_to_jekyll(file_path):
    if not os.path.exists(file_path):
        print(f"File {file_path} not found.")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    convert_soup_to_jekyll(soup)

def convert_url_to_jekyll(url):
    # Regex to match the desired Internet Archive URL pattern
    archive_url_pattern = re.compile(r"^https://web.archive.org/web/\d{14}/http://apple\.sysbio\.info/~mjhsieh/archives/.*$")

    if not archive_url_pattern.match(url):
        print(f"Error: URL '{url}' does not match the required Internet Archive pattern.")
        return

    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        convert_soup_to_jekyll(soup)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert HTML (file or URL) to Jekyll post.")
    parser.add_argument("input", help="The local HTML file or URL to convert.")
    args = parser.parse_args()

    if args.input.startswith("http://") or args.input.startswith("https://"):
        convert_url_to_jekyll(args.input)
    else:
        convert_local_html_to_jekyll(args.input)
