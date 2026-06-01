---
layout: post
title: "XOR as a logical operator in FORTRAN"
date: 2010-06-20 08:58:18 -0800
---

If I recall it right, XOR operator simply is not included in the FORTRAN 9x standard nor FORTRAN 2003 either. However some compilers like XLF and g77 do have it and people have been using this slang for quite some time. Luckily most FORTRAN compilers come with a intrinsic logical XOR(p,q) function that can be use as an equivalent in the condition arguments. You can rewrite it from (p .XOR. q) to (XOR(p,q).
