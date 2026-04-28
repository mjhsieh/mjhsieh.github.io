---
layout: post
title: "A csh loop to wget files"
date: 2002-12-10 00:00:00 -0800
---

Well, in case I forget how to write csh script...  
  
This is about writting while loop in csh, can be used to do anything good or something bad....

```
#!/bin/csh

set j = 101
while ( $j > 1 )
   @ j-- 
   set number=`echo $j | awk '{printf("%3d",$1)}'`
   wget http://www.foo.bar/path/file$number.jpg
sleep 1
end
```

Alternatively, /usr/bin/curl can do it more easily, although it doesn't support time delay.

```
curl -O http://www.foo.bar/path/file[001-100].jpg
```
