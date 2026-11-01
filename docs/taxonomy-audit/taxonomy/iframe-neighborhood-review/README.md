# Iframe neighborhood review

Remote frame loading is now grouped under HTTP client frame behavior. The
previous resource leaf was near its cap; frame-specific matchers and their
consumers moved together, while non-frame resource observations stayed.

The first legacy iframe-delivery batch and the neighboring invisible-frame
rules describe browser frames, not hidden processes. They now live with the
frame behavior. Small or hidden frames can serve ordinary widgets or tracking,
so these combinations are suspicious evidence rather than conclusive hostile
delivery. The existing same-origin exception remains attached to the
off-screen frame rule. Ledger and Portis endpoint observations move to their
respective recognized product namespaces.

The dropper ancestor consumer retains explicit alternatives for the moved
legacy findings. HTTP client ancestor selectors were reviewed: the new leaf
remains inside that same ancestor, and its added frame-loading findings are
HTTP resource behaviors. More iframe delivery rules remain to be reviewed.

Encoded iframe and script-tag reconstruction now lives with its encoding
mechanism as suspicious concealment evidence; a hidden frame alone does not
establish hostile delivery. The full-page remote iframe combination moves to
UI overlay manipulation. The executable-link and hidden PHP frame combination
is an execution-lure clue, without claiming that a payload was delivered.

The final browser-targeted XHR rule is a reusable capability clue: its
alternatives include evaluation, a worker, or a script element. The worker
and eval composites live with their respective remote execution behaviors.
Two neighboring VM-context evaluators moved into a dedicated VM sink, leaving
room in the in-process evaluation leaf without conflating the mechanisms. The
legacy iframe subtree has no remaining rules.
