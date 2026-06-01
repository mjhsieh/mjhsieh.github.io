---
layout: post
title: "Playing with FORTRAN memory allocation."
date: 2010-06-16 19:15:00 -0800
---

I was observing FORTRAN’s reallocating behavior, (No, FORTRAN 9x standards do not have reallocate(), but you can always deallocate and allocate.) things went weird after I grow a group of arrays into a group of larger arrays. The numerical performance went south dramatically. It turns out if your latter re-allocations were larger, ifort will try to reuse previous allocation space and take a very far away address for the arrays that don’t fit into the old space. This of course will penalize the performance dramatically. Even weirder, if your later re-allocations were smaller, allocate() doesn’t fit this smaller group of arrays into the old space, as I would have thought, but claim a continuous memory space far away from the old addresses!

As we all know that, FORTRAN doesn’t have facility to print out the memory address, the only way you can do is to use a C function to do that…

```
#include <stdio.h>
void mjreportmem_(long int myadd){
    printf("mjhsieh: %ld\n",myadd);
}
```

ps. It might be only the case of Intel FORTRAN, beware.
