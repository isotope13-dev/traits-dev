# Literal, import concealment and Android loader review

The 89-rule source-string directory was split into command, expression, label,
property and shape subjects. Existing references were retargeted, including
rules split from mixed-subject files. The largest resulting leaf has 27 rules.
A literal or label does not establish that its contents execute.

The 80-rule import-concealment directory was reduced to 64 rules by moving
hash-based import resolution and runtime-computed module names to their
existing mechanism siblings. The original matchers, inherited defaults and
consumer references were preserved.

Fourteen Android staged-loader rules moved to download profiles, module-loading
profiles, package-manager operations and the module-load execution sink. DEX
strings mentioning wget, BusyBox and Toybox, including beside a boot intent,
do not alone establish execution or a dropped payload: those three composites
now report suspicious rather than hostile and describe the observed strings.
The legacy dropper ancestor consumer retains its previous alternatives.

A rule-by-rule comparison covered all 119 moved rules, their matching
conditions and their effective defaults; only those three severities changed.
No directory cap was changed.
