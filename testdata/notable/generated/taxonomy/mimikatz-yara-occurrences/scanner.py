"""A scanner embeds detection expressions as data. It can pass these rules
into a YARA process without executing any of the commands in the strings.
The names in these definitions are deliberately generic fixture values.
"""
RULES = (
    'rule credential_pattern {\n'
    '  strings:\n'
    "    $needle = \"sekurlsa::logonpasswords\" nocase\n"
    '  condition: $needle\n'
    '}\n'
)
