# Triage Status & Remaining Work (`/x-triage-bad /var/tmp/gauntlet-triage/probable-hostile`)

## 1. Completed Work

### Previous Task (`/x-triage-good /var/tmp/gauntlet-triage/probable-benign`)
- Completed triage of all 11 files in `/var/tmp/gauntlet-triage/probable-benign/manifest.tsv`:
  - 10 benign samples verified (`H=0, S<=1`, no misleading traits) and moved with `hopper mv -target=good`.
  - 1 misplaced sample (`272f1315-14d7-458c-a4ca-e2df423490b4._vbs`, SHA256 `aafbc096e20f259df9166f837d0baf7333f177e6f383ca7cb9215936ecbe7f5e`) given 3 `crit: hostile` traits across 3 directories, copied to `/tmp/triage/misplaced-bad`, and moved with `hopper mv -target=bad`.

### Batch 1: Standalone Scripts (19 / 315 samples — `.ps1`, `.py`, `.sh`, `.zsh`, `.js`) — DONE
- Added/updated rules across 18 YAML files and validated with `make validate`.
- **3 Misplaced Benign (`good`)** (copied to `/tmp/triage/misplaced-good/` and moved with `hopper mv -target=good`):
  - `2156893662-docs_offline_iframe_api_bin.js` (`afac5c6c06b1a932dbcd746fee506be3f6c6dee62545532c31481c6e881740a0`)
  - `install_panel.sh` (`18ab51b6e4d3bb914579a2e87d2f099997574f18b320cf5ab07602b5db6ab19f`)
  - `win64.ps1` (`15a8037f8636d125642676014107ecbb7794ee3a2d3d539aa3096f18241d8756`)
- **16 Confirmed Hostile (`bad`)** (all verified with `H >= 3` across `>= 3` directories and moved with `hopper mv -target=bad`):
  - `script.ps1` (`54d112d07958...`), `pk.ps1` (`698e021b00eb...`), `securedb_stub.ps1` (`ca4024f1a8dc...`)
  - `mbupload-bin49cbw.py` (`8bf95863ec87...`), `main.py` (`73230d494925...`)
  - `rondo.bbk.sh` (`0da7c3d3f9fa...`), `sh.zsh` (`12ebad43eb52...`), `mbupload-sbbj57fb.zsh` (`f91746427929...`)
  - `index.js` (`ec8c8cc8120e...`), `test.js` (`59fc909b578c...`), `6f8211be...js` (`6f8211be7079...`), `6851610c...js` (`6851610cf955...`), `27bdbe2f...js` (`27bdbe2fb555...`), `d255e7de...js` (`d255e7de4b40...`), `3be83f5b...js` (`3be83f5bede5...`), `fb0b1448...js` (`fb0b1448dd02...`)

---

## 2. In-Progress Work: Batch 2 (45 Native Binaries, Installers & `.vir` files)

