#!/bin/sh
for file in reports/*; do
 grep -v "$1" "$file" > temporary
 mv -f temporary "$file"
done
