---
layout: post
title: "How to generate random DNA sequence of a certain length."
date: 2016-11-20 05:43:03 -0800
---

## How to generate random DNA sequence of a certain length.

## of course, I would write this in bash

```sh
# for a length of 24 chars
$ for((i=24;i>0;i--)); do
>     echo -n $((RANDOM%4))
> done | sed -e 's/0/A/g;s/1/G/g;s/2/C/g;s/3/T/g'
```

## shorter

```sh
$ yes 'echo -n $((RANDOM%4))'|head -24|bash \
| sed -e 's/0/A/g;s/1/G/g;s/2/C/g;s/3/T/g'
```

## alternatively

```
$ yes | head -24 | awk '{printf("%i",int(rand()*5)%4}' \
| sed -e 's/0/A/g;s/1/G/g;s/2/C/g;s/3/T/g'
```
