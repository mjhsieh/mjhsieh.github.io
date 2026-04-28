import os
import re
from datetime import datetime
from bs4 import BeautifulSoup
from markdownify import markdownify as md

def convert_local_html_to_jekyll(file_path):
    if not os.path.exists(file_path):
        print(f"File {file_path} not found.")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

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
        match = re.search(r'([A-Za-z]+ \d{1,2}, \d{4}) (\d{2}:\d{2} [APM]{2})', posted_span.text)
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

        markdown_body = md(str(content_div), heading_style="ATX").strip()
    else:
        markdown_body = "No content found."

    # 4. Generate Filename
    slug = re.sub(r'[^a-z0-9]+', '-', raw_title.lower()).strip('-')
    filename = f"{date_str}-{slug}.md"

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

if __name__ == "__main__":
    convert_local_html_to_jekyll("input.html")
