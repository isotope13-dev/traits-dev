#!/usr/bin/env bash
# Local JWT sanity check: list tokens committed to fixture files so reviewers
# can rotate them. No network, no lifecycle hook, no exfiltration.
grep -rEho "[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+" ./fixtures 2>/dev/null | grep "^eyJh" | head -n 5
echo "local token audit complete"
