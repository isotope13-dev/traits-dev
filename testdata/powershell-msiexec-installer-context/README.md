Vendor MSI installers are not WebClient droppers
====================================================

`powershell-webclient-remote-exe-launch` fires when WebClient downloads an
executable and Start-Process launches it. Vendor MSI install scripts match
that shape incidentally: they fetch an MSI over HTTPS and invoke msiexec
(including prior-version uninstall cleanup through Start-Process). That is
installer flow, not a stealth payload launch, so the rule excludes the
`start-process-msiexec` context — the same exclusion the `iwr` sibling rule
already carries.

Run `python3 testdata/powershell-msiexec-installer-context/verify.py
<scratch-directory>`. `plain-dropper-positive.ps1` must report the hostile;
`msi-installer-negative.ps1` must not.
