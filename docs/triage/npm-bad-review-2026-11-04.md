# npm mislabeled-bad review — 2026-11-04

Reviewed 40 entries with Cleave and Atom, inspecting individual archive contents and install hooks. Thirty-five are good, three are bad, and two are inconclusive.

The confirmed good entries `576c23c10d33` and `c45a95aab1be` are versions of a no-op TypeScript logger; `8616a3f04ef6` is a React skeleton component package; `7d0dd68b99e0` supplies development utilities; `b13ed8ea61b2` provides user-invoked audio handling; and `f92c1c6be513` contains ESLint rules and a local rule loader. The scanners report no hostile or suspicious findings on these samples.

The entries `561e0a229023`, `afc15e50f234`, `4db988fbb6a2`, `a14f6d3cfbfb`, `49a104b76bf0`, `a372fa75cbd0` and `1b41aad10bf0` are also good: they contain generator components, visualization code, a native file-event module build, ESLint configuration, an Angular editor wrapper, layout utilities and an asynchronous hook library, respectively. The native module's install hook builds the package locally. Apparent `exec` and base64 matches in the visualization and Angular code are regular-expression operations and inline source maps.

`7a33f468a5e0` is inconclusive: its install script adds an MCP server to many agent configurations and downloads an unpinned native binary from a mutable release URL. The bundled server implements file discovery, but the downloaded binary was not present for review. The existing suspicious findings describe the combined installation behavior; the configuration changes alone do not establish hostile intent.

`ea918b80589a` is bad. Its preinstall hook runs a Bun setup script and the archive carries a heavily obfuscated, approximately 10 MB worm payload. Existing findings in both scanners identify the bundled cloud-secret collector, maintainer takeover and destructive postinstall behavior as well as the install hook.

`a825a8f4d3e5` is bad: an embedded frontend entry point delays an obfuscated image beacon that sends the current page URL and referrer to a Canarytokens endpoint when the site runs outside the configured production hostname. Its constants were decoded offline without executing the script. The new finding combines the delayed evaluator, obfuscated identifiers, browser context, image request and encoded arguments; it does not depend on the endpoint or hostname. This is a canary-style deployment detector, and it reports findings about the host page to an external service.

The same archive's bundled Yarn release produced a misleading decoded-VM finding because unrelated operations appeared on the same long minified line. The existing rule now uses an 8 KiB byte window instead of a line window. Both scanners clear the Yarn bundle and still report a nearby decoded-VM payload control as hostile. Payloads whose related operations are separated by more than the window may need other evidence to match.

`74048b93c558` is bad because its embedded container-isolation test contains runnable fork-bomb and memory-exhaustion payloads. These are guarded by an optional aggressive mode, but they remain attack implementations; both scanners already report them as hostile.

The entries `10830c100112`, `a8987b111dd2`, `13750282edf5`, `121503fa1a6a`, `50b0aa2f57f0`, `565cb5c54cdb`, `c311cd7b7b77`, `3ca8154f2106`, `dde8c4b77824`, `a317d9383cb9`, `f9aa883928f6`, `abdcaeadde54`, `f571d05cdc7a`, `bc9f2c367f6c`, `18f9aa737b89`, `fbc9726f13d8`, `22cac5c4a405` and `5c7a9ebc62ce` are good. They contain libraries, user-directed development tools or interface components; reviewed network, environment and process operations serve their stated functions. The XSL linter's postinstall invokes `patch-package` but includes no patch payload, and the file-event package's installer invokes its bundled native-module installer. Both scanners report no hostile findings, and Cleave reports no suspicious findings for these entries.

`b9afe03d66a1` and `d5dd5d3b71ea` are good: they contain a frontend framework and an asynchronous workflow library, respectively. Neither scanner reported hostile findings, and Cleave reported no suspicious findings.

`dbe92ed81c1b` is good: it is a large identity-service source archive. Both scanners and a targeted review of security-related filenames and host-data reporting found no hostile payload. Its hostname reporting is part of the service's own configured outpost and optional profiling, rather than an exploit or third-party collection PoC.

`3b6fd7d043f6` is good: it is a screen-recording application's source archive. Both scanners and a targeted review of security-related filenames and host-data references found no hostile or suspicious findings; a path-traversal string occurred in a filename-sanitization test.

`4ad0865cc54d` is inconclusive: the package contains a 139 MiB ARM64 executable. The scanners found no hostile or suspicious traits, but static inspection did not resolve the behavior of its extensive bundled runtime and application code.
