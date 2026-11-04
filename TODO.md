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

## 5. Completed Work: Batch 5 (Python Wheels — 62 `.whl` samples) — DONE

- **35 Misplaced Benign (`good`)**: Verified `0H 0S/1S 0 Obj-N` with no misleading findings, copied to `/tmp/triage/misplaced-good/`, and moved with `hopper mv -target=good` (`airbyte_agent_sdk`, `aweb`, `claudecord`, `dashscope`, `elitea_sdk`, `fbuild`, `fontcase`, `luckee_cli`, `moveworks_capi_starter`, `ok_script`, `pirlygenes`, `skills_analyzer`, `splogo`, `stdid_nyxprobe`, `test_workalendar_internal`, `upgini`, `uprobe`).
- **27 Confirmed Hostile (`bad`)**: Verified with `H >= 3` across `>= 3` directories and moved with `hopper mv -target=bad` (Cluster A 11 wheels: `acousticpack`, `asrloom`, `benchworks`, `hookgantry`, `modelworks`, `phonemeforge`, `phonemeprobe`, `soundsocket`, `ttsdock`, `ttsprobe`, `ttsweaver`; Cluster B 7 wheels: `badgertask`, `brambletask`, `brookworker`, `ferretqueue`, `flintqueue`, `larchworker`, `sedgehaul`; Individual families: `fontus`, `gcpwn`, `myra_ai_assistant`, `pafex`, `pyprig`, `resion`, `suggestedtests`, `wallet_tracking`).
- **Engine Bug Fixed**: Fixed `filefacts` Python comment-run `O(K^2)` lexer-budget exhaustion so Python files padded with thousands of `#` comment lines (`splogo-1.0.0-py3-none-any.whl`) parse completely within the tree-sitter lexer budget.

---

## 6. Completed Work: Batch 6 (Chrome Extensions — 66 `.crx` samples) — DONE

- **49 Misplaced Benign (`good`)**: Verified `0H, S<=1, 0 Obj-N` with no misleading findings, copied to `/tmp/triage/misplaced-good/`, and moved with `hopper mv -target=good`.
- **2 Dual-Use (`purgatory`)**: Commercial WhatsApp Web CRM bulk-messaging extensions (`mcfhdbbdcaodbaacopebdkhhogjcaieh.crx` / Izza Bot and `nblcdphhoppanhfnllcbnbbfjnlbknfd.crx` / Wasubot) verified `0H` and moved with `hopper mv -target=purgatory`.
- **15 Confirmed Hostile (`bad`)**: Verified with `H >= 3` across `>= 3` directories and moved with `hopper mv -target=bad` (`ddfdfoaikdeokhfibfkpffonpllddaid.crx`, `acjjhchnekkooeidcjnjpciangnmokgp.crx`, `cchjdbddjikkeeaddghohjljhabbgdfd.crx`, `daabfdbfadnbojjkbbjmegledncaaedl.crx`, `djnpebcpfhbelkdkokmbihhlcdcmbcng.crx`, `dpamgbfmlcbabkbbebemijabckmkffdc.crx`, `fneececehejpknbfdekbjpldplfdllab.crx`, `gihepmncbdnpfdffnbhbkkckffhlkblb.crx`, `hmkdkkmjnhdkbfnheamkefidnbgnhcdj.crx`, `ibnkknhclojkijdeebfhgehmfgkgnmnn.crx`, `jjkmpmebdfbhnlldhknbmpjknidmbnpl.crx`, `maedccdnebfefdjcbebghhcfefknidpf.crx`, `nbjdhgkkhefpifcaechbfdaefacfbndf.crx`, `mlifbfhhhlokpmlbadikcfbdfefpfcbm.crx`, `nnhpfknljdpmfeigdaefebbhbechbdpf.crx`).

---

## 7. Completed Work: Batch 7 (npm Packages — 69 `.tgz` samples) — DONE (ALL 315 / 315 SAMPLES COMPLETE)

