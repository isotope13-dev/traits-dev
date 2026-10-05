SYSVOL payload delivery regression fixtures

Inspired by https://www.security.com/threat-intelligence/warlock-ransomware-critical-infrastructure

`renamed.cmd` and `wrapper.py` must match `objectives/lateral-movement/delivery/gpo::sysvol-public-shell-launch`. They vary the payload name, use %PUBLIC% and an explicit Public-profile path, and exercise a Python wrapper around the Windows command chain.

`copy-only.cmd` must not match that composite: there is no executable launch. `prose.cmd` must not match either that composite or `objectives/command-and-control/dropper/staging/public-folder::public-folder-staging-pattern`.

Checked with atomscan JSON output. Fixtures are analyzed as data and must never be executed.
