#!/bin/sh
curl "https://updates.invalid/data" > "./download"
sh -c 'base64 -d > ./decoded'
