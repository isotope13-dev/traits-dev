# Public-registry second review

All three convictions stand based on executable behavior, independently of
scanner scores, filename labels, and the samples' explanatory comments.

| Sample | Identification | Verdict | Evidence |
| --- | --- | --- | --- |
| `864d38395c99/status.jsp` | Request-command JSP webshell | MALICIOUS | An HTTP `cmd` parameter reaches `Runtime.getRuntime().exec(cmd)` without authentication or command restrictions. The servlet returns the child's stdout in the response. |
| `83a1e89f354c/collab_doors_zipslip_poc.py` | Collaborator review-upload ZIP-slip PoC | MALICIOUS | Constructs a ZIP with five parent hops into `webapps/ROOT`, binding a request-command GSP webshell to that archive member. Posts the archive through the review API, then requests the page with `cmd=id`. |
| `892cb9445ccd/edge_update_install.cmd` | Edge-disguised miner staging script | MALICIOUS | Downloads two executables, configuration and a driver into user Temp; runs a service wrapper, requests an automatic LocalSystem service using Edge Update branding, registers/starts the driver, and launches the renamed miner with pool, worker and algorithm options. |

The JSP executes an OS command directly through Java; it does not necessarily
invoke a command shell. It returns stdout, not stderr, and does not establish
how the file was originally planted. Its existing two hostile findings are
accurate; no JSP-specific rule changes were necessary.

The Python entry point calls upload before trigger. A local exercise replaced
HTTP calls with stubs and inspected the generated ZIP bytes: the escaping
member contains the complete request-to-command-to-response implementation.
The target and session token are placeholders; remote acceptance, the claimed
product vulnerability and servlet mappings have not been independently tested.
This is a functional webshell-planting exploit template, not just a textual
advisory. The source and generated page have no concealed encoding layers.
The engine's `flow-query-incomplete` report is retained; the manual call trace
and stubbed exercise cover the relevant upload and trigger paths.

The batch file has ordinary environment-variable expansion, not obfuscation.
Expansion links the HTTP staging paths to the invoked binaries. It needs
sufficient service-manager privileges and does not elevate itself. The wrapper's
`install` can create the service before `sc create` runs, so that second create
may fail; the script does not check errors. Service and driver creation/start
are attempted behaviors, not evidence that installation succeeded on a host.
The fetched executables and configuration were not retrieved. Their exact
identities, vulnerable-driver exploitation, MSR access and process injection
are not established by this script. Its comments alone do not prove any prior
authentication-bypass chain. The `--cinit-algo` option is configuration evidence,
not sufficient evidence of injection.

Rule corrections

- Added an argument/provenance-bound ZIP member observation and an upload
  composite. Harmless member paths, nonexecutable archive data and archive
  construction without upload are separate controls.
- Required service registration, a Temp image path and mining options for the
  Edge masquerade finding; added automatic service persistence coverage.
  Bare Edge names and paths now have neutral, accurately named homes.
- Removed curl-output-as-browser-launch false positives. Removed injection
  attribution from a lexical cinit-prefix observation and its configuration
  composite.
- Moved driver registration to `os/kernel/driver`, LocalSystem name references
  to `os/user/account`, Java webroot path references to `fs/path/traversal`, and
  executable path references to `fs/path/application/executable`.
- Moved generic download/output/launch co-occurrence out of the dropper tier;
  its description no longer asserts a bound download-to-execution chain.
- Consolidated percent/PowerShell environment EXE paths and percent/delayed
  START variable syntax in their canonical homes. This intentionally broadens
  lexical coverage across valid variable names/syntax; it does not add an
  execution or privilege claim. Updated direct consumers, including the old
  consumers of the removed syntax-specific rules. Canonical leaves stay within
  the existing 100-rule budgets. Actual sample and benign controls were checked
  for unintended objective activation from ancestor selectors.
- Repaired firing cloud endpoint descriptions and raised complete hostname
  observations to notable.

`python3 testdata/triage/acquit-registry-review/check.py` checks 18 positive and
negative cases outside the testdata path. These include zero-hostile controls
for ordinary downloads, browser launch, driver installation, vendor service
installation, mining without service disguise, and service naming without
mining. All 18 passed. Original samples were scanned again with atomscan;
JSON reports confirm 2, 3 and 2 hostile traits respectively. The new ZIP upload,
masquerade and service persistence composites exceed the 3.5 precision bar.

Judgment-marker contents:

```text
JSP request-command webshell: no change
Collaborator ZIP-slip PoC: detect webshell archive upload
Edge-disguised miner stager: fix traits and service persistence
```
