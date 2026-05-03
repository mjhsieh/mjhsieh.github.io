---
title: notes about curl loop
date: 2026-05-03 10:34:00 -0800
---
Just in case I don't remember this:

To make curl download 200 images but not faster than 14 transfers per minute, we could:
```
curl --rate 14/m -O https://example.com/[1-200].jpg
```
