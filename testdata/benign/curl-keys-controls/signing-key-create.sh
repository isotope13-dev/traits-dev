#!/bin/sh
# Create a server-side signing key on the artifact service under test.
KID=$(curl -s -X POST "$BASE/api/v1/signing/keys" -H "Authorization: Bearer $TOK" -H "Content-Type: application/json" -d "{"name":"release","key_type":"gpg"}")
echo "$KID"
