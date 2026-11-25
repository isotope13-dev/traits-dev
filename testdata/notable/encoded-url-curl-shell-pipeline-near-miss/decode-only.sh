#!/bin/sh
URL=$(echo "aHR0cHM6Ly9kZWxpdmVyeS5leGFtcGxlLmludmFsaWQvYm9vdHN0cmFw" | base64 --decode)
echo "$URL"
