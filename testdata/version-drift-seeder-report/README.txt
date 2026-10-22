Guren CLI 2.32.0 version-drift review

Identification and verdict
  @guren/cli 2.32.0, npm CLI for the Guren web framework. BENIGN.
  Original SHA-256:
  c18f82d5a7237bf6be55dc7061365596b1566b4f89cdea3edb10f6a4ea15869b

Decisive execution path
  db:seed -> runDatabaseSeeders -> application config/database.ts seedDatabase
  or runSeeders -> asSeederRunSummary -> summary.seedersRan === 0 ->
  reportNoSeedersRan -> consola.warn/info, or reportSuccess -> console.log.
  The summary contains seeder counts and a database-seeder folder. It is not
  a wallet mnemonic or seed. db:reset and db:fresh also report that summary.
  No network sink or credential acquisition exists along this reporting path.

Version comparison
  Fetched pkg:npm/%40guren/cli@2.31.0 with forager (original registry tarball,
  SHA-256 34f6545dffbf2b3fb5eecb58353dc2d6dd2ce8230db3cbf02e10667aee553533).
  reportNoSeedersRan and reportSuccess are byte-for-byte identical to 2.32.0.
  2.30.0 also contains reportNoSeedersRan. Thus the queued version-drift lead
  does not represent a newly introduced secret-reporting function relative
  to either fetched release. With current rules, 2.31.0 reproduces the FP.
  Manifest changes update ORM/server/core versions and add a Playwright dev
  dependency; neither manifest introduces an install hook. The code diff adds
  destructive-migration checks, browser verification, and reorganized chunks.
  New browser:serve spawns the app entry under Bun with an explicit argv,
  binds 127.0.0.1, and checks the app's local database configuration first.
  Runtime-error fetches validate an HTTP loopback origin and reject redirects.
  The local interactive console intentionally evaluates terminal user input.
  Bundle region comments, import aliases and hashed chunk names are build
  output. Decoded facts show ANSI/Unicode UI text and invalid base64 candidates
  from ordinary identifiers, with no concealed executable payload in this path.
  No deployment context was supplied. Application-specific configuration and
  external dependency implementations were not executed in this static review.

Rule correction and consumer audit
  The unsupported claim was interpreting Seeder run-summary names as wallet
  seed reporting. Narrow report-send-seed-mnemonic-call with a match-local not
  filter for report*Seeder(s){Ran,Run,Found,Missing,Status,Progress}( forms.
  No package-name, file-name, version, score or whole-file exclusion is used.
  Direct consumer: key-material-reporting-call. Its three wallet-key-material
  exfiltration consumers in recon-exfil/wallet-key/telemetry.yaml are unchanged.
  Existing key-reporting-positive.js, wallet-spend-benign.js, and the external
  batch control hostile/xrpl-wallet-header-exfil.js retain identical complete
  finding sets before/after. Mixed secret-reporting plus database-status code
  retains the seed reporting finding; the extracted real database helper does
  not match. Five focused cases pass.

Before/after scan
  atomscan scanned the original archive and members in slow mode, following
  no external references, with the same registry metadata and model v18.18.
  Exactly one distinct suspicious finding disappears: the false wallet rule
  in package/dist/bin.js and its propagated archive-parent copy. No other
  trait is lost or gained. Root risk 131 -> 93; bin.js risk 86 -> 48.
  Classifier verdict BENIGN -> BENIGN, confidence 0.715 -> 0.823.
  No supported attack detection loss or remaining rule/classifier disagreement.

Reproduction
  cleave --traits-dir . --format json \
    testdata/version-drift-seeder-report/database-seeder-report.js \
    testdata/version-drift-seeder-report/seed-reporting-mixed.js \
    testdata/wallet-spend-api-precision/key-reporting-positive.js \
    testdata/wallet-spend-api-precision/wallet-spend-benign.js \
    testdata/hostile/xrpl-wallet-header-exfil.js > focused.json
  python3 testdata/version-drift-seeder-report/check.py focused.json

Environment notes
  Installed atomscan embeds an older Cleave validator that rejects the
  already-reviewed 101-rule metadata/file/naming budget. Scans used
  CLEAVE_VALIDATE=0 after inspecting the documented budget and current engine
  implementation; rule loading/matching remained enabled. Final full validation
  uses /usr/local/var/cyclotron/cleave/target/release/cleave, which implements that
  budget. The model reports its existing v18/v19 feature-version warning;
  before/after scans use the same version. The newer Cleave scan also confirms
  the false finding is removed. Engine flow-analysis limits were supplemented
  by manual tracing of the reporting, database, console and browser paths.
