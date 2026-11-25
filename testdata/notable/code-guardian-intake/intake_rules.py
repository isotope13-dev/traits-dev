"""Repo-intake rules: deterministic checks that read a quarantined copy of a repository as DATA. Nothing here runs,
imports or installs anything from the scanned tree.

Rule ids are `group.name`. Every finding records the file, the line, the rule id, the confidence (low / medium / high)
and the exact text that matched (control and invisible characters are shown as \\uXXXX escapes, long text is cut and
says by how much). Confidence is how likely a hit is to be a real problem rather than a false positive; generic
heuristics are low or medium on purpose. A rule that fires is a reason to look, not proof of harm.

These categories follow public write-ups on repo-borne malware; the rules, patterns and code are written
independently for this project.

Public contract:
    RULES                      {rule id: {"title", "means", "false_positives"}}
    CONFIDENCES                ("low", "medium", "high")
    finding(rule, confidence, file, line, match, summary=None) -> dict
    show(text, limit=MATCH_MAX) -> text with invisible characters escaped and long text cut
    Ctx(root, manifest)        read-only view of the copy: .files, .text(rel), .head(rel, n), .lines(rel)
    run_all(ctx) -> (findings, errors)
"""
_PIPE_TO_INTERPRETER = re.compile(r"(?i)\|\s*(?:sudo\s+(?:-\S+\s+)*)?(?:/(?:usr/)?bin/)?(?:(?:ba|z|da|k|c)?sh|iex|"
                                  r"invoke-expression|python3?|node|perl|ruby|pwsh|powershell(?:\.exe)?)\b")
