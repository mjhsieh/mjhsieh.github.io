---
layout: post
title: "Least Squares in Awk."
date: 2011-08-19 08:15:00 -0800
---

A complete but simplest code in Awk doing least squares fitting. I didn’t write the original code, this kind of code can be found in the text books and from the internet search results.

```
BEGIN{
   sumx = 0;
   sumy = 0;
  sumxx = 0;
  sumxy = 0;
}{
    x[NR] = $1;
    y[NR] = $2;
    sumx += x[NR];
    sumy += y[NR];
   sumxx += x[NR]*x[NR];
   sumxy += x[NR]*y[NR];
}END{
  det = NR*sumxx - sumx*sumx;
    a = (NR*sumxy - sumx*sumy)/det;
    b = (-sumx*sumxy+sumxx*sumy)/det;
  for(i=1;i<=NR;i++) newdet+=(y[i]-a*x[i]+b)^2;
  printf("%.16f %.16f\n",a,newdet);
}
```
