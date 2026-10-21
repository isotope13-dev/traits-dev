# Startup-copy and targetless shortcut review

All three supplied samples are **BENIGN** on their available bytes and context.
No deployment history or externally verified publisher was supplied. These are
minimal, test-like artifacts; the ML verdict is not behavioral evidence.

## Sample behavior

- `e91111877cc453f77210d5ee552134d313764c4881d5f4634fa8c4c7a34ef443`:
  `copy-into-startup.bat`, 80 bytes. Its complete execution path is
  `copy "%~f0" "%APPDATA%\Microsoft\Windows\Start Menu\Programs\StartUp\agent.bat"`.
  `%~f0` resolves the current batch file, and `%APPDATA%` selects the current
  user's roaming data directory. This installs this same one-command script
  for execution at login. The installed copy subsequently tries to copy itself
  onto itself. There is no other payload, branch, download, collection,
  destruction, hidden command, or interpreter stage. Autorun capability is
  real, but copying an otherwise inert script does not establish an attack.
- `c8ccd904e2ad84bf5bfbca2205e473e9d0981295b946c26c5bc501f14f6de921`:
  `without-startup.zip`, 627 bytes, contains only the two members below.
- `a4d00b45b2c7e8680af92e9fabb4d8d53a003c6dda80f1a967a4ff1e6f28dfc1`:
  `without-startup.zip`, 627 bytes. Same member bytes as the preceding archive;
  the outer ZIPs differ at four timestamp bytes only.

Each archive's `launch.lnk` is 404 bytes, SHA-256
`b6016f58f61eca35c953283c6041433f9decfce93b46c753b850f807ba326cf8`.
The 76-byte Shell Link header has the correct CLSID, flags `0xa0`
(`HasArguments | IsUnicode`), and ShowCommand 0 (hidden). Its only StringData
field is the 161-character UTF-16LE argument field. The file ends immediately
after that field and the four-byte zero terminal block. It has no target IDList,
LinkInfo, relative target path, environment target block, icon, or embedded
archive. UTF-16LE is the declared string representation, not an obfuscation
layer.

The argument field is:

```text
/c conhost --headless cmd /c tar -xf "%TEMP%\inner.zip" -C "%TEMP%" settings.ini && copy "%TEMP%\settings.ini" "%TEMP%\runner.bat" /y >nul && "%TEMP%\runner.bat"
```

If handed to a suitable shell by additional context, these arguments request
headless command execution, extract `settings.ini` from a local temporary ZIP,
copy it to `runner.bat`, suppress COPY output, and run it only if extraction
and copying succeed. The shortcut supplies no target to receive these arguments.
Neither `inner.zip` nor `settings.ini` is supplied. The other member,
`stage.txt`, is exactly the 11 bytes `@echo off\r\n`, SHA-256
`c134b2f85415ba5cfce3e3fe4745688335745a9bb22152ac8f5c77f190d8aee3`.
It only disables batch command echoing and is not referenced by the shortcut.
There is no complete runnable payload chain or concrete hostile effect.
The command-shaped argument observations and extension mismatch remain useful
notable facts. A valid external target and an external payload would require
separate review; their contents must not be invented.

## Trait changes and placement

- Move `objectives/persistence/login/startup/folder::batch-copy-self-to-startup`
  to `micro-behaviors/os/autorun/login-items::batch-self-copy-startup-reference`.
  Preserve its matcher, confidence and Windows/batch scope; use notable
  severity and describe command/path evidence without unwanted persistence.
- Remove `batch-self-copy-startup-folder` from the former objective directory:
  it adds only a Startup path already required by the moved atom. This
  consolidates a redundant hostile classification without losing the behavior.
- Move `objectives/persistence/login/startup/folder::batch-copy-to-startup-folder`
  to `micro-behaviors/os/autorun/login-items::batch-copy-startup-reference`.
  Preserve its two required observations, scope and confidence; describe their
  co-occurrence and use notable severity. Update its shutdown consumer.
- Move `objectives/persistence/login/self-install/script::batch-self-install-appdata`
  to `micro-behaviors/fs/path/script::batch-self-input-appdata-transfer-context`.
  Its required self-path input and AppData COPY/MOVE command can be unrelated;
  they establish neither a bound self-copy nor a login trigger. Preserve its
  conditions and scope, describe the self-path context accurately, remove
  unsupported persistence mappings, and use notable severity. Update all five
  consumers without altering their other required evidence.

Exact consumers and ancestor selectors were audited. There are no ancestor
selectors of either retired objective leaf or either new capability leaf.
The broader `micro-behaviors/fs/` consumers are restricted to PE or PowerShell,
so the added batch-only self-path context cannot broaden them.
No dependency, filename, hash, or specimen-specific exception was introduced.
The shortcut traits require no changes.

## Verification

`atomscan <path>` and `cleave facts <path>` were run for each original, with
additional facts and byte-level header parsing for both shortcuts. ZIP member
hashes, contents, sizes, flags, StringData lengths, terminal blocks and the
four differing archive offsets were checked without executing sample commands.

After edits, all originals were rescanned with `CLEAVE_TRAITS_DIR` pointing
at this checkout and `--no-update --format json`. The batch has 13 notable
traits and no suspicious or hostile traits. Each ZIP retains 15 notable
aggregate traits, including 13 on its shortcut and one on `stage.txt`, with
no suspicious or hostile traits. Model probabilities do not decide this review.

The seven controls in `check.py` pass: self-copy, ordinary Startup installation,
unrelated copy, AppData copy, separate self-input and AppData operations,
path-only reference, and the preserved hostile Startup-plus-shutdown consumer.
The existing 26 cases in `../first-reasoned-review/check.py` also pass,
including renamed carriers, targetless and valid-target links, missing chain
operations, distinct source/sink paths, normal windows and archive variants.
