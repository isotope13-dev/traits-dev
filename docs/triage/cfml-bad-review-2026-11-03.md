# CFML mislabeled-bad review

Review completed: nine snapshot artifacts, all bad. Both scanners were used on each; full validation passed before Hopper confirmed the classifications.

- `d44ecba6653bfb116f9f8bf6f327598e7ea5a300b461f9e5873437c4b9187792` — **bad** — Runs a form-supplied command through cmd.exe and displays output from a temporary file.
- `73b5d8d88d5e9f4cf7c0555dc52e34172bd6b0b03a36b515851a509014c7238e` — **bad** — Enumerates server datasources, executes form-supplied SQL and displays query cells. The new combined finding matched in both scanners; replacing the query with a fixed statement cleared it in Atom.
- `a81a1441f538bc69ed1e740a5c5e315f3fa5462a790b376683340a54b246f2f0` — **bad** — Runs a form-supplied command through cmd.exe and displays output from a temporary file.
- `b83247701eb9eefcf900d2b8ec8ab4c4994d53822d2f32007a99830f801a92e4` — **bad** — Runs a program and arguments supplied through a web form.
- `93513da03687e003a7a411e36e372d7332fb0621f71300c725737f983f43d524` — **bad** — Runs a program and arguments supplied through a web form.
- `6c25e8e703fbdac9159479d009b8de76ac3541bc4c70cc6baaafd5743dc97b2f` — **bad** — WebDAV testing package includes executable command webshells for several server languages, including a CFML webshell. The bundled attack implementations make the archive hostile.
- `c6eddc9a612afbfe014528723ac0d00070c9af11ae760c8923a8dad6fa617372` — **bad** — Runs a form-supplied program and arguments and returns the result.
- `c349de0e5fd85a6603d3edc01a2efff254b0a8a85288a7419c9750e24fc29589` — **bad** — Accepts web requests to read, write, upload, copy, move and delete server files.
- `297908b354d6cf832ecb0317cfd6078fd7fc35c4113da5e8998cb6a2cea45a05` — **bad** — Implements a request-driven command and file-management webshell.
