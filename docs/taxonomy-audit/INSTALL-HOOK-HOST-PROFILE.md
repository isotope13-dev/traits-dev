# Host-profile collection and exfiltration leave the lifecycle branch

`install-hook` mixed the install trigger with two different results. The
JavaScript/Node query conjunction collected hostname, architecture, working
directory, interface, and optional CI facts; it did not require an install
hook or data transfer. It now lives in `objectives/discovery/system/profile`
as `js-host-profile-query-set`. Its callers use that canonical discovery ID.

The host-profile transmission composites require a transport and the collected
profile, with package lifecycle evidence where applicable. They now live in
`objectives/exfiltration/stealer/system-info`. Lifecycle declarations remain
referenced evidence, not a second objective category. Matcher legs, per-rule
scope, platform coverage, confidence, and effective criticality/MBC are
preserved. The WebSocket redundancy consumer's comment no longer describes
its host-profile leg as install-time because that leg alone does not establish
the trigger.

The npm public-IP POST plus install-lifecycle composite has also moved from the
legacy trigger branch into `stealer/system-info`; the install-hook declaration
remains a required leg.

This moves the evidence to its canonical homes but leaves two over-cap leaves
to audit: `supply-chain/recon-exfil/install-hook` is now **199 rules**,
`exfiltration/stealer/system-info` is **169**, and
`discovery/system/profile` is **93**. These are cohort counts, not cap
exceptions; all still need technique/data-based subdivision. Strict validation
remains at **60 issues** and **164 over-cap directories**. Soft validation
passes **1,837/1,837 fixtures**.
