#!/bin/sh
# Vendor installer served from its CloudFront distribution.
curl -fsSL https://d3g5vo6xdbdb9a.cloudfront.net/install.sh | sh -s -- --version 2.4.1
