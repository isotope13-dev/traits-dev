Startup shortcut capability controls

- `startup.js`: notable shortcut creation with a Startup path reference.
- `desktop.js`: creates a shortcut but has no Startup reference; no autorun composite.
- `downloader.html`: preserves the hostile HTML downloader consumer.

Migration: move the generic `startup-shortcut-persistence` conjunction from
objectives to `micro-behaviors/os/autorun/login-items::shortcut-creation-startup-reference`.
The matcher is unchanged; the description states co-occurrence, not proven flow.
Move `powershell-startup-special-folder` and its path-reference OR to
`micro-behaviors/fs/path/autostart`; the OR is notable because its alternatives
are complete path observations. Its explicit file scope covers its sole
consumer and the PowerShell resolver. All exact consumers were updated.
No objective-directory ancestor selectors consume the moved rules. Two
filesystem ancestor selectors (`well-known/tool/offensive/powershell-empire`
and `objectives/anti-static/obfuscation/imports/concealment`) already include
the underlying path atoms; the Empire selector requires only one filesystem finding, already supplied
by the underlying atoms; the minimized-import consumers target PE files,
which are outside the relocated rules' scope.

Version comparison: fetched upstream git tags 4.1.13 and 5.12.1. The former
uses settings-controlled Tauri autostart enable/disable. The Go rewrite
reimplements that feature. Commit 52db77fa26148e88cb0cce283f66f72d96641fd7
replaces an invalid text .lnk with WScript.Shell/PowerShell creation; commit
c7b4289ab0852b4c942451e04caeb65fff7249e9 adds the backend argument.
The supplied HEAD update-settings.go is byte-identical to tag 5.12.1.
Autostart targets the current application, is gated by a settings transition,
and removes the shortcut when disabled. The API validates the configured token.
The sample is benign; archive JSON verification has zero hostile and zero
suspicious traits. No software-name exclusion was added.
