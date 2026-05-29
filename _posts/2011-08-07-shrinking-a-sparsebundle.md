---
layout: post
title: "Shrinking a sparsebundle"
date: 2011-08-07 05:57:40 -0800
---

A sparsebundle like many other counter parts in virtual computer environments, does not shrink its size even if you free-up the available space. You need to use hidutil to do it.

```
hdiutil compact /Volumes/Backup/mjhsieh.sparsebundle
```
