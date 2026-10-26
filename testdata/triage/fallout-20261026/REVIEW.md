First reasoned review, 2026-10-26

Samples and decisions

* 3be2f88d6519a2d60ef218ddf2a56ddea815ca344266b557bc4bc0dd7a110c79:
  BENIGN, synthetic protected-script fixture. The original has exactly the
  function body in testdata/powershell-hash-gated-loader/gated_loader.ps1;
  testdata/suspicious/powershell-hash-gated-aes-loader.ps1 adds a synthetic-fixture
  comment. Hex character codes evaluate to Invoke-Update. Base64 decodes the
  32-byte ASCII key 0123456789ABCDEF0123456789ABCDEF, 16-byte IV ABCDEFGHIJKLMNOP,
  and a 30-byte ciphertext beginning aabbccdd. Aes.Create defaults to CBC with
  PKCS7: TransformFinalBlock cannot decrypt a ciphertext whose length is not a
  multiple of 16. No plaintext stage is recoverable. Even beyond that failure,
  ScriptBlock evaluation is guarded by a placeholder all-a SHA256 digest.
  There is no network, persistence, credential collection or destructive code.
  The inert protected-hello.ps1 control uses valid CBC ciphertext and a real
  matching digest for Write-Output 'Protected hello world'. This demonstrates
  why the same protection/integrity pattern cannot imply a hostile payload.
  Static API and concealment findings remain useful despite this verdict.

* e04f43cb2e5d1c0893c5b85d5f4ecfd42f59e31fd2b802d3e82f3278bb05cd77:
  MALICIOUS, functional Aokigahara-protocol stealer reconstruction. Its comment
  explicitly discloses research provenance; it is not an original recovered
  Aokigahara binary. Nevertheless its configured entry point collects actual
  home/APPDATA authentication files rather than fake fixture data. It targets
  Claude, Codex, Copilot, Gemini and Codeium secrets/configuration, AWS
  credentials/SSO, and Cursor/Windsurf state databases. A successful handshake
  gates the read loop; per-file exceptions allow continued collection. Contents
  enter a Uint8Array map, zipSync archives that map, and a cipher encrypts the
  archive. X25519 produces a shared secret with the supplied server key;
  SHA256(shared_secret || 'aokigahara') produces the AES-256-GCM key. The
  12-byte nonce is four zero bytes followed by eight random bytes. The HTTP body
  concatenates nonce, encrypted archive, final bytes and authentication tag.
  /gate/chunk sends the body and /gate/complete terminates the session.
  Headers include a hostname-hash identifier, session randomness, gate/build
  values and a Microsoft-CryptoAPI user agent. CLI arguments supply the server,
  peer key, gate token and build ID. No live server or runtime success was
  established; no persistence, child process or cleanup is claimed. Explicit
  invocation and research comments are the strongest benign explanations;
  the working real-secret collection/export path tips the decision.

* 0152e8257c9f80312aba3e3b54e0b3939a781eea4522e00e88f8e47e5e5e495f:
  BENIGN, cjdelisle/Matterfoss, Mattermost server source at
  v1.4.1-0.20190314161043-f1414dd14a5d. Forager downloaded the exact PURL from
  proxy.golang.org, verified h1:uDGeEW1MphIg49GVNwrBnbpksX+99xTdgAHOjMnzEWM=
  against sum.golang.org, and recovered a byte-identical ZIP (same SHA256).
  Provenance and the recovered artifact remain in scratch/fallout-provenance.
  Read README, model/client4.go, plugin/supervisor.go, app/plugin_install.go,
  build/Jenkinsfile.k8s and the nested testplugin.tar.gz bundle. Client4 builds
  normal authenticated Mattermost API requests against its configured server.
  The supervisor launches an installed plugin selected by the manifest, under
  the plugin lifecycle; installation extracts a tarball and does not activate
  it by itself. Jenkins checks out Mattermost repositories, provisions test
  databases, builds/tests artifacts and publishes releases. testplugin has
  only a manifest and a Webpack bundle: entry module 171 installs a plugin
  whose initialize registers ProfilePopover; its render emits the example
  plugin greeting. React, Babel/core-js and Redux account for generic dynamic
  calls, browser/global resolution, DOM operations and timers. No credential
  theft or concealed payload was found along these paths. This is source/test
  packaging, not evidence of a deployed server or an authorized deployment.

Rule decisions and preservation

