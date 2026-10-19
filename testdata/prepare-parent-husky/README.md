# Ancestor-directory Husky prepare setup

Reviewed sample: `@adyen/adyen-web@5.32.0`, **BENIGN**.
SHA-256: `2ea3e03b05966ff06d77c74cf2ade5a9869236866d43e457cf56fba75217b96e`.
The sample is byte-identical to the npm registry tarball.

## Decisive release comparison

Fetched `5.31.0` and the immediate predecessor `5.31.3` from the npm registry.
The former has no prepare hook. Compared with that release, the manifest adds
Husky and lint-staged as development dependencies and declares:

```json
"prepare": "cd ../.. && husky install packages/lib/.husky"
```

The identical hook and development dependencies already exist in `5.31.3`.
All seven runtime dependency declarations are unchanged across these releases.
The `5.31.3` to `5.32.0` manifest diff otherwise updates development tooling,
adds a stylesheet lint script, and removes CSS/SCSS from the Prettier task.

The two UMD source maps contain the same 1,030 source modules. There are no
added or removed modules and only three changed modules:

- `OnlinebankingPL/index.ts`: removes the forced `showImage: false` override.
- `internal/IbanInput/IbanInput.tsx`: propagates structured validation errors
  through the existing parent callback and adjusts error messages.
- `internal/IbanInput/validate.ts`: treats empty holder names separately.

All embedded first-party source contents match the official GitHub `v5.32.0`
tag. The distributed files contain ordinary bundles, locales and declarations;
the published file list does not include `.husky` or a new installation helper.
Decoded strings were inspected: Unicode escapes recover the same bundle and
an incidental Base64 candidate decodes to nonsensical bytes, not a payload.

## Execution path

In the official source tree the manifest lives at `packages/lib/package.json`.
The two ascents reach that repository's root. Husky 8.0.1's CLI dispatches
`install` to `install("packages/lib/.husky")`; it checks Git, creates its helper
directory, copies `husky.sh`, and sets Git's `core.hooksPath`. This command
does not install another dependency or rewrite consumer source. The existing
repository pre-commit hook invokes lint-staged (with a Vagrant development
helper branch). The setup is consistent with the lint-staged manifest changes.

Existing SDK HTTP requests and analytics use the configured Adyen loading
context. The checkout-attempt analytics code caches a session ID, sends the
experiments configuration, and logs SDK events; these modules are unchanged.
Secured-field message handling validates the iframe's origin. No changed path
introduces credential theft, a remote payload, or an attacker endpoint.

## Rule correction and controls

The former exclusion recognized one parent only and emitted an ordinary Husky
setup as an attacker objective. Its only consumer now uses a whole-script
exclusion supporting repeated ancestor segments. The ordinary prepare
declaration remains visible through existing lifecycle metadata. Additional
commands, redirection, command substitution and Windows expansion do not
qualify for the exclusion. No package name or version is required.

Run `python3 testdata/prepare-parent-husky/verify.py <scratch-directory>`.
The controls check eight setup variants and twelve near misses, including
named dependency installation before/after Husky. Existing postinstall
consumer-injection controls are independently retained in
`testdata/postinstall-nested-subdir-install/verify.py`.

The sample was rescanned with both atomscan and the edited local rules:
zero suspicious or hostile traits remain.
