The renamed hook should match both python-system-netcat-reverse-shell and
pth-startup-reverse-shell. plain-reverse.py should match only the former.
Import-only, path-only, quoted payload, comment-only, and listen-mode controls
must match neither. Indented imports and commands on a separate line must not
match the startup trait: site.py ignores those lines.

Run `python3 scripts/check-pth-reverse-shell.py` to check the expectations.
These files are scanned statically and must not be executed.
