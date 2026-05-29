---
layout: post
title: "Okay awk is slow..."
date: 2012-01-27 07:21:00 -0800
---

(The performance data were updated in a more recent post.)

Here is what I got from counting occurrences of substring in a string

```
bash-3.2$ time -p for i in {1..10}; do\
                     gawk -F 的 '{s=s+NF-1}END{print FS"     "s}'\
                          /Volumes/ramdisk/lotsoftext.txt;\
                  done > /dev/null
real 6.02
user 5.60
sys 0.36
bash-3.2$ time -p for i in {1..10}; do\
                     ./test.pl 的 < /Volumes/ramdisk/lotsoftext.txt;\
                  done > /dev/null
real 3.63
user 3.42
sys 0.18
```

And… here is the test.pl:

```
#!/usr/bin/env perl -w
use strict;
my $query=$ARGV[0];
my $size = 0;
while (<STDIN>) {
   $size++ while $_ =~ /$query/g;
}
print "$query       $size\n";
exit;
```

I thought gawk script is still a thing of beauty, but well.
