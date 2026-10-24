The three stranded members were independently reviewed from their complete
source, package entry points and Cleave facts. Archive convictions were retained.
The original archive and member SHA-256 values match the supplied identities.
No specimen code or downloaded executable was run.

* `perl_cmd.pl` is DK's CGI command backdoor bundled with DAVTest. It reads
  QUERY_STRING, decodes `%20` and lowercase `%3b`, executes the same scalar
  through backticks, and returns captured stdout as HTML. No authentication or
  command restriction is implemented. `/etc/passwd` appears in usage text;
  this does not establish fixed credential theft. DAVTest's explicit backdoor
  upload operation establishes an operational payload role. Authorized testing
  is possible, but the member implements an unrestricted remote command
  surface, supporting MALICIOUS. Actual deployment and upstream access controls
  are unknown. Both existing hostile findings and the suspicious request-to-
  command finding are accurate. The new notable trait records the no-cache
  HTTP header without claiming no-store, evasion or persistence.
* Android `process.py` requires a target package, checks Frida connectivity,
  invokes Objection for component enumeration, root-check and TLS-pinning
  bypass, searches memory for secret-shaped strings, lists Keystore entries,
  queries debug state via ADB and writes a local JSON assessment. Memory search
  results are counts; up to 2,000 characters of Keystore output are retained.
  Its Frida inline-script helper is defined but not called by main. The visible
  assessment workflow, explicit target and local output support BENIGN;
  target authorization is unknown. The existing suspicious root-check bypass
  is accurate and retained, as are the notable pinning/memory/Keystore signals.
  New notable traits record a dumpsys package command passed to a call and an
  actual FLAG_DEBUGGABLE membership test. Neither claims anti-analysis intent
  or a successful privilege escalation.
* zlibxjson `main.py` implements only a Windows executable downloader/launcher.
  Its wheel console entry calls init; importing the package only exports init.
  init reads APPDATA and passes a fixed Discord attachment URL and that directory
  to a helper. The helper derives the file basename without the URL query,
  streams requests.get chunks into that file and returns its path. Another
  helper launches that path with shell=True and CREATE_NO_WINDOW. Missing
  APPDATA and launch failures produce diagnostics. No JSON/compression utility,
  persistence, secret theft, exfiltration, obfuscation, elevation or cleanup is
  implemented. Its sole-purpose hidden loader and placeholder package provenance
  support MALICIOUS. Final executable contents and runtime success are unknown.
  The exact payload URL returned HTTP 404 through Forager. Required all-wheels
  recovery for zlibxjson failed after PyPI metadata 404 and unavailable Chromium
  ICU data; the supplied original wheel remained available. Forager recovered
  the exact original ai-forge wheel, including its .forage.json provenance.

All firing hostile/suspicious findings were checked against execution paths.
No existing trait was removed, narrowed, relocated or reduced in severity.
The zlibxjson rules accurately cover HTTP/file staging, APPDATA lookup, shell
parsing, window suppression and the linked helper launch. Source-to-helper,
file-to-launch, destination and visibility boundaries were investigated using
all ten existing stranded-review cases. The generalizable mechanics are shared
by legitimate updaters. Neither a hosting provider nor hidden execution alone
supplies an unauthorized result; additional hostile rules would require
unsupported intent, duplicate this one chain or invent downstream behavior.
This hostile-intent coverage gap remains open. The unavailable EXE prevents
investigation of downstream attack outcomes. The Perl member likewise has only
one command channel and its output; there is no distinct third hostile result.

Run `python3 testdata/stranded-member-observations/check.py` for the four added
positive/near-miss controls, covering comments, docstrings, quoted code,
no-cacheable, a different command and a different debug flag. All pass.
`python3 testdata/stranded-review/run_cases.py` passes all ten existing controls.
The new rules use existing admitted leaves and do not alter existing consumers.
Cleave's parser reports source-local flow limitations; manual source tracing
covers the relevant paths. Atomscan reports model feature specification v18
versus expected v21. Detailed per-analysis-unit before/after counts, additions,
losses and classifier values are recorded in review.json. Raw scans, facts,
Forager artifacts and failed-recovery logs are retained in the task scratch
stranded-review directory.