- **39 Misplaced Benign (`good`)**: Verified `H=0, S<=1, ObjN=0` with no misleading findings, copied to `/tmp/triage/misplaced-good/`, and moved with `hopper mv -target=good` (`coderabbit-0.9.{1,2}.tgz`, `sentencex-win32-x64-1.0.33.tgz`, `chutes-build-win32-x64-2.0.{1,2,8,10}.tgz`, `watchmen-cli-win32-x64-3.0.{0,4}.tgz`, `mq-bridge-win32-x64-msvc-1.3.0.tgz`, `paidwithtab-3.0.0.tgz`, `git-span-win32-x64-1.1.{47,48}.tgz`, `executable-stories-playwright-8.15.0.tgz`, `hexo-theme-linen-1.0.45.tgz`, `free-email-domains-1.9.9.tgz`, `@retailrocketgroup-retailrocket-edit.abandoned-view-vue-email-template-render-11.0.433449.tgz`, `hyperframes-{0.7.10,0.8.5}.tgz`, `@bobfrankston-mailx-store-web-0.1.133.tgz`, `@ppa-web-components-ppa-searchform-0.1.0.tgz`, `trustlint-2.2.0.tgz`, `foremerge-win32-x64-0.6.0.tgz`, `cmdly-0.2.1.tgz`, `@gowri48-npmpublish-2.1.7.tgz`, `@stefanosala-vc-cli-linux-x64-0.1.0.tgz`, `mega-code-dev-0.5.2.tgz`, `@lightdash-cli-2.618.0.tgz`, `suppa-mcp-2-1.43.0.tgz`, `@reason-machines-cli-linux-{arm64-0.2.333,arm64-musl-0.2.306,x64-musl-0.2.290,x64-0.2.290}.tgz`, `@telora-mcp-products-0.23.5.tgz`, `@beloved-lenora-opencode-shared-rpc-1.0.0.tgz`, `@toptal-davinci-graphql-codegen-extensions-2.0.0.tgz`, `worsier-win32-x64-msvc-3.10.0.tgz`, `@devflow-tools-devflow-0.18.60.tgz`, `hugo-bin-0.166.0.tgz`).
- **5 Suspicious / Carrier Packages (`purgatory`)**: Verified `H=0, S=2, ObjN=0` and moved with `hopper mv -target=purgatory` (`dependencykfeg-25.1.3.tgz`, `atlassian-wallboard-plugin-10.0.0.tgz`, `@chatunity-baileys-1.2.2.tgz`, `@flexmr-survey-client-2.0.12.tgz`, `@flexmr-survey-conversation-1.0.12.tgz`).
- **25 Confirmed Hostile (`bad`)**: Verified with `H >= 3` across `>= 3` directories and moved with `hopper mv -target=bad` (`litecore-lib-ltc-1.9.{8,14}.tgz`, `spectral-core-3.0.5.tgz`, `@johnruff215-dev-solana-wallet-tracker-1.0.1.tgz`, `@ifasn-mmdd-doc-mcp-1.1.0.tgz`, `tw-motion-css-2.0.2.tgz`, `raiden-baileys-2.1.4.tgz`, `itsa-react-button-16.0.11.tgz`, `@goparrot-dashboard-combos-0.0.1.tgz`, `@atedone-workspace-context-0.0.{16,22}.tgz`, `@majapisoftwares-router-0.2.0.tgz`, `@zervonex-baileys-3.0.8.tgz`, `scdn-jquery-0.1.6.tgz`, `@axon-web-icons-1.0.1.tgz`, `konnektive-one-1.6.1.tgz`, `@conduitops-logview-archive-1.0.1.tgz`, `@elfhkry666-baileys-0.3.{20,23,24}.tgz`, `@pisell-pisellos-2.3.176.tgz`, `@jexkcode-baileys-1.1.5.tgz`, `animatecss-tailwind-presets-1.0.0.tgz`, `animatecss-tailwind-luminary-2.0.6.tgz`, `akuuong-1.0.0.tgz`).
