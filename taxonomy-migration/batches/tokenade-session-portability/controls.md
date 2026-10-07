# Control results

- PASS cdp-read.py: cdp-discovered-cookie-jar-read present at 3
- PASS cdp-no-read.py: cdp-discovered-cookie-jar-read absent
- PASS in-process.py: chromium-in-process-cdp-cookie-theft present at 5
- PASS oauth-literal.py: placeholder-client-secret present at 3
- PASS oauth-variable.py: placeholder-client-secret absent
- PASS macos-http.py: macos-cookie-path-http-client present at 3
- PASS macos-no-http.py: macos-cookie-path-http-client absent
- PASS pack-magic.py: python-pack-hex-u32 present at 3
- PASS pack-string.py: python-pack-hex-u32 absent
- PASS fingerprint.py: browser-fingerprint-marker present at 3
- PASS fingerprint-neighbor.py: browser-fingerprint-marker absent
- PASS raw-cookie-tunnel.py: strengthened cookie-upload objective present at 5
- PASS raw-cookie-no-tunnel.py: strengthened cookie-upload objective absent
- PASS php-file.php: micro-behaviors/communications/http/curl::file-upload present at 3
- PASS php-text.php: micro-behaviors/communications/http/curl::file-upload absent
- PASS curl-source.c: micro-behaviors/communications/http/upload::curl-upload-or-form-option present at 3
- PASS curl-no-upload.c: micro-behaviors/communications/http/upload::curl-upload-or-form-option absent
