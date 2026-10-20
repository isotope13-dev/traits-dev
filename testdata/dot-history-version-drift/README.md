standardgalactic/dot v0.63.0: BENIGN

Compared the submitted Go module ZIP with v0.62.1 fetched from
https://codeload.github.com/standardgalactic/dot/zip/refs/tags/v0.62.1.
Of 281 submitted files, 280 are byte-identical; only scripts/ws changed.
The earlier GitHub archive contains nine additional entries (eight removed
scripts and git/.git-templates/.git-templates, absent from the module ZIP).
Both bundled ELF files, every shell startup file, and scripts/_old/gh are
unchanged. The current rules flag the earlier release's history file too.

The changed Perl workspace manager adds an explicit Docker image pull command,
reads user.name from the workspace YAML, mounts the chosen workspace at that
user's container home, records prompted user/group/shell configuration, and
refuses to create an existing workspace. Main dispatch selects x_<user command>;
without an argument it prints usage. Docker execution follows explicit commands.
There is no added secret collection, remote tasking, or concealed execution.

.bashrc sources .shell.d/history.bash. The latter enables vi editing and sets
history retention; its only history -c is in a comment. Even the suggested
history -a; history -c; history -r sequence appends history to disk before
reloading it for pane synchronization. The deleted regex confused HISTFILESIZE
with HISTFILE and crossed into that comment.

Retired objectives/evasion/self-delete/file/script::shell-history-clear-cleanup:
history clearing belongs with indicator removal, and the existing
objectives/evasion/indicator-removal/logs::history-clear-call already recognizes
parsed history calls with the -c argument. The self-delete composite now uses
that canonical trait. The existing Pritunl exclusion remains on the consumer.
This intentionally drops comment-only matches and the arbitrary HISTFILE
proximity requirement; it adds no filename-based exclusion.

Controls (analyze copies outside test paths so fixture exclusions cannot hide
the results; never execute these scripts): commented-sync has no history
clearing; clear has the canonical suspicious call; self-delete-clear retains
the hostile self-delete composite; self-delete-comment does not satisfy its
history-clearing leg.
