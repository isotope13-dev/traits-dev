# Stranded member triage regression controls

The remote-evaluation rule now requires `eval(receiver.responseText)`, rather
than independent HTTP, response-body and eval observations. The XSS wordlists
contain separate HTTP alert probes and inline eval probes; they are inert data.
The new negative fixture reproduces this erroneous cross-probe combination.
This deliberately narrows detection: arbitrary variable eval alone does not
prove that the evaluated variable originated in an HTTP response.

The responseText eval atomic keeps its matcher, scope and notable criticality,
but moves from objectives/execution/interpreter/eval/remote to
micro-behaviors/process/interpreter/eval/direct. Every exact YAML consumer was
updated. Six ancestor-selector consumers already accept the destination eval
subtree as an alternative; none relies solely on the retired selector.

The bare ActiveXObject reference moves from process/create/script/wsh to
os/com/automation, preserving its matcher and Windows JavaScript scope. Its
one local wait-loop consumer now references the new ID. There are no ancestor
selector consumers. The call-specific constructor rule remains distinct.

Request.Form moves from http/server/managed to http/request/form-input,
preserving the ASP/C#/HTML matcher and Windows scope. Both exact webshell
consumers were updated; there are no ancestor-selector consumers. The form
reference establishes request input, not a managed-server implementation.

The user-key matcher requires object/array-entry punctuation and a real key
separator. It excludes the Laudanum comment describing username/password
syntax. PowerShell hashtable keys retain their equals separator. Console logging
inspects a parsed call for a text variable or property argument; it no longer
captures `text` from a later XPath expression outside console.log's arguments.

Positive and nearby negative fixtures are recorded in cases.json. Member scan
reports, complete facts and individual judgement markers are kept outside the
traits repository. No malware was executed or ZIP bomb expanded.

The eval/direct leaf was already at its 100-rule cap. Its existing
`evaluate-helper-identifier-call` observation is a call to an arbitrary helper
named evaluate, with no evidence of code interpretation. It moves, unchanged,
to data/control-flow/dispatch; its exact platform-profile consumer follows it.
Ancestor eval selectors intentionally stop treating arbitrary helper calls as
interpreter evaluation. This semantic correction keeps the leaf at 100 without
creating an artificial partition.

The dispatch leaf was also at 100. Its Lua while/if-loop observation describes
a loop, not dispatch; it moves unchanged to data/control-flow/loop, and its
one VM consumer follows it. No ancestor dispatch-selector consumers exist.
This is a placement correction; neither matcher nor scope changes.

The loop leaf's two infinite-loop metric atoms searched exactly the same
metric, with overlapping TypeScript scopes and no exclusions. They consolidate
into source-infinite-loop-metric over the union of their scopes, at notable.
The JavaScript-only ID had no consumers. This removes duplicate TypeScript
findings and preserves all positive observations. The existing source ID and
its consumers remain; their enclosing file-type gates retain their language
boundaries.

The response-body-text leg is redundant with the required responseText-eval
matcher and was removed from the two ActiveX fetch/eval composites. The direct
response-to-eval relationship itself supplies this role; separate tests exercise
loader detection with the HTTP request and eval in the same script.
