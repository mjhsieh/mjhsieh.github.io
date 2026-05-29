---
layout: post
title: "Removing millions of empty folder under a specific path"
date: 2024-04-22 23:56:52 -0800
---

## Removing millions of empty folder under a specific path

Well only happens on my Catalina box for some reason
```perl
#!/usr/bin/perl
$b = "/private/var/folders/aa/somehash/A/com.apple.metadata.mdworker";
opendir(F, $b) or die;
$i = 0;
while (readdir F) {
    next if /^\.|\.\.$/;
    if (-d "$b/$_") {
        rmdir "$b/$_" or warn "rmdir failed on $b/$_";
        warn "$b/$_\n";
    }
    $i++;
}
print "$i directories identified under $b\n";

