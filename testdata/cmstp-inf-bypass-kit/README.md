INF-driven CMSTP elevation bypass kit
========================================

Unlike the COM-moniker variant in `uac-bypass/com/`, this technique never
touches the auto-elevate CLSID: a crafted INF runs attacker commands from
its pre-setup section, cmstp is killed so the evil profile installs
cleanly, and UAC policy is disabled. `cmstp-inf-presetup-bypass-kit`
requires all three legs, so a lone printer-driver INF carrying
RunPreSetupCommands and a plain corporate VPN provisioner invoking
cmstp.exe do not convict.

Run `python3 testdata/cmstp-inf-bypass-kit/verify.py
<scratch-directory>`. The positive fixture must report the hostile; both
negatives must not.
