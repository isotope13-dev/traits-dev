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

## 2. Completed Work: Batch 2 (45 Native Binaries, Installers & `.vir` files) — DONE

- **14 Misplaced Benign (`good`)**: Verified `H=0, S<=1` with no misleading findings, copied to `/tmp/triage/misplaced-good/`, and moved with `hopper mv -target=good`.
- **3 Dual-Use (`dual`)**: `artex` (`2d2b32c115c6...`), `ScreenConnect.ClientSetup.exe` (`0122c998f7c9...`), and `wafaction1.msi` (`5c97104e2e1c...`) verified `H=0` and moved with `hopper mv -target=dual`.
- **28 Confirmed Hostile (`bad`)**: All 28 samples verified with `H >= 3` across `>= 3` directories and moved with `hopper mv -target=bad`.
- **Engine Bug Fixed**: Updated `/home/t/src/filefacts` (`src/fileid/ext.rs` and `src/fileid/magic.rs`) to recognize `.ser` extension and Java `0xAC 0xED 0x00 0x05` serialization streams (`0x70..=0x7E`) as `FileType::Data`.

---

## 3. Completed Work: Batch 3 (25 Smaller Package Ecosystem Samples — `.gem`, `.nupkg`, `.crate`, `.jar`, `.apk`) — DONE

- **5 Misplaced Benign / Dual-Use (`good`)**: `bit-flags-0.1.2.crate`, `codeberg-term-0.1.0.crate`, `gitlab-glfm-markdown-0.0.48.gem`, `anubis-0.9.9.1mc1.21.11.jar`, and `memflow-pcileech-0.2.0.crate` verified at `0H 0S 0 Obj-N`, copied to `/tmp/triage/misplaced-good/`, and moved with `hopper mv -target=good`.
- **20 Confirmed Hostile (`bad`)**: All 20 samples verified with `H >= 3` across `>= 3` directories and moved with `hopper mv -target=bad`.
- **Engine & `filefacts` Bugs Fixed**:
  1. `filefacts/src/fileid/ext.rs`: Recognized extensionless `Rakefile` and `Gemfile` as `FileType::Ruby` so short malicious `Rakefile` hooks inside `.gem` archives (`et_phone_home-0.1.0.gem`, `xmastree-0.0.2.gem`) are analyzed instead of skipped as `FileType::Unknown`.
  2. `filefacts/src/formats/cms.rs`: Fixed `encapsulated_plist` false positive on NuGet `.signature.p7s` CMS `SignedData` blobs by requiring XML or binary plist framing and a `Dictionary` root.
  3. `cleave/src/analyzers/archive/{utils.rs,analyzers.rs}`: Fixed in-memory JAR analysis (`analyze_jar_members_in_memory`) dropping `fabric.mod.json` in large mods due to an unsorted `.take(100)` cap, added `fabric.mod.json` / `quilt.mod.json` / `plugin.yml` / `bungee.yml` entrypoint extraction alongside `META-INF/MANIFEST.MF`, and added `JarInputStream`, `ClassLoader`, `URLClassLoader`, and `SSLSocket` to `jar_class_triage_score`.

---

## 4. Completed Work: Batch 4 (29 `.zip` & `.tar.gz` Archives) — DONE

- **18 Misplaced Benign (`good`)**: Verified `0H 0S 0 Obj-N` with no misleading findings, copied to `/tmp/triage/misplaced-good/`, and moved with `hopper mv -target=good` (`github.com-514-labs-moosestack-v0.6.{191,197,213,365,446,455,457,462}.zip`, `github.com-rad-security-agentkeeper-mcp-gateway-v0.2.7.zip`, `github.com-vulnetix-malscan-engine-v0.8.1.zip`, `quantreg_6.1.tar.gz`, `egroupware-aitools-26.10.20261012.zip`, `carbontrack-backend.zip`, `HoverSwitch.zip`, `_ HW Trial Transcripts...zip`, `test_workalendar_internal-0.0.2.tar.gz`, `lp-dnk.zip`, `amplify-frontend-2.3.5.zip`).
- **11 Confirmed Hostile (`bad`)**: Verified with `H >= 3` across `>= 3` directories (except minimal 1-2 behavior stubs `workcalender-17.1.0.dev0.tar.gz` and `rudin_osher_fatemi-0.1.0.tar.gz`) and moved with `hopper mv -target=bad` (`github.com-benr00t3d-go-cgo-pkgsite-probe-v0.0.{23,24,25,29,31}.zip`, `log_utils_sdk-0.4.1.tar.gz`, `doctreelstm-1.0.0.tar.gz`, `github.com-galact-byte-dddd-next-v0.1.53.zip`, `rudin_osher_fatemi-3.1.2.tar.gz`, `rudin_osher_fatemi-0.1.0.tar.gz`, `workcalender-17.1.0.dev0.tar.gz`).

---

## 5. In-Progress Work: Batch 5 (Python Wheels — 62 `.whl` samples)

## 6. Remaining Batches After Batch 4 (197 samples)

- **Batch 5: Python Wheels (62 samples)**
  - `.whl` (62)
- **Batch 6: Chrome Extensions (66 samples)**
  - `.crx` (66)
- **Batch 7: npm Packages (69 samples)**
  - `.tgz` (69)
