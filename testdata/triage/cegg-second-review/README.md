# MindBreak C Egg second review

Sample: `cegg.unpacked`, SHA-256
`637fa506f553fd49503971a58f009ac1a44d8a5ae67cfde8c7e1c1c7dc6517fe`.
Verdict: **MALICIOUS**. Static reverse engineering with rizin; the sample was
never executed. Public-registry origin and earlier labels were not used as
behavioral evidence. No external corroboration was assumed.

## Verified paths

- ELF64 entry `0x401e50` supplies main `0x401b00`. Main forks, calls setsid,
  starts background workers and scans without an operator-supplied target list.
  Worker `0x4077a0` combines random addresses with sequential /24 sweeps and
  calls service dispatcher `0x407250`. A separate child scans local interfaces.
- Credential collector `0x407fd0` passes root SSH keys, `/etc/shadow`, shell
  history, dotenv files, AWS credentials, Docker config and kubeconfig to
  `0x407a40`. It also enumerates `/home` and constructs equivalent user paths.
  That helper opens and reads up to 1399 bytes, terminates the returned buffer,
  and passes the same buffer to `0x406840`. The latter escapes the contents into
  a typed JSON report, wraps it in an HTTP POST, and calls the send wrapper
  `0x446240` over a connection obtained from the C2 connector `0x406450`.
  This is an actual file-content-to-network chain, not path/string coincidence.
- `0x407b20` checks readable private keys, runs a known_hosts/history address
  extraction pipeline, and formats an SSH command with `-i` and those hosts.
  It invokes the resulting command through `0x40c300` (system), downloading
  and starting a shell payload remotely. It avoids selected operator networks.
- Redis routine `0x4069c0` connects to port 6379, probes INFO, and retries weak
  AUTH values when necessary. At `0x406ab5` onward it sends CONFIG SET dir,
  dbfilename authorized_keys, a public-key SET value and SAVE. At `0x406bc3`
  onward it similarly redirects snapshots into the root cron spool, inserts a
  recurring download-and-shell entry, and saves. Responses control progression.
  Both existing hostile persistence composites accurately describe these paths.
- C2 loop `0x4065a0` registers, sleeps with jitter, submits scan/hit/spread
  statistics, receives replies, and parses a UDP DDoS command and target. It
  starts thread `0x4024e0`, which parses the target, creates datagram sockets,
  sends 1024-byte buffers through `0x446300` (sendto syscall 44), closes the
  sockets and repeats while a shared flag is set. A stop command clears it.
- Docker path `0x403c60` probes the remote Engine API, constructs a privileged
  container mounting host `/` at `/mnt/h`, downloads into the mounted host,
  chroots to launch the payload, then sends container-create and start requests.
  Router exploit templates are also referenced by executable request builders;
  these are not signatures embedded in a defensive scanner.

## Concealment and limits

The executable is statically linked and has no section headers or symbols.
Those properties alone do not establish hostility. Most operational strings
are plaintext. SIMD loads reconstruct some command text from contiguous data;
this is compiler-generated copying, not encryption.

The dead-drop decoder at `0x405f70` searches a response for a marker, parses hex
pairs with `%02x`, XORs each byte with `(7 * tm_yday + 3) | 1`, and accepts only
digits and dots. It is called from the fallback endpoint-recovery path. The
remote response is absent, so its decoded address cannot be recovered from this
artifact alone. The new XOR trait describes the loop's observable transform,
without assigning a destination or attacker intent to the capability.

Installation circumstances, registry package identity, operator authorization,
and live infrastructure are unavailable. The combined automatic propagation,
private-key exfiltration, remote persistence and C2-triggered flooding tip the
judgment; ordinary administration does not explain this default workflow.

## Rule changes and controls

Add neutral observations for key-authenticated detached SSH commands and remote
HTTP download commands, plus a suspicious composite requiring known_hosts
harvesting alongside deployment. Extend the UDP flood label atom to equivalent
`ddos_udp` spelling; its consumers still require their other attack evidence.
Add the address-character XOR loop observation. No IP, public key, payload name,
family banner, exact artifact size or hash gates these detections.

Tighten the postgres process-name observation to an exact token so a database
URL does not match. Consolidate Docker config paths under secret-config, move
chdir syscalls to directory operations and general SSH-directory references to
credential paths. Narrow the mixed SSH config/known_hosts matcher to config and
move it to config/app; known_hosts retains its public-key observation. Existing
consumers no longer treat a public host inventory alone as secret configuration.
Remove the SSH-directory atom's invalid dependency on an objective: a malicious
Ruby environment probe can still reference an SSH directory.

The credential-leaf audit found no duplicate matchers, but identified two
specific subjects misplaced there: a SAM file is an account database, and a
Keychain service name is not a filesystem path. Move these to their existing
subject homes and update exact consumers. The Keychain rule excludes BEAM,
WASM and JVM class files to satisfy its new home's text-matcher scope limit.
Other relocated predicates retain their matchers and scope. Directory selectors
intentionally lose these misclassified observations; they are not replaced with
broader destination selectors that would import unrelated evidence.

All 20 focused controls passed. Run `python3 testdata/triage/cegg-second-review/check.py` for generated positive
and near-miss controls. ELF fixtures are parser inputs and are never executed.
Controls separate SSH discovery, download and launch; test old and new flood
labels; distinguish database URLs from process tokens; vary the XOR loop's
nonsemantic operands and remove essential XOR/address-filter instructions;
and exercise the relocated path and syscall observations.
