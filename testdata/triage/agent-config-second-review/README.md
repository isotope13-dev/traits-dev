# Agent configuration second review

Both submitted SHA-256 hashes were verified against the complete file bytes.
No family attribution or external reputation was used.

`article-tasks.json` is a VS Code tasks v2 configuration, not an article
catalog. Its shell task probes Node on Unix and Windows, then invokes a
font-suffixed entry under public/fonts. It runs on folderOpen, hides the task
from the picker, suppresses terminal reveal and echo, and masks failures with
an empty echo fallback. This supports a malicious concealed workspace loader.
The font body is absent: no theft, network connection, or payload effect is
claimed. Workspace trust and automatic-task approval remain prerequisites.

`agent-config-poison.txt` is a staged agent instruction bundle, not an
executable program or demonstrated persistence installation. Its apply-in-order
instruction presents root deletion, PowerShell policy bypass, a requests
lookalike installation, an HTML-comment HTTP-to-shell pipeline, and a Base64
system prompt decoding to "ignore previous instructions". The combined hidden
shell injection and encoded guardrail override support MALICIOUS. The .test
URL is a placeholder; the file proves no reachable infrastructure. sudo does
not disable GNU rm root preservation. No successful deletion or durable
reactivation is asserted.

Corrections:

- Policy assignment moved from C2 staging to OS security policy, retaining its
  matcher and defensive exclusion; the WMI consumer follows the new ID.
- The old review-override composite incorrectly asserted a hidden comment and
  supply-chain modification. Its replacement requires an encoded override and
  concealed agent-directed shell injection, under the LLM override objective.
- Lookalike installation now requires pip command context and is suspicious;
  a spelling alone proves neither malicious package contents nor dependency
  confusion. The firing rules moved from depconf to typosquat. Its consumer is file-scoped rather than archive-wide.
- Root deletion matching requires recursive force flags and an exact root
  target, excluding /tmp cleanup, and describes a request rather than a wipe.
- VS Code presentation and shell-type fields require task structure so unrelated
  JSON properties cannot assert these task behaviors.
- Font interpreter matchers require an argument terminator, rejecting ordinary
  build.woff2.js script names.

Focused controls are executed outside testdata to avoid path-based testing
exclusions. They cover unrelated JSON keys, a font-directory build script,
misspelling prose and temporary-directory cleanup, isolated encoded prompt
quotation, policy assignment, and a hidden agent shell instruction without an
encoded override. Full samples are rescanned with atomscan and local traits.

Results: the JSON and text samples each emit two hostile findings, spanning
different objective directories. New encoded-override hostile precision is
7.4 (minimum 3.5); concealed-font-loader precision is 5.9. Ordinary JSON,
spelling prose, /tmp cleanup, and policy assignment controls have zero hostile
or suspicious findings. The font build script and isolated encoded override
each have zero hostile and one suspicious finding. The plain hidden agent
shell instruction retains one hostile shell-injection finding but rejects the
encoded-override conclusion. A bare policy assignment remains notable and
an unrelated proxy bypass assignment does not match it.

Migration consumers: the WMI exact reference follows the policy assignment.
The root-request references in shell-out and file-deletion follow its renamed
ID. The only depconf directory consumer is pkginfo-scoped; neither moved pip
rule supported pkginfo before the move. Other supply-chain parent selectors
still include the typosquat destination. The removed comment-review override
had no exact consumers. The new override has stronger required evidence.

The installed engine treats `data` as an opaque file type rather than the
documented data group; explicit text scope preserves the assignment matches.

Full-validation follow-up: stale required and forbidden fixture IDs now follow
the moved/renamed rules. Task-list and presentation matchers cover both tasks.json lists and
code-workspace nested task lists without exceeding the directory rule cap. The local-script policy assignment fixture
was overturned to benign: it invokes a local PowerShell file with a hidden
window and policy bypass, but has no demonstrated attack payload or intent.