* Two PowerShell hostile composites required only existing Base64/AES,
  ScriptBlock/eval and digest/character-array observations. None bound the
  alleged entry point, digest comparison or decrypted payload to one another.
  Retained their match sets, renamed descriptions to co-occurrence claims and
  used suspicious severity. These are corrections to existing rules in the
  retained legacy multi-layer branch, not new rules added to that closed home.
  All other existing concealment, decryption and eval traits are preserved.
* Moved ComputeHash/comparison co-occurrence from crypto/hash/file to
  crypto/verify: the matcher never requires a file. Preserved its regex and
  scopes; corrected the gate claim and all live references/fixture mappings.
* Three agent path catalogs previously inferred hostile reads/collection from
  path/read co-occurrence. Existing posix-paths.js returns local file buffers;
  windows-catalog.cs stores file buffers but only prints protocol route URLs.
  These concrete non-export controls refute the unauthorized-transfer claim.
  Retained all three match sets as suspicious with precise descriptions.
* Moved the generic X-Gate-Token header reference out of malware identity to
  HTTP token authentication, preserving matching scope. A family-name literal
  supplies separate identity corroboration. The route/header profile remains
  suspicious, while the hostile family composite now requires the bound
  credential-export chain. Route/header research alone no longer convicts.
* Added a structural source-to-export matcher. It binds a selected list of
  hidden application auth paths through the nested read loop, shared map,
  ZIP variable, cipher receiver, nonce, concatenated ciphertext body and fetch
  body. It requires at least two distinct credential paths. The accepted paths
  may belong to cloud or agent authentication stores; credential is therefore
  its common source home. A hostile composite further requires the cross-agent
  auth and configuration catalogs. Names and route values chosen by an
  operator are not required by this general export detection. The conservative
  syntactic chain does not model arbitrary aliases, wrappers, reordered stages
  or every equivalent implementation. No sandbox observation is asserted.
* Added the missing notable cipher-authentication-tag operation. Promoted the
  existing fetch/POST co-occurrence from component to notable and corrected its
  description; composition membership cannot hide a networking observation.
* Audited exact and ancestor consumers using rg over the four rule tiers.
  The old PowerShell names and hash-gate ID had only their two composites and
  fixture mappings as exact consumers; no live directory selector requires
  the moved file-hash member. Agent catalog IDs had no external consumers.
  Gate-token had only the family profile and focused check as consumers.
  No suppressor was added and no accurate operation was removed.

Verification and limitations

Run python3 testdata/triage/fallout-20261026/check.py and
python3 testdata/ai-train/check.py. Controls cover the full export, renamed
locals, a different sent body, overwritten archive, wrong cipher, a map not
passed to ZIP, no file read, ordinary document backup, route-only upload,
marker-only and single-vendor cases. Original existing catalog fixtures retain
all path observations without hostile verdicts. The genuine encoded Remcos
fixture retains 13 hostile/8 suspicious findings at the outer file, 13/8 at its
AES-decoded layer and 12/6 at its decimal-byte-array stage.

Before/after atomscan scans use the same worktree, local models, slow mode,
no update, and --follow=none. Both original files and every reported archive
member are compared in scan-comparison.json. Cleave facts were collected for
all three originals, including decoded strings and archive members. The
Matterfoss archive and all 806 reported analysis units have no trait changes.

H/S counts: PowerShell 2/3 -> 0/5; JavaScript 4/0 -> 2/5; archive 0/0 -> 0/0.
The two new JavaScript hostile findings cover the bound encrypted secret
export and its family-specific protocol context. The three-to-five hostile
trait goal is not reached: there is no independent supported persistence,
execution, destruction or spying capability beyond secret collection/export
and host identification. Those collection, crypto, staging, POST and host
operations remain covered by suspicious/notable findings; inventing a third
hostile objective or duplicating the chain would inflate coverage. The
source matcher repairs the missed archive-encryption/body link; cloud and
agent credential paths remain visible. No material attack coverage is lost.

The ML ensemble still calls all three hostile: probabilities respectively
0.9976863 -> 0.99775344, 0.99787337 -> 0.9982183 and unchanged 0.9878904.
The PowerShell and archive calls are classifier false positives after this
reasoned review. The scan warns that model feature spec v18 predates v21;
accurate trait changes were not reversed to manipulate those probabilities.
Final repository validation is run with make validate after all edits/markers.

Primary external reference for the reconstructed protocol, not sample identity:
https://research.checkpoint.com/2026/infostealer-riding-the-ai-train/

The existing protected-script fixture moved from testdata/hostile to
testdata/suspicious because the validation harness categorizes expected trait
severity and rejects suspicious objective findings in testdata/benign. This
preserves five accurate suspicious observations; the original sample verdict
is BENIGN, as recorded in its marker and the reasoning above.
