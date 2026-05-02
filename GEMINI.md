# Mengjuei's Blog (mjhsieh.github.io)

This is a Jekyll-powered blog hosted on GitHub Pages. Gemini contributes to
feature implementation, bug fixes, and records necessary infomation into the
GEMINI.md file.

## Project Structure

- `_layouts/`: Contains page templates.
  - `archive.html`: Main layout for the index and archive pages.
  - `post.html`: Layout for individual blog posts.
- `_posts/`: Markdown files for blog entries.
- `assets/`: Static assets (CSS, images, PDFs).
- `_includes/`: Reusable HTML snippets (head, custom components).

## Recent Changes

### 2026-05-02: Fix Duplicate Posts on Index Page

- **Issue**: The index page was displaying the first 5 posts as excerpts but then including them again in the bulleted "Rest of the entries" list.
- **Root Cause**: The `offset: 5` filter in `_layouts/archive.html` was not correctly skipping the posts when used with the `assign` tag.
- **Fix**: Replaced `offset: 5` with `slice: 5, site.posts.size` to reliably skip the first 5 entries before grouping the remainder by year.
