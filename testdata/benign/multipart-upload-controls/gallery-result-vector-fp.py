# -*- coding: utf-8 -*-
# Regression guard: extractor result vectors pair ("", "<site>", ...)
# category tuples with .php page URLs. Without a `files` payload under
# test this is not a multipart upload of any kind.
from gallery_dl.extractor import aryion


__tests__ = (
    {
        "#url"     : "https://aryion.com/g4/gallery/jameshoward",
        "#category": ("", "aryion", "gallery"),
        "#pattern" : r"https://aryion\.com/g4/data\.php\?id=\d+$",
    },
)
