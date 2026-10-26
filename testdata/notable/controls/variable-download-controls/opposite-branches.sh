#!/bin/sh
if test -f local; then
curl -fsSL https://downloads.example.invalid/helper -o "$download"
else
/bin/sh "$download"
fi
