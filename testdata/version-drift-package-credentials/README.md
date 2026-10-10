Version drift triage, 2026-10-10

NW.js nw-v0.113.0 source archive (2038edfc61b3): BENIGN.
Fetched https://codeload.github.com/nwjs/nw.js/tar.gz/refs/tags/nw-v0.112.0.
Compared every unpacked file by SHA-256. Only 19 paths differ: version,
Chromium/Node dependencies, documentation, ffmpeg patch, three C++ source
files, seven node_modules/.bin links, and four Python build helpers.
Build helpers migrate Python 2 exception syntax and decode subprocess bytes.
The flagged issue-number package.json fixtures, all PepperFlash binaries,
and test/sanity/tar/test.tar are unchanged. Rizin identifies the x64 DLL as
PE32+ with Pepper Flash build provenance and normal plugin exports.
Numeric package names are metadata, with no supply-chain compromise claim.

Ente Go module snapshot 561986b103df (cc0e0de26e6d): BENIGN.
Fetched https://codeload.github.com/ente-io/ente/tar.gz/refs/tags/v2.0.34
(the preceding available Go release tag; v2.0.35 is a pseudo-version).
Compared relevant paths and traced their intervening commits using fetched
upstream Git history. This older tag is from 2024; it is not asserted to be
the exact undisclosed earlier version used by the original triage judge.
release-notify.mjs is new relative to that release. Commit 6e0c903563
extracts the existing jq/curl Discord notification into JavaScript: both
send release title, grouped notes and download links to the configured
internal-release webhook. Later commits extend supported apps and formatting.
The webhook is a request destination; no credential is intentionally put
in the body. The coarse payload-flow facts report environment/secret may-flow;
the helper serves both public release-title and secret webhook lookups.
SET_WALLPAPER belongs to the new photo wallpaper preview, with a non-exported
WallpaperActivity. Traced September 10 Flutter UI/hardening commits.
The new CI rust-cache dependency restores build caches; onnxsim is declared
in a new ML playground alongside ONNX, torch and model optimization tools.

Fetched swatinem/rust-cache c19371144df3bb44fab255c43d04cbc2ab54d1c4 and
v2.9.0 from codeload.github.com, unpacked and compared src/cleanup.ts:
byte-identical credential deletion via fs.promises.unlink before cache save.
The 9 MB ncc restore/save bundles include unrelated HTTP clients and reads
of Cargo manifests/lockfiles. Co-occurrence of a credential path, fs import,
and HTTP request proves no credential read or export. The corrected upload
composite requires actual credential-file-to-body flow; it no longer uses
file-wide co-occurrence alone. Its generic credential-path grouping moved
from objectives into fs/path/credential, with consumers updated.

Generic environment-body flow and wallpaper permission remain notable.
Removed the duplicate environment-flow alias from request/credentials;
provider-authentication exclusion already exists on the canonical body rule.
Added an argument provenance matcher for credential bytes from readFileSync
passed to req/request.write or .end, following the existing request-body
matcher convention. The objective also requires HTTP-client evidence. upload.js is positive; cleanup.js
is a near miss that deletes credentials and uploads only a manifest.
Both fixtures are inert static-analysis controls and must not be executed.

Selector audit: no ancestor consumers select the retired registry group or
HTTP rule. The only broad fs/ consumers are two PE import-concealment
composites; the moved package-path group is constrained to JavaScript and
TypeScript, so it cannot introduce extra PE evidence or threshold counts.

Validation evidence: atomscan with CLEAVE_TRAITS_DIR set to this worktree
and SCAN_NO_UPDATE=1 reports zero suspicious/hostile traits for both primary
archives and a separate scan of the fetched Rust cache archive. cleave facts
was run on both primary archives and the notifier. Focused test-rules checks
match the upload and reject cleanup with the same request variable spelling.
Source-analysis budgets still apply to large bundles; this judgement rests
on source inspection and predecessor comparison, not absence of findings.

Full-validation regression: retain a separate suspicious env-body objective
when both environment/secret body-flow facts and a credential-named read
(or Go whole-environment enumeration) occur. This catches the existing npm
agent token leak and Go environment dump controls while the generic body
capability remains notable. Ente's public release notes require no such
credential-named read or enumeration.
