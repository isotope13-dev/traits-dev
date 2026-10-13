# Pi cookie-client regression fixtures

These fixtures are scanned, never executed.

- `optin-gated-reader.tgz` — benign Pi extension shaped like the
  `@vanillagreen/pi-web-tools` corpus regression: a Chromium cookies-table
  reader (`reader.js`, entry symbol `readBrowserCookies`), a Gemini Web
  `StreamGenerate` fallback client (`gemini.js`), a `browserCookieAccess`
  opt-in setting, `pi-package` keyword, `pi.extensions` manifest entry, and
  a harmless postinstall hook. The neutral
  `micro-behaviors/communications/http/cookies::chromium-cookie-gemini-web-cooccurrence`
  must fire. Neither retired claim,
  `objectives/credential-access/browser/session-hijack::node-chromium-cookie-gemini-web-abuse`
  nor
  `objectives/supply-chain/credential-theft/package::npm-postinstall-chromium-gemini-web-cookie-hijack`
  may fire. An opt-in gate does not make the underlying cookie-client
  capability disappear.
- `ungated-cookie-hijack.tgz` — historical fixture name retained; its code
  only exports a query and an endpoint. It performs no credential reads or
  requests, even when invoked by postinstall. The same neutral finding must
  fire without either hostile claim. A missing setting does not prove theft.

The checker also scans `../pi-cookie-client-triage`: direct and namespace
Slack clients, unrelated constructors, comments, a Gemini class suffix,
directory enumeration without recursion, and unchecked versus origin-checked
cookie redirects. The redirect control renames the helper and local variables
to check that detection follows the relationship rather than sample names.

Rebuild the archives from `src/` after editing a fixture:

```sh
cd testdata/taxonomy/pi-gated-cookie-reader
tar czf optin-gated-reader.tgz -C src/optin-gated-reader package
tar czf ungated-cookie-hijack.tgz -C src/ungated-cookie-hijack package
```

Run `python3 testdata/taxonomy/pi-gated-cookie-reader/check.py` to check
all controls.
