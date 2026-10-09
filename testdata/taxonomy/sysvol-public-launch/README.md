SYSVOL payload delivery regression fixtures

Inspired by https://www.security.com/threat-intelligence/warlock-ransomware-critical-infrastructure

`renamed.cmd` and `wrapper.py` must match `micro-behaviors/process/deploy::sysvol-public-shell-launch`. They vary the payload name, use %PUBLIC% and an explicit Public-profile path, and exercise a Python wrapper around the Windows command chain.

`copy-only.cmd` must not match that composite: there is no executable launch. `prose.cmd` must not match either that composite.

Checked with atomscan JSON output. Fixtures are analyzed as data and must never be executed.

`privileged-tunnel.cmd` combines administrator-group addition, SYSVOL delivery, Public-profile execution and IDE tunnel service registration. It must match `objectives/command-and-control/channel/tunnel/relay::privileged-sysvol-execution-and-tunnel-service`.
