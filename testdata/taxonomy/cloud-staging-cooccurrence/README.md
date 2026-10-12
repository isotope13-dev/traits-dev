# Cloud-staging co-occurrence guard

`local-data-read-for-cloud-upload` was a bare-`any` umbrella that relabeled
a neutral sensitive-config read as "for cloud transfer" everywhere either
leg fired. It is removed; `cloud-object-local-data-upload` now references
the two micro read legs directly with identical required evidence
(endpoint + upload + either read).

`cloud-staging-positive.js` carries all three legs and must still match the
suspicious composite without reaching the hostile `shadow-it-cloud-staging`
(which additionally needs discovery mapping and cloud credentials). Cases
checked with `cleave --traits-dir . --json` and assertions over emitted IDs.
