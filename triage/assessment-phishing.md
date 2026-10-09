# Assessment-source and credential-export review

## Judgements

| SHA-256 prefix | Identity | Judgement |
| --- | --- | --- |
| 582cb66713fd | EmbedXPL-Forge 5.0.1 Python wheel | BENIGN |
| 3582cd79b789 | Browser credential retry/export client | MALICIOUS |
| 00fa11a959d9 | Shorter credential retry/export client variant | MALICIOUS |

The wheel is an offensive assessment framework. Its entry point starts the
interactive console. Exploit modules accept caller-selected targets; malware
builder components return source templates. The reviewed wiper and ransomware
components do not execute their generated programs on import. The SonicWall
module's dry-run and live branches print instructions rather than implement the
advertised exploit chain. The shell module returns parameterized commands and
provides a listener that relays terminal input; it does not execute those command
strings locally.

The embedded Base64 ELF in the Dell iDRAC ExploitDB example was decoded and
inspected with rizin. It is a 32-bit SuperH shared library, with fork/execlp
imports and racadm user-administration arguments. It accompanies an explicitly
invoked exploitation script. Keep its embedded-ELF observation suspicious,
including the decoded view of the same payload.

Both TypeScript files retain password attempts in distinct record slots, copy
password and OTP input values into the record, emit that record over Socket.IO,
and dispatch remote commands that reset or reveal authentication inputs. Their
HTML imitates browser chrome and an identity-provider URL. The relay domain is
reserved `.invalid`; the shorter variant does not insert its HTML and assumes
missing host-page elements. These are credential-harvesting designs, not proof
of a working deployed relay.

## Corrections and boundaries

- Vocabulary, identifiers, syscall constants, protocol fields, service-port
  references, and constant representations retain neutral observations. They
  cannot establish a backdoor, brute force, scanning, C2, or AES algorithm.
- JSON serialization of a User-Agent is distinct from cookie theft and does
  not itself establish an HTTP POST. An `/accounts` path must terminate as a
  path segment; `//accounts.google.com` is a host, not that endpoint.
- Webhook-profile evidence must share one member file. Module exec and
  executable-name evidence likewise cannot pool unrelated archive members.
- Config/codec, HTTP/deletion, and profile-collection joins describe
  co-occurrence. They do not assert value flow or exfiltration.
- Framework plugin and generator exceptions require source interfaces and
  caller configuration. They are attached to the affected attack detectors;
  capability observations remain visible. Explicit module activation prevents
  the assessment-plugin exception from being borrowed by the activation control.
- Returned shell-command maps and typed host/port arguments distinguish command
  construction from locally executing the embedded command. BuildConfig plus
  script-source strings similarly identify source builders.
- ExploitDB wrapper identity requires both its publication URL and its script
  bridge declaration. Third-party untyped signatures use this named source
  context instead of convicting the bundled PHP example. The CUPS signature
  excludes a declared assessment-plugin class.
- SystemTen identity additionally requires its own identifying evidence;
  preload/libc/syscall references alone cannot establish that family.
- The browser-window phishing rule now requires indexed input-value storage
  and socket record export. Remote MFA dispatch keys are neutral observations.
  The three hostile composites combine impersonation, credential capture,
  retained retries, and remote authentication control.

New leaves distinguish algorithm-independent key representation from AES;
pseudo-socket paths from traversal; multipart requests from HTTP clients; and
scanner request context from general HTTP client references. Hex constant
representations are separate from configuration-schema labels. Quoted target-loop
text belongs to source generation, while actual target-list reads retain their
file-reading home. References were updated with the moves; no aliases preserve
misleading classifications.

## Reproduction

Run `atomscan` and `cleave facts` on each supplied sample. The wheel must have
zero hostile traits and one distinct suspicious trait (`binary/embedded/base64-elf`).
Each TypeScript file must retain three hostile traits across the phishing UI and
operator-control leaves.

Run `python3 testdata/triage/assessment-and-phishing/check.py` for independent
controls. It copies fixtures to neutral temporary paths, then statically scans
actual reverse shells, an activated fake plugin, a returned shell template,
ordinary authentication, browser artwork, an endian conversion, and a renamed
credential-export variant. It never executes fixture code.
