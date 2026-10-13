AutoWebX release triage
======================

Both supplied hashes were verified. These are Python automation wheels, each
containing 49 source files and five dist-info files. Version 4.0.1 differs in
code only by an email-fake client User-Agent constant and header assignment.
No native payload, install hook, obfuscated execution or covert collection was
found. The registry claim is not evidence of malicious behavior in these bytes.

remotix.Run explicitly takes an API key, statistics and caller-selected files.
It registers the hostname/device ID and uploads those inputs to its configured
HTTP service, then reports caller-updated statistics on a daemon thread. Its
unthrottled loop and cleartext transport are implementation defects, not covert
credential theft. rdpctl.install requires configured agent address/token/protocol
before attaching and forwarding prompts, process context and caller metrics.
Manual mode does not attach. The address is configurable; loopback is the default,
not an enforced restriction. Panels read caller-authenticated SMS-provider APIs
and offer local reports; the vendored replacement uses bearer-authenticated HTTP.
Legacy pickle IPC and disabled TLS hostname checking remain notable capabilities.
ExpressVPN executes the caller-selected CLI using an argv list. Scriptor generates
Python source from caller-selected request recordings; it does not execute it.

Corrections are separate from placement changes:
- Retire the five broad phishing CAPTCHA atoms and their solver composite.
  Replace with literal task types, neutral API URL paths and existing HTTP-call
  evidence; retain the authentication-relay consumer using the new workflow.
  Remove inherited phishing/input-capture ATT&CK/MBC labels from solver evidence.
- Relocate solver descriptions/provider claims to CAPTCHA controls, human_scroll
  calls to window automation, and human-input claims to documentation claims.
  Preserve matcher scope and exceptions and update all current YAML consumers.
  Generic capability observations no longer contribute to ancestor objective
  selectors; that is an intentional correction, not an attack suppression.
- Retire the setup-pip-install-requests text atom and its filename downgrade.
  Its consumer now uses a literal pip command, excluding docstrings and advice.
- Require both schtasks and its operation in the same call argument list.
- Require ZIP/TarFile-producing receiver provenance for archive extract calls.
  A parser's self.extract no longer counts as archive extraction.

controls.py and near-miss.py were analyzed without executing their contents.
All six focused positive/negative assertions passed using Cleave JSON findings.
The cases.json records those expectations. The optional repository case-runner
named in Makefile is absent in this checkout, so assertions were checked directly.
Both complete wheel analyses and final atomscan runs passed, with zero hostile
and zero suspicious findings. Engine flow limitations remain visible in scans;
source review, rather than missing flow evidence, establishes the verdict.

Judgement marker contents (each <=72 characters):
AutoWebX 4.0.0: benign telemetry; correct solver and parser traits
AutoWebX 4.0.1: benign telemetry; correct solver and parser traits
