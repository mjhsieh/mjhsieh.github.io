---
layout: post
title: "Multiple-volume backup in tar"
date: 2012-01-01 10:15:27 -0800
---

I found that `split(1)` command is much easier to use for making a multiple volume tar ball with fixed volume size 100MB.

BEFORE: `$ tar cMf /Volumes/webdav/backup01.tar /some/important/files/ -L 102400`  
(please do remember to use ‘n /Volumes/webdav/backup02.tar’ command and two return keystrokes to proceed to the next “volume”.)

AFTER: `$ tar cf - /some/important/files/ | split -b 100m - /Volumes/webdav/backup01.tar.`  
(the final dot is important because it’s the prefix of multiple filenames we are trying to store at the remote server.)
