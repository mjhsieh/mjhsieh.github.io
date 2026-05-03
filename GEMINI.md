# Mengjuei's Blog (mjhsieh.github.io)

This is a Jekyll-powered blog hosted on GitHub Pages.

## Project Structure

- `_layouts/`: Contains page templates.
  - `archive.html`: Main layout for the index and archive pages.
  - `post.html`: Layout for individual blog posts.
- `_posts/`: Markdown files for blog entries.
- `assets/`: Static assets (CSS, images, PDFs).
- `_includes/`: Reusable HTML snippets (head, custom components).

## Recent Changes

### 2026-05-03: Enhance tools/test.py for Internet Archive Content

- **Change**: Added URL validation for Internet Archive links and implemented image downloading/local path updating functionality in `tools/test.py`.
- **Implementation**:
    - `convert_url_to_jekyll`: Validates input URLs to ensure they match the `https://web.archive.org/web/<time stamp>/http://apple.sysbio.info/~mjhsieh/archives/.*` pattern.
    - `convert_soup_to_jekyll`: Iterates through `<img>` tags, downloads images matching `^https://web.archive.org/web/\d{14}im/http://apple\.sysbio\.info/~mjhsieh/.*$` to `assets/images`, and updates `src` attributes to local paths.



### 2026-05-02: Fix Duplicate Posts on Index Page

- **Issue**: The index page was displaying the first 5 posts as excerpts but then including them again in the bulleted "Rest of the entries" list.
- **Root Cause**: The `offset: 5` filter in `_layouts/archive.html` was not correctly skipping the posts when used with the `assign` tag.
- **Fix**: Replaced `offset: 5` with `slice: 5, site.posts.size` to reliably skip the first 5 entries before grouping the remainder by year.

### 2026-05-02: Update tools/test.py

- **Change**: Refactored `tools/test.py` to accept a URL or local file path as a command-line argument.
- **Implementation**: Used `argparse` for argument parsing and `requests` for fetching remote content. Shared conversion logic between local and remote sources.
