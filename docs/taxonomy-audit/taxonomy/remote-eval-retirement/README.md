# Remote-code evaluation retirement

The last 26 rules in `dropper/script-eval/remote-code` moved to network
execution, task dispatch, transformed execution, neutral deployment behaviors,
profiles, or an exclusion-only HTTP context. The legacy remote-code namespace
has no remaining YAML rules or live YAML references. Five findings based on
unbound or weaker clues now report suspicious, and their IDs and descriptions
state those clues without claiming a linked payload. Generic profiles no longer
inherit execution or ingress technique tags.

The network direct-evaluation leaf was divided by activation mechanism:
execution in the current interpreter, a child interpreter command, or browser
script-element insertion. The network source now has leaves of 41, 20, 8, 20
and 10 rules, including its existing constructed and decoded categories. A
curl-to-PowerShell stdin rule moved to the interpreter-stdin sink. This makes it
available to the existing FTP-banner positive directory selectors, whose type
and proximity restrictions still apply.

A separate hostile rule recognizes absolute-URL JSON fetches whose content is
evaluated, preserving the hostile fixture while keeping unbound fetch/eval
co-occurrence as suspicious supporting evidence.

The two legacy ancestor consumers retain all 25 eligible moved alternatives;
the same-origin exception remains exclusion-only. A rule-by-rule comparison
accounted for all 87 reviewed rules and preserved match conditions and
non-technique defaults. No directory cap was changed.
