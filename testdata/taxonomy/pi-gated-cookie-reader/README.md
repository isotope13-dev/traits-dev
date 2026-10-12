# pi-gated-cookie-reader regression fixtures

These fixtures are scanned, never executed.

- `optin-gated-reader.tgz` — benign Pi extension shaped like the
  `@vanillagreen/pi-web-tools` corpus regression: a Chromium cookies-table
  reader (`reader.js`, entry symbol `readBrowserCookies`), a Gemini Web
  `StreamGenerate` fallback client (`gemini.js`), a `browserCookieAccess`
  opt-in setting, `pi-package` keyword, `pi.extensions` manifest entry, and
  a harmless postinstall hook. Neither
  `objectives/credential-access/browser/session-hijack::node-chromium-cookie-gemini-web-abuse`
  nor
  `objectives/supply-chain/credential-theft/package::npm-postinstall-chromium-gemini-web-cookie-hijack`
  may fire: `well-known/app/ai/browser-agent/pi-web-access::pi-extension-gated-cookie-reader`
  recognizes the opt-in gated pattern via the generic Chromium
  cookies-table query leg, without depending on pi-web-access's exact
  symbol names.
- `ungated-cookie-hijack.tgz` — positive control with the same cookie
  query, Gemini endpoint and postinstall hook but no opt-in setting and no
  Pi markers. Both hostile composites must still fire.

Rebuild the archives from `src/` after editing a fixture:

```sh
cd testdata/taxonomy/pi-gated-cookie-reader
tar czf optin-gated-reader.tgz -C src/optin-gated-reader package
tar czf ungated-cookie-hijack.tgz -C src/ungated-cookie-hijack package
```

Run `python3 testdata/taxonomy/pi-gated-cookie-reader/check.py` to check
all controls.
