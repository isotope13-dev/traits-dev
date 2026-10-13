# Qinghu skill release triage — 2026-10-13

The inspected releases are benign. This judgment covers the supplied archive
bytes and the checksum-pinned qhkit dependency, not subsequent mutable installs.

| Archive identity | SHA-256 | Behavior |
| --- | --- | --- |
| linkpix-kling-3-clone 0.1.5 | 1f040392a1ebc44242b5592ff5226a4fcdc151e1183c27ecbd050f97466c10c5 | Qinghu video-inspiration and Kling generation workflow |
| qinghu-amazon-keyword-trend 0.1.1 | 90bede0ff4a116a613b5c7536d23d91ff474f8c65771caf6fe56dee4c3d5b8f2 | Paid keyword_research_trends MCP query |
| qinghu-shipinhao-videos 0.1.1 | 21fd0dd5cf67fadfb68a3521a72f10687279357ea834346f30ba4e6ad7e17946 | Paid fetch_user_videos MCP query with cursor pagination |

Each ZIP contains only SKILL.md, skill-card.md, and _meta.json. SHA-256
checks match the provided identities. Archive facts show ordinary regular
members, without encrypted entries, traversal paths, or executable sidecars.
The source's low capability score does not establish an attack.

The skills bootstrap qhkit through npm, optionally using npmmirror. Node setup
fetches the official distribution and SHA256 manifest, checks the digest before
extraction, and prepends the user's local install directory to PATH. LinkPix
also documents Python/Pillow image compression. Tokens are requested for the
service the user intends to access. Paid submissions require user consent;
read-only schema, price and status queries support the described task.

The inspected @iqinghu/qhkit 0.14.0 tarball matches the claimed SHA-1
b6a3683909f1756b85b533614788c98a365aeb9d and SHA-512
e5f6e71609a5c4aafdb5825455c5ca5e1e3fd18ecbd19cdf32e5e8f7ea1cafca0adc0da9ecb77b7c919db61d1d01801f1fc5457d1953408613411260be225558.
It has no installation hook or third-party runtime dependency. Its command
registry resolves local modules. Configuration reads its own service-token
files/environment; ordinary authentication uses an Authorization header and
configured iqinghu.com/autoagc.com hosts. Config display masks the token;
new user configuration is written with mode 0600. No unrelated secret store,
shell launch, dynamic code evaluation, hidden executable, or obfuscated payload
was identified. Explicitly selected image/video/audio files are uploaded for
media tasks. HTTP Range reads inspect media headers. MCP calls use JSON-RPC,
validate tool parameters, and save large results under its own data directory;
retention cleanup removes old result JSON files. Version checking only fetches
registry metadata and prints an upgrade instruction, without executing it.

## Corrections and reference audit

- Move node-v version-path evidence and its distribution-host conjunction from
  a dropper objective to communications/url/path. Preserve the atom matcher
  and update the standalone-loader consumer. The conjunction describes
  co-occurrence, not a bound URL or download.
- Move Homebrew install text out of package metadata, and install/add command
  text out of shell/build, to os/package-manager/install. Preserve matchers and
  effective platform/type scopes; update the Homebrew context consumer.
  Widen the global npm install and SHA256 command text observations to Markdown
  so a skill's documented setup stays visible. Descriptions assert references.
- Move OPENCLAW-prefixed variable-name text from product identity to env/provider.
  A third-party integration variable does not make qhkit the OpenClaw product.
- Move SCHEMA/TARGET assignment labels to source declarations. Preserve scope,
  matchers and exclusions; update schema and encoded-constant consumers.
- Separate synchronous directory listing from recursive traversal using the
  existing parsed Node call and Python walk observations plus relative-find
  text. Update removal/symlink consumers. Move the existing listing-or-traversal
  umbrella to readdir, qualify all former local references, and update its
  credential, exfiltration, ransomware and family consumers. The deliberate
  matcher change rejects quoted Node API mentions as directory operations.
- Tighten hidden-temp-path evidence to path.join(os.tmpdir(), '.entry'). A
  homedir-or-tmpdir fallback no longer establishes a temporary artifact.
- Move form-named value members to property/access and require nearby DOM
  evidence for the browser-form composite. Preserve the UI composite ID and
  its callers; ordinary video duration option records no longer assert a
  browser form. This is explicitly co-occurrence, not receiver provenance.
- Move module-level calls on imported objects from module loading to module
  execution; preserve the structured matcher and update two objective
  consumers. Update existing golden fixture IDs. Two benign score caps rise
  by one solely because the unchanged observation has a different taxonomy
  weight; their hostile exclusions remain mandatory.
- Rename browser-Blob construction to JavaScript Blob construction and update
  every exact consumer and golden expectation. Node implements Blob and
  FormData too; remove the unsupported browser claim from both descriptions.
- Describe result-named mode members without asserting response provenance.

Exact references and YAML directory references were searched before changes.
Removed identity/objective membership is intentional: generic references must
not supply software identity or attack intent through ancestor selectors.
Historical migration inventories remain historical rather than being rewritten.
There are no new taxonomy leaves or inline YARA changes.

## Verification

Atomscan was run for all supplied ZIPs, and Cleave facts was captured for the
archives, SKILL.md members, dependency archive and MCP implementation. Plain
JavaScript control flow, local-module dispatch, configuration sources, network
sinks, upload paths and retention deletion were reviewed statically; rizin
confirms ordinary ZIP format for the first archive. No package was installed
or executed during triage.

Final atomscan outputs for all three archives and qhkit contain zero hostile
and zero suspicious traits, with ML level -1 (no calibrated alert). Seven
positive/near-miss fixtures in testdata/taxonomy/qinghu-capability-boundaries
pass, covering DOM vs records, temp vs fallback, listing/removal, declaration
and integration references, and install/checksum commands. Existing golden
fixtures are also checked by full validation.

The installed atomscan embeds an older directory whitelist that rejects the
checkout's pre-existing metadata/signed/script leaf. Scans therefore use
CLEAVE_VALIDATE=0 only to bypass that stale bundled authoring check; trait
matching remains enabled. Full validation uses the current local release
Cleave at /usr/local/var/cyclotron/cleave/target/release/cleave with validation
controls enabled, through make validate. Scan dependency following and hopper
uploads are disabled; the exact checksum-pinned dependency is scanned directly.

Judgment marker summaries (also used verbatim in the commit body):

- LinkPix Kling 0.1.5: setup/API workflow; fix capability trait scope
- Qinghu Amazon 0.1.1: legitimate MCP; correct generic capability traits
- Qinghu Shipinhao 0.1.1: legitimate MCP; correct capability traits

The first post-commit make validation encountered stale cached analyzer state:
eight unrelated DOS/batch fixtures lost inline-YARA-derived findings. An
uncached test of the missing boot-sector composite restores both required atoms
and the hostile match. Final verification bypasses analysis, mapper and YARA
caches using CLEAVE_SKIP_CACHE=1 and CLEAVE_SKIP_MAPPER_CACHE=1. No unrelated
DOS rules or fixture requirements were changed, and no precompile was run.
