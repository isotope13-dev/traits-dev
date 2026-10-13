# Current file-population controls

These 33 parser and metric controls reuse the B100 fixtures to exercise the
current file-population declarations. The frozen B102 case file remains intact
as historical evidence; its expected ID for the three-or-fewer string rule
predates the later rename to
`metadata/file/profile/string-population::analyzed-layer-string-count-at-most-three`.
The wired `make taxonomy-check` gate uses this current-ID copy so later taxonomy
changes do not make the historical B102 record an invalid current-tree test.
