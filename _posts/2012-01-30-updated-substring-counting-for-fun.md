---
layout: post
title: "(updated) substring counting for fun..."
date: 2012-01-30 08:10:00 -0800
---

Now it’s even slower, I was about to write down a fortran version, but index() intrinsic is not very fast, either…. (By the way, unicode is slow.)

```
bash-3.2$ /usr/bin/time -p bin/count.occurrence.py 測試
測試    819
real        11.51
user        11.27
sys          0.16
bash-3.2$ /usr/bin/time -p bin/count.occurrence.pl 測試 < /Volumes/ramdisk/newTEXT.txt
測試    819
real         0.88
user         0.83
sys          0.04
bash-3.2$ /usr/bin/time -p gawk -F 測試 '{s=s+NF-1}END{print FS"        "s}' /Volumes/ramdisk/newTEXT.txt
測試    819
real         1.28
user         1.22
sys          0.05
bash-3.2$ /usr/bin/time -p bin/count.occurrence2.py 測試
測試    819
real         1.40
user         1.36
sys          0.04
```

The code for python counter1:

```
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import codecs
import sys
uquery=unicode(sys.argv[1],"utf-8")
myCount=0
f = codecs.open('/Volumes/ramdisk/newTEXT.txt', encoding='utf-8')
for line in f:
    myCount=myCount+line.count(uquery)
print myCount
```

The code for python counter2

```
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
myCount=0
f = open('/Volumes/ramdisk/newTEXT.txt')
for line in f:
    myCount=myCount+line.count(sys.argv[1])
print myCount
```