### A. Misplaced Benign (`good`) in Batch 2 (13 samples)
All 13 samples have been inspected:
- **12 already have `H=0, S<=1`** (verify no misleading `notable`/`baseline`/`component` traits before moving to `good` and copying to `/tmp/triage/misplaced-good`):
  1. `EqualizerAPO-XT-Setup.exe` (`3a547db56b607bf1845c74f13dd39736841082a550019de038d97aea9e944337`) — `H=0 S=0` (legitimate EqualizerAPO-XT installer)
  2. `36febbaaee18944359bad74a574204089838cc3642ab410d6a237da2fd4ccc2c` — `H=0 S=0` (`qqpet-relay-bridge.zip` LAN-to-MQTT game bridge)
  3. `zapret-discord-youtube-1.10.2.rar` (`d9a57ab8254f1f8daa1c382736d7cd6ae60e5dbe128138844c3cf04648228330`) — `H=0 S=1` (`sc-create-start-sequence`, DPI bypass utility)
  4. `b6fc79eb75ec31ecfcd05fdca6efd198882f198eb67e0ce781b471c5e04d39f4` — `H=0 S=0` (non-functional toy `.bat` file)
  5. `fc91000a99bfacbc13b07f21b0023e4e4117a7f13afcafc397034c2ddd37056b` — `H=0 S=0` (benign CTF `crackme.pyc`)
  6. `virussign.com_0f3a0b504c4a1ff46e1b2fe8b31ad0c0.vir` (`d842d5f301c5...`) — `H=0 S=0` (`skin_face_v2_20240828.model` zip)
  7. `virussign.com_0d2ac483ce3e2190c146c9ad18913750.vir` (`0e213c3bdc50...`) — `H=0 S=0` (gzipped Amazon.it HTML page)
  8. `virussign.com_84a15af3dd065f5ce6683c78a6287f00.vir` (`a6e6187b9983...`) — `H=0 S=0` (Ren'Py `renpy.compat` `.pyc`)
  9. `virussign.com_0ba27def95a1c705e6f9dedd9e28c100.vir` (`e5e7b2614761...`) — `H=0 S=0` (`rensa-0.5.0` wheel)
  10. `virussign.com_825e41b855aeb69603989d2f663d5690.vir` (`518e5ceea9f8...`) — `H=0 S=0` (website HTML with Kint debugbar)
  11. `virussign.com_e801dcdd7f6b2946ac29e6d6a2c1bbb0.vir` (`0170f815271e...`) — `H=0 S=0` (`White Page India` HTML)
  12. `virussign.com_028a0a867cd59d1dbce8fc80bece0010.vir` (`b86dda7b9081...`) — `H=0 S=0` (gzipped `Victory Electronics` HTML)
  13. `virussign.com_0fec9ee5b04e4469887c59fa9e6753d0.vir` (`a9873f499d43...`) — `H=0 S=0` (gzipped corporate HTML)
- **1 benign sample needs FP reduction (`H=0 S=2` -> `H=0 S<=1`)**:
  14. `af4bf1720937874ad837c291a74c84d70881a86ee6e33d3b44e3b152c7cc77a3.exe` (`Botzilla.exe` — legitimate 6 MB Botzilla Studio v0.72 RPA/browser automation IDE):
      - Currently matches `metadata/file/profile/process/hidden::dotnet-dense-network-hidden-child-profile` (`S`), `objectives/anti-static/obfuscation/reflection/invoke::dotnet-reflection-write-child-profile` (`S`), and `objectives/impact/ui/manipulation/ad-fraud::embedded-browser-script-injection` (`N`).
      - **Fix needed**: Exclude large UI-rich .NET applications (`metadata/file/profile/string-population::native-string-over-256-kib` or `size_max`) on those `.NET` profile rules, and downgrade `embedded-browser-script-injection` / `shell-explorer-browser-control` in `objectives/impact/ui/manipulation/ad-fraud/windows-native.yaml` to `crit: component`.

### B. Dual-Use (`dual`) in Batch 2 (3 samples)
1. `2d2b32c115c606e33cabd48e0b132e5515fd7bb33827ad17191fb37356a121b9` — `H=0 S=2` (`github.com/Autumn-27/artex` security assessment CLI) -> ready for `hopper mv -target=dual`.
2. `0122c998f7c99de562fdae27ef486c6653544e89e15963b67d3418fe7f92c73e.exe` — `H=0 S=7` (`ScreenConnect.ClientSetup.exe` pre-configured unattended installer) -> ready for `hopper mv -target=dual`.
3. `wafaction1.msi` (`5c97104e2e1c354d2001fa5ce026fe899e91ee88a73516a7f659f6a7f068180d`) — signed Action1 RMM Agent MSI (`H=1 S=1`):
   - **Fix needed**: Add `- id: well-known/dual-use/remote-admin/action1::action1-version-resource-context` to `unless:` of `window-hook-thread-dll-injector` in `objectives/execution/payload/process-inject/dll-load/window-hook-dll-injection.yaml` so `action1_remote.exe` does not trigger a `hostile` DLL-injection FP, then move with `hopper mv -target=dual`.

### C. Confirmed Hostile (`bad`) in Batch 2 Already at `H >= 3` (16 samples)
- `nix-update` (`39757ff17030...`) — `H=4(d=2)` (garble-obfuscated Go yamux/uquic agent)
- `macho_eb38f2f91b58.bin` (`eb38f2f91b58...`) — `H=6(d=3)`
- `65f7b9d663b9...` (`65f7b9d663b9...`) — `H=3(d=3)`
- `2026-10-30_4b80f355...` (`e4b7804f8a6f...`) — `H=3(d=3)`
- `2026-11-01_bf0dfd0f...` (`98a45cd8b9c8...`) — `H=5(d=4)`
- `2026-10-22_10d87b73...` (`7a469b572de1...`) — `H=5(d=4)`
- `1a7f0e2e962a...` (`1a7f0e2e962a...`) — `H=4(d=3)`
- `deathstar.mipsel` (`1f4073e35d78...`) — `H=3(d=2)`
- `deathstar.m68k` (`06c75b58e566...`) — `H=3(d=3)`
- `d872e02c03b4...` (`d872e02c03b4...`) — `H=3(d=2)`
- `d95938132917...` (`d95938132917...`) — `H=3(d=2)`
- `deathstar.powerpc` (`64d441263415...`) — `H=3(d=2)`
- `deathstar.mips` (`4cd746c8908f...`) — `H=3(d=2)`
- `0d23bcb2e85e...` (`0d23bcb2e85e...`) — `H=3(d=2)`
- `tadashi.arm4` (`7026dd6d82af...`) — `H=3(d=1)` (add multi-directory rule alongside `tadashi.arm64`)
- `tadashi.arm6` (`48b493ecfffa...`) — `H=3(d=1)` (add multi-directory rule alongside `tadashi.arm64`)

### D. Confirmed Hostile (`bad`) in Batch 2 Needing Rule Additions (`H < 3`) (12 samples)
1. `who-r-u0000.bin` (`55f688a2084e...`) — `H=2(d=2) S=1` (7z containing pickle reverse shell; promote/add 1 `crit: hostile` trait in another directory).
2. `cd578333a4be...` (`cd578333a4be...`) — `H=1(d=1) S=0` (Python `ctypes.pythonapi.Py_GetArgcArgv` + devnull redirection + `runpy.run_path` `.so` loader; add 2 `crit: hostile` traits in other directories).
3. `database.ser` (`c9018dd5dbb9...`) — `H=0(d=0) S=0` (Java serialized CommonsCollections4 + AspectJ `SimpleCache$StoreableCachingMap` gadget dropping JSP webshell; add 3 `crit: hostile` traits across 3 directories).
4. `tadashi.arm64` (`c1839b85d724...`) — `H=2(d=1) S=1` (ELF aarch64 botnet binary; add 1+ `crit: hostile` trait in another directory).
5. `bot_riscv64` (`c452aa71a7e8...`) — `H=1(d=1) S=4` (ELF RISC-V Go IRC agent; promote/add 2 `crit: hostile` traits in other directories).
6. `mbupload-oa0493qn.bin` (`453505bf331a...`) — `H=1(d=1) S=0` (ELF Renesas SH Mirai `dvrHelper` HTTP downloader stage; add 2 `crit: hostile` traits in other directories).
7. `mbupload-b9kcd0z1.bin` (`01c97268134b...`) — `H=0(d=0) S=1` (ELF x86-64 multi-vector flooder `native-multivector-flood-worker-symbols`; add 3 `crit: hostile` traits across 3 directories).
8. `macho_a9cd105e5cdf.bin` (`a9cd105e5cdf...`) — `H=1(d=1) S=2` (Mach-O universal binary masquerading as `com.apple.authorization` with `packed-sparse-command-runner`, `elapsed-time-key-corruption`, `export-trie-name-hash-resolution`; add 2 `crit: hostile` traits in other directories).
9. `ccfd73a74d88...` (`ccfd73a74d88...`) — `H=0(d=0) S=0` (static ELF x86-64 UDP packet flooder; add 3 `crit: hostile` traits across 3 directories).
10. `My 2FA KeyX.exe` (`137378852feb...`) — `H=0(d=0) S=0` (trojanized Go Wails `twoFA_modern` app with `main.AddrFromKey`, `main.maskToRegex`, `main.decodeProductState`, `main.RunMeElevated`, `main.Rundll32`, `main.launchDetached`; add 3 `crit: hostile` traits across 3 directories).
11. `2026-10-15_9d2685a6...` (`95c8a06e6b51...`) — `H=0(d=0) S=1` (Win32.Sality polymorphic file infector with executable `.reloc` section on PyInstaller binary; add 3 `crit: hostile` traits across 3 directories).
12. `cf_bypass.x86_64` (`b717c915ae68...`) — `H=0(d=0) S=0` (Go HTTP flooder with `main.floodWorker` + `bogdanfinn/tls-client` + `bogdanfinn/utls` + `bdandy/go-socks4`; add 3 `crit: hostile` traits across 3 directories).

---

## 3. Remaining Batches After Batch 2 (251 samples)

- **Batch 3: Smaller Package Ecosystems (25 samples)**
  - `.gem` (5), `.nupkg` (6), `.crate` (7), `.jar` (5), `.apk` (2)
- **Batch 4: `.zip` & `.tar.gz` Archives (29 samples)**
  - `.zip` (22), `.tar.gz` (7)
- **Batch 5: Python Wheels (62 samples)**
  - `.whl` (62)
- **Batch 6: Chrome Extensions (66 samples)**
  - `.crx` (66)
- **Batch 7: npm Packages (69 samples)**
  - `.tgz` (69)
