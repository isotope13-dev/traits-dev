# Koi offensive-toolkit triage

Sample: `koi_handler-0.11.6-py3-none-any.whl`

SHA-256: `fd663dcc11dff40f07a5c6f5fdcc490d7e01d8a64f5b414ae7fb765e2d41e222`

Disposition: **bad**, following the requested victim-machine threat model.
The package supplies offensive payloads and post-exploitation operations. This
classification does not assert that installing the wheel automatically runs
those payloads or that the package was covertly trojanized.

Hopper confirmed the move from `good/foraged-promote/.../koi-handler/` to
`bad/mislabeled-good/koi_handler-0.11.6-py3-none-any.whl`: one moved, zero failed.

## Static reconstruction

The wheel has 61 members, including 55 Python source files and no native
payload. All Python sources were parsed without importing or executing them.
The entry points are `koi`, `koifuscator`, and `koireview`.

| Component | Implemented behavior |
| --- | --- |
| `main.py`, `listener.py`, `session.py` | Operator CLI, incoming shell sessions, command dispatch, terminal upgrades; upgrades suppress target shell history by default. |
| `utils/payloads.py`, `modules/duplicate.py` | Constructs Bash TCP, Python socket/descriptor/PTY, PHP, and PowerShell reverse shells; duplication launches a further callback through an existing session. |
| `utils/bash_obfuscate.py`, `utils/ps_obfuscate.py` | Base64, hex, XOR, string splitting, variable replacement, noise insertion, kernel-thread argv disguise, and rewriting ConPtyShell identifiers. |
| `utils/powerupgrade.py` | Fetches ConPtyShell, rewrites it, serves it over TCP, and sends an encoded PowerShell launcher to the target. |
| `modules/secrets_dump.py` | Reads Git/AWS/PostgreSQL/Docker credentials and shell histories, searches dotenv files, inspects other processes' environments and browser credential artifacts. Results return over the existing shell session. |
| `modules/ligolo.py` | Fetches an architecture-appropriate Ligolo agent and uploads it; Windows deployment first adds Defender path and process exclusions. |
| `tunnel/` | Builds and deploys a Python zipapp agent; relays TCP/UDP/IP using a userland stack and a local TUN interface. TLS uses a generated preshared key, so disabled certificate checks alone do not establish unauthenticated transport. |
| `modules/populate_win.py`, `peas.py`, `sharphound.py` | Fetches and deploys offensive tools. SharpHound is run and its output retrieved; the other two modules stage tools rather than automatically invoking every uploaded executable. |
| Other enumeration modules | Host, process, user, route, neighbor, service, Wi-Fi, environment, and privilege-escalation opportunity discovery, including a ping sweep. `winscalate.py` checks opportunities; its descriptions of LSASS dumping and BYOVD are not implementations of those attacks. |
| Transfer modules and `blueprint.py` | Remote command wrappers, TCP file transfer, tar/ZIP directory transfer, Base64 chunked upload, staging cleanup. |
| `mcp/` | Optional authenticated loopback MCP interface; command/module execution requires an explicit enabled setting. It does not establish a hidden external command server. |
| Remaining utilities | Configuration, cache, console UI, SSH transport, and session logs. No concealed installation hook or fixed third-party credential receiver was identified. |

## Rule changes

Reversed all three hunks of
`09969afecd362c15106d5b0ec1b7d3486a5af25d.diff`. Typed `ip`/`port`
parameters and a returned template are not benign evidence. The parameter
declaration fact existed only to feed that suppression, so it was removed
along with the exception and its consumer reference.

The restored PTY rule detects the socket/stdio/shell chain. New Bash and
PowerShell rules describe runtime payload construction, not execution on the
generator's host. They require interpolated source strings with the relevant
shell or read/evaluate/reply mechanics. Bash's stdin bridge must occur in the
same interpolated string; PowerShell's network and command-loop evidence must
overlap. Plain documentation and unrelated strings do not suffice.

Additional rules cover command arguments reading three distinct credential
stores, remote history suppression, Defender exclusions in a single constructed
argument, and kernel-thread shell disguise. The kernel-name reference extends
an existing neutral observation to Python rather than duplicating it. No
conviction depends on the wheel name, package version, author, or host address.

The wheel scan emits four hostile traits (three reverse-shell mechanisms and
the existing developer-credential sweep) plus seven suspicious traits. Existing
notable findings retain networking, encoding, file transfer, credential-path,
ConPtyShell, and tunnel-interface observations. Hostile findings classify attack
capability; they are not proof that every module ran on a particular machine.

## Verification

Run `python3 testdata/triage/koi-offensive-toolkit/check.py` and `make validate`.
Both passed after the final rule placement correction.
The 31 controls are inert source files scanned from temporary paths. They cover
renamed parameters, the reverted suppression, omitted I/O/command components,
ordinary clients, documentation, credential path references, and separated
Defender arguments. The harness never executes sample or fixture code.

Full `atomscan` and `cleave` reports are retained in `/tmp/koi-final-atomscan.json`
and `/tmp/koi-local-final.json` during this triage session. The initial Hopper
upload was blocked by the sandbox; the approved network retry succeeded.
