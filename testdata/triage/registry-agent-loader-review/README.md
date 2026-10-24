Both original samples are judged MALICIOUS after a second static review.
The complete before/after findings, extracted-stage hashes, classifier data,
relocation map and limitations are in `review.json`.

`html_comment_curl_shell.md` is an Environment Status Checker skill document.
Its visible dependency-checking description does not implement those checks.
Instead, its hidden comment tells an agent to fetch remote content and pass
it to Bash as environment validation. This is an agent prompt-injection
attempt. The remote response and any authorized research context are unknown.
Two hostile findings are supported; no third distinct hostile effect is
inferred from an unavailable response. A literal command, an HTML delimiter
and a frontmatter label do not independently establish trojanization.

`TPsecured_stub.ps1` is an encrypted loader. Offline AES-256-CBC/PKCS7
decryption with its embedded key/IV recovers a second PowerShell script.
That script decodes a repeating-key XOR/Base64 assembly and reconstructs a
separate decimal-byte-array PE. It polls for the host process, reflectively
loads the assembly and passes it the host path and native payload. The CIL
entry point builds an ordered delegate pipeline: suspended hidden process
creation, PE-header parsing, thread-context retrieval, image unmapping,
allocation, header and section writes, PEB image-base update, EAX entry-point
replacement, context update and thread resumption. On failure it can kill
the child and retry. This is a process-hollowing chain, independent of names
such as Beacon Controller or the weak external scanner result. The inner
native PE has no ordinary import table and remains protected. Static
disassembly and bounded isolated Unicorn CPU emulation did not recover its
final behavior; no network, persistence, theft or family identity is asserted.

The new suspicious CIL detection describes repeated branches over invalid
metadata-call tokens and null-array traps. The initial unconditional branch
skips those instructions; the following constant-false branch points back
into the trap. This obstructs linear disassembly/decompilation. It is
suspicious rather than hostile because legitimate software protectors also
use anti-decompilation techniques. Its fixture is the actual extracted
assembly (SHA-256 in `review.json`), not a reconstructed program.

Six existing observations move to their supported taxonomy homes. Existing
consumer references, scope and exclusions are preserved. The comment-specific
hostile now also requires the pipeline to occur inside a comment: previously,
an unrelated comment and a visible pipeline could satisfy that claim. The
broader concealed-agent instruction detection remains intact. Generic comment
pipeline syntax becomes notable metadata rather than suspicious
trojanization. The original matcher also matches the inert attack example in
`testdata/benign/tirith-rule-docs-controls/rules.toml`; its scanner-context
exception does not turn the syntax itself into an attack on other files.
The supported syntax remains detected, and agent-directed intent retains two
hostile findings. No hostile coverage is lost. Five unreferenced vocabulary
components cease appearing in the compact Markdown report after dependency
changes; their rules remain unchanged.

Exact and ancestor consumers were inspected before editing. The added
frontmatter alternative covers a subset of an existing member of the same
metadata directory; natural-phrasing/command ancestors have no directory
consumers. HTML-directory exclusions now recognize the comment delimiter as
markup; the existing HTML controls and hidden-agent positive were included in
the focused run. CIL obfuscation ancestor consumers require separate C2,
credential-transfer or build-configuration evidence and do not convict on
this new finding alone.

Run the focused checks outside `testdata`, so path-based suppressors cannot
hide failures:

```sh
python3 testdata/triage/registry-agent-loader-review/check.py /path/to/scratch/controls
```

The 13-file run passed. Controls include ordinary managed binaries, a mutation
that changes only invalid token-table bytes to MethodDef, ordinary installer
documentation, unrelated comment/command placement, phrase-only text, an
existing hostile hidden-agent HTML fixture and an existing masked-host
PowerShell profile. The mutated assembly is a control for one matcher, not
a claim that the rest of the assembly is benign.

The default classifier calls the Markdown benign before and after, despite
retained hostile rule findings (final probability 0.9470687, level 25000).
This is a classifier miss, not a reason to restore inaccurate taxonomy or
add duplicate hostile traits. PowerShell remains classifier-hostile at 0.98,
level 25. Both full-path `.MALICIOUS` markers were written. The required final
repository validation command is `make validate`.
