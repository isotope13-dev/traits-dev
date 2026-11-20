#!/bin/sh
cat part*>joined
base64 -d joined>output.txt
mv output.txt backup.txt
