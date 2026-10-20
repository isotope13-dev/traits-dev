Static review of the eight queued members
=======================================

The three enclosing archives retain their confirmed MALICIOUS verdicts.
Each member below was judged from its verified SHA-256 and complete source,
with `atomscan` and `cleave facts` collected before and after trait edits.
No sample commands, network requests, or destructive writes were executed.

| Member | Verdict | Traced effects |
| --- | --- | --- |
| `findsock.c` (`2a5548094577`) | MALICIOUS | Walks inherited descriptors, uses `getpeername` to select the supplied peer address/port, duplicates that descriptor onto 0/1/2, and replaces itself with interactive `/bin/sh`. This reuses an accepted connection; it neither connects out nor listens. |
| `qsd-php-backdoor.php` (`eaa0a356da77`) | MALICIOUS | Unauthenticated request dispatch reaches `exec`, arbitrary file reads/writes/deletion, upload placement, chmod 0777, and caller-supplied MySQL queries. The archive branch interpolates a requested directory into a shell command. Base64 and URL decoding transport editor content into `fwrite`; they do not hide executable payloads. |
| `cmd-asp-5.1.asp` (`e5b91baf39dc`) | MALICIOUS | `Request.Form("C")` flows through `szCMD` into WSH Run with `win.com cmd.exe /c`. Output goes to a temporary web-root file, cacls grants Everyone full control, the response prints the file, and another command deletes it. No privilege elevation is established. |
| 1.6.9 `p.js` (`d6f337222fab`) | MALICIOUS | Exported function enumerates C/D/E/F roots, joins each entry to its drive, selects regular files with stat, and writes empty contents to the same path. This destroys existing contents without recursing into directories. |
| 1.6.9 `v.js` (`2e5535f938bc`) | MALICIOUS | Exported function invokes forced, quiet, recursive deletion of the C:\Windows\System32\*.dll glob. Errors and child output are discarded. The matching system-file deletion traits remain suspicious because their general patterns can also occur in image maintenance. |
| 1.6.9 `t.js` (`28db8a38c16d`) | MALICIOUS | Exported function sequentially sets the default boot entry to ignore all failures and disables boot recovery. The shared try block means failure of the first call prevents the second. General policy-setting detections remain suspicious because administrators can intentionally set these policies. |
| 1.6.9 `a.js` (`5ca165dfa018`) | BENIGN | GETs image bytes from Discord CDN, saves the response body under the temporary directory, and tries ordinary start, WIA/MSHTA, a maximized borderless topmost WinForms image, and an inline MSHTA image document. No downloaded code execution, persistence, credential access, or UI lockout is established. The unusual inline-document trait is retained. |
| 2.0.5 `a.js` (`1c33be9e0a79`) | BENIGN | Checks a relative image path, then would write local image-viewer HTML and open it through start/MSHTA. In this extracted tree the computed path ends at `.../o/p/g/bck.png`, which is absent, so it returns before either launch. The bundled image is instead at `.../f/g/bck.png`. No hostile effect is established. |

The JavaScript modules export functions rather than running their payloads on
import. Both package entry points invoke them from the exported `sorgu`
function. Alphabetical directory nesting and single-letter names are not a
hidden code decoder. Facts contain no concealed payload in these members;
the C comments produce an incidental, non-executable Base64 decode.

Trait changes and placement review
----------------------------------

* Move the four `htons`/`htonl`/`ntohs`/`ntohl` symbol matchers and the
  `byte-order` roll-up from `communications/ip/parse` to the existing
  `data/buffer/integer-codec` leaf. Preserve matcher, confidence, severity,
  formats, and platforms; update the explicit serialization consumer.
* Move the native byte-swap builtin matcher out of `os/bpf/network-manip`
  into the same integer-codec leaf, name it for generic byte swapping, and
  make that complete conversion observation notable. Retire the unreferenced
  `ntohs-bswap` composite: its IP-parsing directory selector asserted byte
  conversion even for a plain IP parser.
* Ancestor-selector audit found four `os/bpf` consumers: three TLS
  interception rules and a shared-library backdoor exclusion. A byte-order
  conversion establishes no BPF use and must supply neither evidence nor an
  exclusion for them. No `communications/ip/parse` or integer-codec ancestor
  consumers require expansion. Other existing rules stay in their homes.
* Add notable Node stat and regular-file checks, and a structural Axios
  response-body-to-file detection. The latter binds the promise callback
  parameter to the data argument of `fs.writeFileSync`; unrelated writes,
  headers, and logging are near misses. It makes no payload-execution claim.
* Retain the suspicious structural loop and its hostile fs-import composite.
  Add a hostile corroboration requiring the parsed empty-write/default-mode
  observation as well: the same bound loop empties files with Node's
  destructive default mode, rather than append or exclusive-create options.
  This adds no invented behavior and reuses the canonical matchers.

Run `python3 testdata/stranded-members-review/check.py` for positive and near
miss controls. They check relocated facts, quoted API mentions, distinct
response values, renamed/parenthesized callback parameters, application
directories, different write targets, and nonempty writes. They analyze source
only. The new hostile corroboration scores 6.2 in `cleave test-rules`, above
the 3.5 authoring bar. The eight members and three archives were also rescanned as the focused
corpus; the two BENIGN members retain zero hostile and one suspicious trait.
