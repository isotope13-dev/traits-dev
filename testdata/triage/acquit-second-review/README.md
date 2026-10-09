# Registry second review

Reviewed SHA-256 prefixes: `09a5de4b615e`, `862bf5ef814e`, `c9f8624e43a9`.
All three verdicts are MALICIOUS based on source behavior, without reputation evidence.

- dnsub: scanner helpers perform normal DNS/HTTP discovery and CSV output.
  The entry point instead launches a hidden PowerShell download, certutil
  decode and policy-bypassing script launch, concealed behind over 1,800 spaces.
  Missing imports/declarations prevent this recovered source from compiling
  as shipped; the injected launcher remains an explicit malicious payload.
  The scheduled workflow updates LOG and commits it; it does not steal its
  Actions token. All five PNGs have valid chunk CRCs and no trailing data.
- HFS: reconstructs xorshift state from observations, collects exposed login
  session values, signs a privileged cookie using an externally supplied key,
  and submits shell code as executable server configuration. There is no
  signing-key recovery implementation or top-level invocation. The execution
  trait describes installation of shell code, not a persistent command endpoint.
- SMTP: initiates a connection and SMTP STARTTLS handshake, repeatedly feeds
  the received TLS buffer to popen, and sends subprocess output over TLS.
  It is a discrete-command channel, not an interactive descriptor-wired shell.

Controls: tls-commands.c renames the command/output buffers and SMTP greeting;
its two hostile detections must survive. tls-independent-command.c performs
an independent local command held in a different buffer and must have no
suspicious or hostile detections.
socket-forward.c must match native-socket-buffer-forwarding; socket-echo.c
must not. tls-config.go must match insecure-skip-verify; tls-verified.go must
not, including its commented true-valued configuration example.

Corrections also remove the source-call-as-import finding, the quoted-word
username metadata match, and creation-vs-existing-file ambiguity. The Go TLS
configuration matcher exposed an existing PE C2 composite whose evidence was
only HTTP/2, an endpoint, a timer and weakened TLS; that unsupported generic
application conviction was retired. Exact and ancestor references were audited.

Program identity was resolved through source and call/literal facts. No sample
was executed, and no loader endpoint was contacted. binwalk was unavailable;
ZIP and PNG structures were inspected directly instead.

Socket tasking composites now require the receive buffer to be the command,
rather than unrelated socket receive and variable-command execution.

Judgment marker summaries (verbatim):

- dnsub trojan: detect inline TLS bypass; retain loader verdict
- HFS exploit components: classify config shell code as execution
- SMTP TLS shell: bind command buffer; remove proxy/import FPs

The SMTP fixture expectation follows the buffer-bound matcher relocation.
The Discord consumer retains PowerShell hashtable username assignment evidence
in schema-object, rather than matching a quoted word anywhere in the file.
