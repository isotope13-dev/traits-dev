# Source-verified placement follow-up

The seven queued members were reviewed again from the supplied bytes; verdicts
remain five MALICIOUS and two BENIGN. Full facts, initial/final atomscan reports,
and fresh QuickJS traces with mocked filesystem, Axios and child-process APIs
are in the task scratch directory. No specimen command or URL was executed.
Mock traces use virtual paths and do not establish Windows command success.
The image-display members do not establish an input lock or code download.
The 2.0.5 image guard returns for the shipped package layout. Failure of the
first recovery command prevents the second command from running.

Three observations had misleading mechanism placement:

| Previous ID | Canonical ID | Supported claim |
| --- | --- | --- |
| `micro-behaviors/process/create/spawn::shell-true` | `micro-behaviors/process/argument/option::node-shell-true-option` | A JavaScript object property sets `shell` to `true`; it need not be passed to a process call. |
| `micro-behaviors/process/interpreter/shell::windows-shell-option-command` | `micro-behaviors/process/argument/option::windows-interpreter-option-syntax` | Text contains a Windows interpreter command followed by an option; it does not establish in-process interpretation. |
| `micro-behaviors/process/create/launch::mshta-inline-about-document` | `micro-behaviors/process/create/eval::mshta-inline-about-document` | An MSHTA command supplies an inline document as interpreter input. |

Matcher bodies, type/platform scope, confidence and criticality are preserved.
The source files' other rules remain in place. Exact consumers were rewritten;
there are no selectors of the old `launch` or `interpreter/shell` directories.
The old `spawn` selectors now exclude the moved bare option intentionally:
package runtime installation, Socket.IO command execution, obfuscated package
execution, WSH proxy execution, logic bombs and OOB behavior must not infer a
spawn from an otherwise unused `{shell:true}` object. Exact consumers that
explicitly use the option retain it. Ancestor process/create selectors likewise
no longer receive that property as creation evidence. Its new parent is the
existing neutral argument/option leaf. The inline-MSHTA observation joins the
existing interpreter-source execution leaf and remains suspicious, including
for an image document; no benign filename exception was added.

Removed T1059 from the bare option and T1218.005 from the inline document
observation: configuration and document syntax alone do not establish those
attack techniques. The original MSHTA comment incorrectly equated inline HTML
with security bypass; it now states the narrower supported observation.

Six additional positive/near-miss fixtures check object properties versus
comments and false values, interpreter option syntax versus bare names, and
inline MSHTA documents versus about:blank. The original 14 behavior controls
remain. Run `python3 testdata/triage/stranded-member-review/check.py`.

Final member coverage: findsock has two hostile traits, QSD has two hostile
traits, and ASP has three hostile traits. DLL deletion and recovery sabotage
retain two suspicious traits each: their generalizable matchers can also see
offline-image servicing and deliberate administrative boot configuration, so
hostile severity is not warranted for those matchers. Each image viewer retains
zero hostile and one suspicious trait. All seven supplied SHA-256 values match.

Validation expectations and the older stranded-member cases now use the new
canonical IDs. The real-spawn shell-option fixture gains one score point (6 to
7) because argument configuration and creation occupy distinct taxonomy prefixes;
its zero-hostile and zero-suspicious limits are unchanged. The comment/false-option
negative control keeps its existing score and severity limits.

The 20 focused controls and all four affected older stranded-member emission
controls pass. An exploratory run of the complete older nine-case file reports
an unrelated existing expectation for `go-shutdown-command-construction` that
is not emitted (its two constituent call traits are emitted). Shutdown rules
and that fixture are outside this change and were left untouched.
