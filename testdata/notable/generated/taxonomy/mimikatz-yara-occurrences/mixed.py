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

"""This control contains an actual Mimikatz command argument. It must remain
visible to the command-reference matchers regardless of whether the file also
contains an embedded detection rule. The fixture is analyzed statically and
must never be launched during validation.
"""
import subprocess
subprocess.run(["mimikatz.exe", "sekurlsa::logonpasswords"])
