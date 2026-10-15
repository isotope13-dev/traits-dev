# Yantra Mobile 12.0.107-alpha.1 triage

Package: `@adminide-stack/yantra-mobile@12.0.107-alpha.1`

SHA-256: `161d9077c430b9b6a4861cb2f3114be3710ce6e59f5b6ba7f563f3fe35711a97`.

## Assessment

Benign React Native application package. No concealed payload, package-install
code runner, obfuscated execution stage, unrelated credential-store harvesting,
or attacker-directed collection was identified in the supplied artifact.
This is a static assessment of the supplied archive; registry dependencies and
remote application backends were not fetched or executed.

The archive has 1,352 regular files, with no links: 660 JavaScript modules,
660 source maps, three TypeScript files, two JSON files, one PNG, 25 WebP
assets and a license. Compiled JavaScript totals approximately 4.98 MB and
122,503 lines. Of the maps, 659 include readable original TypeScript/TSX
sources. Those were extracted for inspection alongside the executable modules.
Atomscan analyzes 1,342 entries including the archive.

The package manifest declares a prepublish build but no preinstall, install or
postinstall script. Its exports integrate UI features into the host app.
Large source files include design prompt catalogs, airport data and editor UI.

## Sensitive behavior reviewed

- `readAuth0Session` reads the application's `id_token` and `access_token` via
  Expo SecureStore, falling back to application AsyncStorage. The WebView
  authentication bridge returns this session to the hosted application; it
  does not enumerate other applications' credentials.
- Surface sessions are minted through configured GraphQL endpoints. Injected
  boot scripts deliberately copy the session token into the surface's local
  and session storage and intercept its auth-context lookup. Navigation is
  routed by `classifySurfaceNavigation`; this is an application trust boundary,
  not proof that every possible configured surface is trustworthy. The shell
  also allows mixed content and grants WebView media capture through host
  permissions. These are visible application integration settings, with no
  concealed attack logic found around them.
- HealthKit and Health Connect readers request platform access and query
  permitted records such as steps, sleep, workouts and heart rate. Sync runs
  for signed-in users after sync is connected or a device is paired, sending
  data to the configured Fitness backend. It is not a background package
  installation action.
- The BLE transport loads `react-native-ble-plx` lazily, requests Android
  scan/connect or location permissions as appropriate, discovers health
  devices, and reads, writes and monitors GATT characteristics.
- The visible audio recorder prepares and starts recording when mounted,
  exposes cancel/send controls, stops at a duration cap, and uploads the
  chosen recording for transcription. Native dictation has an explicit
  permission request. Camera/editor and map WebViews implement visible
  application features.
- Gateway communication uses configured HTTP, GraphQL and WebSocket services.
  The AI helpers send application prompts/tool results; map, shopping, travel,
  messaging and media features use their corresponding service calls. No
  hidden shell launcher, environment dump or encoded executable payload was
  found in the indexed source operations.

The source review used the compiled modules, embedded source maps, API-call
searches, and `cleave facts` on the credential, handoff, location and BLE files.
Raw facts, extracted sources, operation indexes and scan outputs are retained
under `/tmp/triage/yantra-mobile-12.0.107-alpha.1/`.

## Added neutral coverage

Eight provider/operation findings were absent from the original scan:

- Expo SecureStore import plus asynchronous item read.
- Health Connect import plus record query.
- HealthKit import plus health-sample query.
- Expo audio import plus recording preparation.
- BLE discovery, GATT read, GATT write and GATT monitoring calls.

Four reusable parsed-call atoms also expose the underlying item getter,
record query, health-sample query and recording preparation. Each is notable;
none makes a surveillance or credential-theft claim. Provider composites use
engine-emitted import facts and named call atoms, and describe same-file
co-occurrence rather than claiming receiver provenance. BLE method receivers
can be renamed. Comments, string examples and method declarations do not
satisfy parsed-call conditions.

The health APIs query application record stores, so they belong in
`micro-behaviors/data/db/query`. Expo protected storage belongs in
`micro-behaviors/os/security/credential-manager`. Recording preparation and
GATT operations use the existing audio and wireless leaves. No new taxonomy
branch or package-specific exclusion was added.

The two existing ancestor selectors are exclusions on arithmetic findings;
recognizing audio setup preserves their intended audio-context exclusion.
The additional generic database-access leaf has no ancestor consumer.
`selector-audit.json` records the reviewed selector set.

## Repaired legacy placement

Four previously notable observations were filed under attacker objectives even
though their own matchers do not establish an attack. Their matchers, effective
file types, platforms, criticality and confidence are retained:

- `BUCKET_ORDER` now appears as a source-identifier reference under
  `metadata/lang/source/naming`. Here it ranks movie formats (`standard`,
  `imax`, `dolby`, etc.), not email deliverability.
- Payment-control and transfer-method names also live under source naming;
  `bank-transfer` alone does not establish payment-page manipulation.
- A phrase addressing an AI agent lives under `micro-behaviors/data/llm/agent`.
- Appending tool-role messages to history lives in the same neutral agent-data
  leaf. The upload consumer continues to require its separate transfer and
  learning-endpoint evidence.

Exact contextual consumers now reference the relocated observations. Ten source
ancestor selectors were audited. Existing any/unless lists explicitly retain
the moved members. Two required unions were rewritten as all(required roles)
plus any(original namespace, relocated members), preserving the original
Boolean condition without making a context reference optional. The credential
export consumer is renamed to describe both reconnaissance and ranking
references, and its exact caller was updated. A package-manifest consumer's
description now acknowledges its existing exfil/agent-text alternatives.

The AUI Agent Builder outer-scoped exception moved to its existing well-known
product leaf, preserving its three legs and scope so the neutral capability
does not depend on an objective. There are no effective destination-ancestor
selectors for these moves; a local rule definition named `metadata` was
excluded from the reference audit. `legacy-relocations.json` records the moves,
selectors and consumer rename. No placement holds remain for these four
findings, and no suppression or package-name exclusion was added.

## Validation

```sh
python3 testdata/triage/yantra-mobile-12.0.107-alpha.1/check.py
make validate
```

All 24 focused cases passed. They cover namespace aliases, ordinary libraries
with similarly named methods, imports without calls, native recording setup,
BLE write variants, comments, strings and method declarations. Six additional
cases verify the relocated source names and agent operations, including the
original email-bucket and payment-control consumer contexts.

`make validate` passed all configured corpora, including hostile 668/668,
benign 1478/1478 and does-nothing 176/176. The archive rescan has zero
suspicious and zero hostile findings and includes all eight new provider/
operation findings. The minor final authoring adjustments factor an equivalent
query regex and restrict the generic item-getter atom to the observed native
mobile platforms; they preserve these source matches.

The already-reviewed sample was moved to Hopper's `good/mislabeled-unknown`
pool and the local archive is at
`/tmp/triage/misplaced-good/@adminide-stack-yantra-mobile-12.0.107-alpha.1.tgz`.
After completing the legacy moves, `atomscan-complete.jsonl` again reports
zero suspicious and zero hostile findings and replaces all four old IDs with
the correctly placed observations.

The final full validation after all four legacy relocations also passed every
configured corpus (`validate-complete.log`), including hostile 668/668,
benign 1478/1478 and does-nothing 176/176. `result.json` contains the concise
final disposition and verification results.
