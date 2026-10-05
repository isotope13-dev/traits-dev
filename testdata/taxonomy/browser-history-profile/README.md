These dual-use controls check the distinction between suspicious capability
combinations and hostile remote-command behavior. They are not benign-suite
fixtures: a local browser-history exporter intentionally matches the suspicious
staging rule, and fixed_command.py exercises the existing proximity-only socket
dispatch rule.

Expected negatives:
- local_export.py: no python-websocket-shell-client or remote-shell-chromium-domain-profiling.
- fixed_command.py: no received-command-popen-shell or python-websocket-shell-client.

The comment-only query control is in testdata/benign/browser-history-profile.
Positive Python and JavaScript fixtures are registered in expectations.toml.
