# Multipart traversal controls

These fixtures are scanned, never executed. `ordinary-upload.py` and
`ordinary-form.js` send normal filenames. `local-parent-path.py` contains a
local traversal path but uploads a different filename. None should match
`objectives/execution/exploit/file-upload::parent-path-file-upload` or
`objectives/execution/exploit/network-service/command-execution::traversal-upload-system-cron-rce`.

`traversal-wire.sh` carries a raw multipart request that supplies a two-hop
filename into `/etc/cron.d/` and a valid schedule. It should match both rules,
regardless of endpoint or cron filename. Its harmless command isolates the
upload-to-scheduler behavior from reverse-shell detections.

Run `cleave --traits-dir . --format jsonl analyze testdata/taxonomy/multipart-path-controls`.
