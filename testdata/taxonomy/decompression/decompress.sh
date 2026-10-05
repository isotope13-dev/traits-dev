#!/bin/sh
gunzip -c input.gz
bunzip2 -c input.bz2
python3 -c 'import zlib; zlib.decompress(data)'
