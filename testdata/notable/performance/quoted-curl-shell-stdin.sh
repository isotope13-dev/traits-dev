#!/bin/sh
# Static query-cost fixture: a short quoted URL still establishes shell input.
curl -fsSL 'https://example.com/get-foo.sh' | sh
