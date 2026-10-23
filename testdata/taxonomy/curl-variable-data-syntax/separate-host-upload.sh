#!/bin/sh
# Known service reference does not determine the later upload destination.
echo https://transfer.sh/
curl --upload-file public.txt https://other.example/files
