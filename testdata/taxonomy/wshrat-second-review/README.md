# WSHRAT second review

Sample: `stage2.js`, SHA-256
`67575637a4eb7a3da0b33247960a0531b41cf4d547c7d664a91d3811b4c098f8`.
Verdict: **MALICIOUS**, based on the script's execution paths.

The source is readable Windows Script Host JScript, with no encoded payload
or obfuscation layer. Facts reported no parser errors or decoded text layers.
Its own registration identifies it as WSHRAT. No registry provenance, scanner
score, external advisory or presumed downloaded-plugin behavior establishes
the verdict.

## Verified behavior

- `instance()` calls `upstart()`, which copies the running script into AppData
  and Startup and registers `wscript.exe //B` launches in HKCU/HKLM Run keys.
- Every loop calls `install()`. On writable, ready removable drives
  (`DriveType == 1`), it copies itself, sets hidden/system attributes, hides
  original files/folders and creates lookalike shortcuts. Each shortcut runs
  the script before opening the original file or folder, retaining its icon.
- The five-second polling loop posts to `http://james1919.ooguy.com:7044/is-ready`.
  Server responses are split into tasks. `excecute` evaluates supplied source;
  `cmd-shell` runs supplied command text hidden, reads redirected output and
  posts that output back. Download commands save response bodies and run the
  saved executable. Process enumeration and log-file upload also return data.
- Check-ins carry a machine profile in the User-Agent header: disk serial,
  computer/user names, OS, antivirus inventory and USB propagation status.
- `get-pass` downloads a tool, runs `/stext` to produce a data file, then uploads
  that file. Keylogger, file-manager and remote-desktop tasks download and
  launch external plugins. This script does not implement their internal
  credential extraction, keyboard capture or desktop protocol.
- With the `elevated` argument, `disable-uac` writes zero to HKLM's `EnableLUA`
  and `ConsentPromptBehaviorAdmin`. These are policy weakening operations;
  they do not establish an elevation exploit. `elevate` currently fails at
  `oneonce.close()` because `instance()` shadows that global with a local
  variable, so the following consent-based ShellExecute request is not reached.

The source was also evaluated in QuickJS with mocked WScript/COM/filesystem,
WMI, network and process objects. No real network or process operations ran.
Separate task responses confirmed evaluation, shell output return, USB lures,
policy writes, file download/launch, password-tool result upload, plugin
launch, process return, log upload and the broken elevation path. Success on
a real host still depends on permissions, installed COM components, network
availability and external payloads.

## Detection changes

WSHRAT identity is consolidated from `backdoor/wshrat` and `rat/houdini` into
`rat/wshrat`, using two distinctive command sequences plus WSH, HTTP POST and
dynamic-evaluation context. Generic Startup lookup, splitter names, command
verbs and lone request labels no longer emit family-identity findings.
Renaming a variable or registration label does not defeat the identity.

Startup resolution is consolidated into `fs/path/autostart`, retaining the
union of JavaScript/VBScript/HTML and whitespace spellings; exact consumers
now reference it there. The Win32 WQL observation no longer claims browser
execution. Repeated RegExp construction no longer claims distinct patterns,
and the HTTP prefix/shutdown names describe only their matched operations.
The unbound `Type = 1` fragment now lives under property assignment; only its
ADODB-context composite makes a stream claim.

UNC paths now start at the beginning of a literal, avoiding WMI monikers.
SecurityCenter WQL is excluded from SQL detection. A remote `keylogger` verb
no longer implies a global keyboard listener. ShellExecute is covered by its
desktop-opener traits rather than the executable-image API matcher.
Two call-site-specific rules cover the previously missed UAC policy writes,
requiring the HKLM hive, exact policy path, value name and zero value together.

Run `python3 testdata/taxonomy/wshrat-second-review/check.py` for the focused
controls. The existing first-review controls also exercise the consolidated
identity and its renamed-registration near miss.
