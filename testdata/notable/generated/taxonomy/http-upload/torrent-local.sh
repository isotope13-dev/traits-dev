#!/bin/sh
tar -czf release.tar.gz input.txt
mktorrent -a https://example.invalid/announce -w https://example.invalid/release.tar.gz -o release.torrent release.tar.gz
