---
title: dkms might not be built correctly post-apt-upgrade
date: May  1, 2026 13:00:00 -08:00
---
Not just ubuntu, debian also has similar issue that after a big upgrade through
apt upgrade, you might not get the link to the right version of kernel header.

So the next time you lose your broadcom-sta-dkms after rebooting post upgrade,
you know you can do
```bash
apt install linux-headers-$(uname -r)
```
Just that you have to have a backup network... Or you could create a case of
circular depedencies: "You need a working network to install a package
in order to fix the network.
