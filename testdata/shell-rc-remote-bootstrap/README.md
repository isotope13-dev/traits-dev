RC bootstrap needs the remote payload in the RC line
====================================================

`shell-rc-remote-bootstrap` used to convict whenever one file combined any
shell-RC write with any curl-to-shell text, however far apart: a benign
PATH-prepend installer that prints a reinstall hint (OpenClaw's
`scripts/install.sh` persists `export PATH=...` to `~/.bashrc` and echoes a
`curl ... | bash` pointer) read as "Shell RC persists remote payload
execution". The composite now also requires
`shell-rc-redirect-remote-fetch-line`, which only matches when the
remote-fetch text and the RC redirect share one line.

Run `python3 testdata/shell-rc-remote-bootstrap/check.py
<scratch-directory>`. `rc-persists-remote-payload.sh` must report the
hostile; `path-prepend-with-hint.sh` must report no hostile at all.
