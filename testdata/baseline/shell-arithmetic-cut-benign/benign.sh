#!/bin/sh
for item in alpha bravo charlie; do
  echo "$item" | cut -b 1-3
done
