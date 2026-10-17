# portable-pty local service

`macos-pty-socket-shell-backdoor` (hostile) convicts any binary
combining `openpty`, fork/exec, fd redirection, socket IPC, and a shell
path. That is also exactly what a local PTY multiplexer daemon does:
opencode-pty (a Rust service built on the `portable-pty` crate) spawns
the user's shell and proxies it over a Unix-domain socket under the
user's state directory, with uid ownership checks and no remote
endpoint, persistence, or exfiltration.

`well-known/lib/platform/portable-pty::portable-pty-crate-reference`
marks binaries carrying the crate's registry path; the backdoor rule
skips files carrying it. The marker stays notable so the dependency
remains observable, and crate-free PTY/socket/shell combinations still
convict.

## Controls

`verify.py` builds minimal Mach-O 64 fixtures (LC_SYMTAB imports plus a
string payload) and scans them with `cleave --traits-dir`:

- `pty-backdoor-positive.macho`: fork/exec/dup2/connect/send/recv
  imports plus `openpty` and `/bin/sh` strings, no crate marker. Must
  report `macos-pty-socket-shell-backdoor`.
- `pty-local-service-negative.macho`: the same plus a
  `portable-pty-0.9.0` marker. Must not report the hostile but must
  report `portable-pty-crate-reference`.
