# Batch carrier review

The legacy encoded-carrier leaf had 85 traits. This review moved 39 batch
observations and composites to their subjects, leaving 46. Literal variable
assignments, command fragments and command text do not by themselves establish
an assembled payload or a launch. They now live with assignments, fragments,
command references or character-code observations. Partial observations are
component or notable and no longer inherit the batch file's unrelated ATT&CK
claims. The ordinary build-script fixture that runs cscript with an explicit
VBScript engine now expects notable: that command alone does not indicate a
hostile stager.

The two batch combinations that indicate a likely WebClient download and
PowerShell evaluation moved to `execution/payload/script-eval/network` and
retain their hostile severity. The document-decoy combination moved to document
masquerading. Other combinations that lack sufficient launch or payload
indicators became suspicious encoding or script-evaluation profiles, with
descriptions limited to their matched clues. Proven data flow is not required
when the combination supports a likely chain.

The two remaining batch composites subsequently moved into file-execution
categories after a joint review of their crowded destinations; see the
[file-execution neighborhood review](../file-exec-neighborhood-review/README.md).
Other carrier and sibling staging rules still need migration. The existing
staged-loader consumer is scoped to Python; these moved rules are scoped to
batch files.

[moves.json](moves.json) records original predicates, defaults, severity and
identifier changes. Run `uv run docs/taxonomy-audit/taxonomy/batch-carrier-review/check-moves.py`
to verify the moved definitions, references and destination counts.
