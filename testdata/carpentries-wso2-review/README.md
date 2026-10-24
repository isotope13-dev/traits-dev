# Carpentries Actions and WSO2 Carbon review

All three supplied samples are **BENIGN**. Each is byte-for-byte identical to
its freshly fetched upstream archive. Forager additionally verified both Go
module archives against sum.golang.org. These provenance checks corroborate
the execution paths below; they do not replace their review.

| Sample | Identification | Hostile before → after | Suspicious before → after | Notable before → after |
| --- | --- | ---: | ---: | ---: |
| 1b65306d825c | Carpentries Actions v1 | 0 → 0 | 0 → 0 | 508 → 508 |
| ef7c14f5785e | WSO2 Carbon Kernel 4.4.2-rc1 | 0 → 0 | 0 → 0 | 687 → 693 |
| 633cbac15b29 | WSO2 Carbon Kernel 4.4.9-rc2 | 0 → 0 | 0 → 0 | 709 → 715 |

Counts are distinct root trait IDs, including inherited member observations.
All analyzed units were compared: 1,898 for Actions (including 68 fetched
registry records), 1,016 for Carbon 4.4.2, and 1,040 for Carbon 4.4.9. No
supported observation disappeared after accounting for the two ID relocations.
There were no hostile/suspicious findings in archive members before or after.

## Behavior and judgment

**Carpentries Actions v1.** Action manifests select the reviewed JavaScript,
Bash and R entry points. The JavaScript actions instantiate Octokit with an
explicit action token, validate PR identity/history/workflow changes, create or
update bot comments, download a selected workflow ZIP, and delete the requested
preview branch. The credential checker sends its bearer token to GitHub's
`/user` endpoint and tests returned OAuth scopes. Organization/workflow checks
gate the optional AWS role assumption and Secrets Manager PAT retrieval;
retrieved PATs are masked and passed to the documented repository operations.
Workflow updates fetch the configured Carpentries upstream, extract workflow
files, replace local workflow definitions and remove temporary extraction data.
Image pruning deletes selected untagged GHCR package versions. These actions
match the documented lesson-build and repository-maintenance purpose.

The apparent secret-export source in Octokit is actually
`def encrypt(public_key: str, secret_value: str)` in a Python/PyNaCl example
quoted inside TypeScript API documentation. No request body or transfer is
established by that match. Both affected dependencies were scanned separately
before and after: `@octokit/openapi-types` 2.0.1/2.2.0 and
`@octokit/plugin-rest-endpoint-methods` 4.4.1/4.4.3. Fresh registry tarballs
contain the exact matching source bytes bundled in all four actions. Their
hostile and suspicious counts remain zero; their notable counts are preserved.

**Both Carbon releases.** These are Maven/OSGi server source distributions.
Bootstrap and CarbonLauncher load the configured local server/framework jars;
Main's shell execution obtains the parent PID for the PID file. The admin home
page checks the authenticated session, validates it again before refreshing
server status, and uses a string timer for the refresh callback. This is an
administrative status page, not an operator-command webshell. Java crypto uses
the configured keystore to encrypt/decrypt with RSA and Base64-serialize the
result; 4.4.9 also supports the configured symmetric-encryption path.

The large AJAX bundle contains Prototype/Overlib/widget code. Prototype's
response evaluation, YUI's script loader and jQuery's script handling are real,
dual-use capabilities and remain detected. EditArea 0.8.2's gzip expands to the
same full JavaScript file. Its embedded script substitutes twelve tokens back
to `this`, `function`, `prototype`, `settings`, and other editor keywords. The
reconstructed code implements editor state, syntax highlighting, keyboard
handling and configured callbacks; it is inserted into the editor iframe.
The PHP compressor implements the corresponding asset compression/cache path.
The decoded stage was written to scratch, inspected and scanned separately.
Its capabilities were retained without inventing an obfuscation attack claim.

`carbondump.bat`/`.sh` require the selected Carbon home and PID, gather OS,
network and process reports, invoke jmap/jstack, copy server logs/configuration/
databases into a diagnostic bundle and clean staging data. Their local
reporting explains the Windows survey finding. The OLE storage finding comes
from EditArea's bundled Windows `Thumbs.db`, not executable Office content.

There is no supplied installation history, operator identity or consuming
application context. These old server sources and CI actions can expose
powerful capabilities or vulnerabilities. Their concrete implementation,
packaging, declared purpose and exact upstream provenance support benign
judgments; no covert theft, backdoor, destructive payload or deceptive
substitution was established. No specimen entry point was executed.

## Trait corrections and coverage

* Relocated the unchanged `secret_value:` predicate to
  `metadata/lang/source/naming/resource::secret-value-colon-token`. The name
  and description now state exactly the token observation. Removed unsupported
  T1041/B0030 mappings. Updated its exact secret-service consumer, which still
  detects the request/route combination. A source token alone no longer acts
  as exfiltration evidence for broad objective selectors.
* Relocated the Windows command survey to
  `micro-behaviors/os/sysinfo/profile::windows-survey-command-cluster`, keeping
  all alternatives, the three-condition threshold, scope, confidence,
  criticality and PeaZip exclusion. Removed unsupported attack mappings and
  updated exact consumers. Preserved the broad credential-export consumer
  with an explicit reference. Other discovery-directory consumers are
  JavaScript/Python scoped and cannot observe this Windows survey under their
  file scopes; the JavaScript vendor exceptions are likewise unaffected.
* Added six notable observations: jmap heap dumping, jstack thread-stack
  dumping, RSA Cipher selection, static JVM Base64 encoding, parsed JavaScript
  string timers, and HTML/JSP string timers. Existing crypto, network,
  execution, deletion and encoding observations remain intact. JVM source
  call facts omit receivers, so the new Cipher/Base64 observations require
  bounded, receiver-specific source call syntax.

## Verification and classifier disagreement

`python3 testdata/carpentries-wso2-review/check.py` passes **26 assertions
across 16 cases**. It stages fixtures outside test-named paths so generic test
exclusions cannot conceal behavior. Controls cover the real Octokit example,
the retained secret-service consumer, local versus exported surveys, command
mentions/help versus dumps, callback functions versus string timers, commented
HTML, JSP, RSA versus AES, and Base64 versus unrelated encoders. The Windows
HTTP survey-export hostile consumer is retained. An existing out-of-batch
PowerShell network-recon fixture also retains its hostile finding.

The initial and final scans use the same v18.18 models and engine 2.13.0,
with updates disabled. The model warns that its feature specification is older
than the engine's. Actions remains below the calibrated classification grid
(level -1), with probability 0.453376 → 0.631871. Both Carbon archives remain
classified HOSTILE (level 0), with probability 0.744794 → 0.850503, despite
zero hostile/suspicious rules and the benign code/provenance evidence. The
higher scores after adding accurate ordinary capabilities are a classifier
false-positive gap, not grounds to remove those detections.

`review.json` records per-sample and dependency counts, probabilities,
provenance hashes and every added member observation. Full scans, facts,
decoded EditArea code and Forager artifacts/sidecars remain under
`/usr/local/var/cyclotron/tmp.noindex/cyclotron-28a4cdc2/scratch/fallout-review`.
