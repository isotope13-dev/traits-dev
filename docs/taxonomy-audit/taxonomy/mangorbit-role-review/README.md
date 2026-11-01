# Mangorbit role migration

The Open VSX evil-twin extension is a trojanized extension whose identity is
defined by its campaign endpoint and extension-specific markers. The existing
two atoms and composite moved unchanged from `well-known/malware/supply-chain`
to `well-known/malware/trojan/mangorbit-evil-twin`; no YAML consumers of the
old namespace were found.

The synthetic positive fixture contains the campaign domain and User-Agent;
the near miss retains the User-Agent but uses an unrelated domain. Cleave
reported the moved hostile family composite only for the positive fixture. The
near miss still reports the independent User-Agent observation. No network
request is made by either fixture.
