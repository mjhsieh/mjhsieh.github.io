---
layout: post
title: "Creating file with 'heredoc'"
date: 2002-12-10 00:00:00 -0800
---

This is how I creat file with template in a shellscript.  
Using label in script and redirect sign in unix shell, "cat" can be very interesting.

```
#!/bin/sh
var1 = "test1"
cat << EOF > sample.file
Super hero
Super scum
$var1
EOF
```

If you run this script, you can review the output file "sample.file":

```
$ ./mysrcript.sh
$ cat sample.file
Super hero
Super scum
test1
$
```
