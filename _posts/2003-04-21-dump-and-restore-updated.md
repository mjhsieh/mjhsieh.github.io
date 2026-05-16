---
layout: post
title: "dump and restore (updated)"
date: 2003-04-21 13:10:00 -0800
---

Something which is worthy of remembering it. Why I am using dump and restore? I don't even have access to any tape drive or large sized removable multi-rewritable media. The reason is very simple: it's still a kind of short-cut to copy a filesystem!

This is what I did yesterday.

```
# mount /dev/hdb6 /mnt2
# cd /mnt2
# dump -f - /dev/hda6 | restore rf -
```

It's so easy, but every time I still need 20 to 30 minutes to figure out the arguments. By the way, these commands do not work very well, we shouldn't waste any of our time to do that:

```
# dd if=/dev/hda of=/dev/hdb
```

It's damned slow!
(Updated)
[csardas](https://web.archive.org/web/20040522083458/http://csardas.geekat.net/) said:

how about seting bs argument?  
dd if=/dev/hda of=/dev/hdb bs=1024k

and you have to use hdparm to open ultra-DMA mode of your hd  
(in Linux, ultra DMA seems disable by default)

It costs me 1.5 hours to clone 120G hardisk from hda to hdb.

Yes, I test the hdparm command and it really helps. I tried to enable udma2 using hdparm -X66 ... The problem is that these two disks are not really identical!!!! (Though the model number is the same.)
