---
layout: post
title: "GNU Env Modules and prepend-path"
date: 2024-04-26 18:42:07 -0800
---

Today I learned that prepend-path doesn’t modify $PATH if the path you want to prepend already exists in the $PATH. See <https://modules.readthedocs.io/en/latest/modulefile.html#mfcmd-prepend-path>
