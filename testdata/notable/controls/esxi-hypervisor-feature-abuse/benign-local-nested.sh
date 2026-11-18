#!/bin/sh
./tools/migrate --dry-run
printf "%s\n" ./tmp/esx64 /selftest
