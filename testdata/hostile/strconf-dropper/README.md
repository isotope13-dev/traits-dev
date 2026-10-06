# strconf-dropper

Clean-room variants of the `github.com/goappconf/strconf` Go-module dropper
(see `samples/hostile/github.com-goappconf-strconf-v0.1.1.md`). None are the
real sample bytes. The URLs use invented paths and hosts. Never execute them.

The family is a config-sounding library that holds one remote-script pipeline
per OS (`curl … | cmd`, `wget -qO- … | sh`, `curl … | bash`), picks one at
runtime, and runs it with a hidden console. The script it fetches stages a
bootstrap in an editor config dir (`~/.vscode`), which installs a portable Node
and runs a downloaded JavaScript payload. These fixtures cover the variations
expected in future waves, so no rule depends on this one sample's strings:

| fixture | variation |
|---|---|
| `go-shortener-per-os.go` | Other shorteners (tinyurl/is.gd/bit.ly), `bash -c`, `\| zsh`, renamed package and entry point |
| `go-init-vercel-direct.go` | No shortener (direct `*.vercel.app` routes); fires from `init()` on import, from a map rather than consts |
| `github.com-cfgkit-envparse-v0.3.2.zip` | The `init()` variant in Go module-proxy zip layout |
| `py-per-os-pipe.py` | Python port: `platform.system()` table, `shell=True`, `CREATE_NO_WINDOW`, runs at import |
| `js-per-os-pipe.js` | Node port: `process.platform` table, `execSync` with `windowsHide`, runs at require |
| `stage2-cursor.sh` | Unix stage 2 into `~/.cursor` through a variable, leading blank line before `#!` |
| `stage2-windsurf.cmd` | Windows stage 2 into `%USERPROFILE%\.windsurf`, `call`-launched |
| `stage3-node-bootstrap.sh` | Stage 3: portable Node, `env-setup.js` + `package.json`, `npm install`, run |

Expected convictions:

- Libraries: `dropper/execution/pipe::per-os-remote-script-pipelines` on every port. Neutral process/pipeline co-occurrence is reported separately as `micro-behaviors/process/create/shell/pipeline::spawned-curl-shell-pipeline`. Shortener ports also get `dropper/delivery/pipe::shortened-url-shell-pipeline`, and `init()` ports get `supply-chain/trojanized/library/module-init::go-init-remote-script-pipeline`.
- Stages: `dropper/editor-bootstrap::{bootstrap-var-download-exec,batch-bootstrap-download-exec,node-payload-download-exec}`.
