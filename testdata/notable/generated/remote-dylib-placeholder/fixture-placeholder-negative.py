"""Manifest-parsing test with documentation-domain fixture URLs.

Mirrors the risset package-manager test that referenced
https://example.com/old.dylib: RFC 2606 placeholder hosts are not staged
payloads, so source-remote-dylib-url must stay silent here.
"""
DATA = [
    {"platform": "linux", "url": "https://example.com/old.so"},
    {"platform": "macos", "url": "https://example.com/old.dylib"},
]
