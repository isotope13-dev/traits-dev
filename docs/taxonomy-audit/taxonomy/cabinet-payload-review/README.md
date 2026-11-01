# Cabinet payload review

The legacy cabinet-payload rules mostly matched archive listings together with
independent file properties. They now describe executable, script or data
content and archive layout; their conditions do not establish that two
observations refer to the same member. Generic member sizes, entropy, media
format and encryption are notable observations, not dropper verdicts.

Business-themed executable and script names retain the likely lure intent,
while document-extension PIF clues follow file masquerade. A script-member
and curl-output combination is a download capability. None of those claims
requires that a payload was executed. Existing match conditions, scope,
size gates and exclusions were preserved.
