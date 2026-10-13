Triage controls for XYO Statement Graph, SvelteKit, and ethjs-filter.

All three submitted SHA-256 values match the archives. Final atomscan runs
contain no suspicious or hostile traits. Manual source review supplements
reported flow-graph limits; no sample code was executed.

XYO Statement Graph 0.1.9 implements finalized block replay, hash-verified
checkpoint persistence, grant projections, and subscription handshake
validation through application-supplied chain/viewer/store interfaces.
The archive contains source maps and declarations, without install hooks.

SvelteKit 3.0.0-next.25 implements HTTP request handling, SSR, client routing,
form/remote-function transport, Vite build integration, environment modules,
and worker-based build tasks. Its CLI synchronizes generated definitions.
child_process.execSync appears in JSDoc examples, not executable calls.

MetaMask ethjs-filter 0.3.0 creates, polls, and uninstalls Ethereum filters
through the supplied query object. Watcher callbacks and configurable decoding
are expected behavior. CommonJS and Webpack distributions reflect the source.
The prepare hook runs the declared Babel/Webpack build. No trait change.

Placement audit:
- Move XYO scoped-name and schemas-name declarations to metadata/package/name/
  identity; move the repository declaration to metadata/package/repository.
  These declarations establish metadata, not implementation identity.
- Preserve the missing-author exclusions through exact updated references.
  No exact consumers of the removed name-only identity composite were found.
  Ancestor well-known/lib selectors intentionally lose these unsupported
  identity matches; relocated metadata must not restore blanket suppression.
- Consolidate the npm repository mirror into the package.json declaration:
  archive aggregation still surfaces it, avoiding duplicate representations.
  The repository leaf remains at its admitted 100-rule limit.
- Anchor the repository URL to reject hosts merely embedding the GitHub URL.
- Remove the redundant raw-text exec-family matcher and its require-plus-call
  composite. The canonical js-child-process parsed-call matcher covers real
  activation, including execFileSync/spawn/fork. Two objective consumers now
  reference it; their required remote-stage or duplex-shell evidence remains.
  This intentionally expands API coverage while excluding comments/strings.
- Remaining XYO provider exception rules are unchanged and do not fire here.

Executed controls:
- exec-calls.js: canonical execution trait matches all three API call records.
- exec-comments.d.ts: documentation example does not match.
- regex-exec.js: RegExp.exec and executable-looking string do not match.
- xyo/package.json: name and repository declarations both match.
- near-miss/package.json: neither declaration matches; the repository URL
  embeds the upstream text in an unrelated host.
- All three complete archives were rescanned after the changes.
