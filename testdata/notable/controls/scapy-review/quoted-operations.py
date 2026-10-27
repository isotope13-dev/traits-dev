# Parser-backed operation detectors must ignore these references.
example = 'os.pipe()'
codec_example = 'value.decode("base64")'
request_example = 'Request(url, data=payload)'
text = b"plain text".decode("utf8")
triple_example = '"""YWJj""".decode("base64")'
