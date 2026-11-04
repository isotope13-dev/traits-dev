# Composer mislabeled-bad review

All seven archives were inspected and scanned with Cleave and Atom, with reference following disabled. The existing hostile traits describe the identified behavior; no taxonomy change was needed. The gated functions are capabilities in the supplied code and are not assumed to run merely on package installation unless noted.

- `9951efaa0c65652bc4d0855e49bbf1b9564e4d90abf135826110f5f59c25956a` — **bad** — An environment-gated function writes a Windows Startup shortcut that fetches and runs a remote command. Both scanners report hostile persistence.
- `b8e4ebd8be3869a1b5ed9888e2d436eea0ae7b2ba978bcde2220631cc04f5755` — **bad** — An environment-gated function decodes a disguised Base64 value and runs an interactive TCP reverse shell. Both scanners report hostile reverse-shell behavior.
- `c309635b497eb3228eb1d3dfafe40a3da8d7175c2d6cb8ce04ebd4ee3cbd9dc7` — **bad** — The archive vendors a SweetAlert2 routine that waits three days, then disables pointer input and loops remote audio for selected browser languages and host domains. Both scanners report hostile regional sabotage.
- `b5ef102b1df597a9c09b66e513a6c7cbfe6f8bc913a1de0e563ab0379a8db6b9` — **bad** — An environment-gated method discovers mounted devices and overwrites the start of each device with zeroes. Both scanners report the destructive operation.
- `806b6b1be694c3b2713940156fb59a8c11a2e553472190d32c98d88bd00650a6` — **bad** — An environment-gated method writes 1 GiB cache files indefinitely until writes fail, exhausting disk space. Both scanners report hostile disk filling.
- `74bae4c28ce8a839371ce47c0cc3471be81386a22ae03f9ead2cacf3877ce710` — **bad** — An environment-gated method uploads browser login data, cookies and Safari files to a remote relay. Both scanners report hostile credential exfiltration.
- `853e5169d938eb223929d7fc9509991319d29e4f40233ca57c0e3c5cc7ad6e8d` — **bad** — Composer autoloads helpers.php, which constructs a remote hostname from character codes, downloads a PHP payload, and silently launches it using a per-host marker. Both scanners report the obfuscated dropper.
