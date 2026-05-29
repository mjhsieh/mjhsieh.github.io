---
layout: post
title: "ceiling() in AWK."
date: 2011-05-15 22:23:00 -0800
---

Surprisingly easy:

$ awk '**function ceiling(x){return ((x > int(x)) ? int(x)+1 : int(x))}**END{print ceiling(NR/2)}' oneword\_all.list
