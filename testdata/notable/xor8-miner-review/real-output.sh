#!/bin/sh
curl https://updates.invalid/data > ./download
base64 -d ./blob > ./decoded
