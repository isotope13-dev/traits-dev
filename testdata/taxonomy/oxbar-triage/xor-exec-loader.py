import base64
encoded_payload = "Z2hpa2xtbm9wcXJzdHV2d3h5eno="
exec("".join(chr(b ^ 42) for b in base64.b64decode(encoded_payload)))
