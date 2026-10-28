# Gauntlet missed samples: review in progress

140 samples received separate fresh local scans with `--mode slow --analyze local --follow=none` and workspace traits. Scan completion is not a completed manual verdict. Baseline counts precede the rule corrections recorded below.

Raw scan summaries, archive indexes, extracted sources and facts are stored under `/tmp/gauntlet-missed-review/`, keyed by SHA-256. Samples were not executed. Labels have not yet been moved.

## Corrections under review

- Serialized Java/JSP command implant: expanded the neutral Java webapps path observation to include JSP/data/text and added a hostile exploit composite. Targeted scan confirms the new match.
- Hollow npm host survey: relocated the generic behavior to micro-behaviors; added a parsed console-call disclosure fact and a suspicious dependency-confusion PoC composite.
- Relabeled `http-compile-exec.py` from hostile to suspicious: its only behavior is an explicit `load(url)` function fetching and evaluating caller-selected source; it has no import-time trigger, fixed hostile destination, or malicious payload.
- Caller-selected Python remote job runners: moved generic download/child-interpreter and fetched-source execution from hostile objectives to suspicious capabilities; removed a duplicate staged-child verdict.
- Font/host census sent through a quick tunnel: suspicious reporting boundary, without proof of unauthorized collection.

## Outstanding work

- Two JavaScript samples have now been decoded independently: `6baed65e86355ac0.js` and `0c76358cf582c52e.js` contain the same XOR-28/Base64 hidden full-window security-check iframe stage.
- Complete per-member manual reviews for rows marked pending; archive/background indexes alone do not resolve a sample.
- Confirm final matches after the current rule edits.
- The dummy-package, calendar-build and unsafe-pickle precision issues are addressed in [improvements.md](improvements.md).
- Investigate filefacts misidentifying tab-indented decoded Python as Makefile; the reproducible artifact is `resion/decoded-final.py` under its hash directory.
- Final validation now passes; Hopper moves and the remaining manual reviews are still pending.

## Sample ledger

| Sample | Baseline H/S | Review | Provisional pool | Evidence / remaining work |
|---|---:|---|---|---|
| @elfhkry666-baileys-0.3.20.tgz | 5/1 | pending-manual-review | pending |  |
| @jexkcode-baileys-1.1.5.tgz | 1/1 | pending-manual-review | pending |  |
| resion-22.0.1-py3-none-any.whl | 4/1 | payload-decoded-static | bad | Verified checksum/length of default.config, decompressed XZ, inspected pickle opcodes with pickletools (no pickle.loads), decoded Base64 and XOR stages. Payload writes pywild/__init__.py and __cached__.py plus pyc_abi3-cross.pth importing pywild. Inner code launches hidden children, fetches encoded Python, and on Linux uses memfd and execve. Decoded evidence under /tmp/gauntlet-missed-review/<sha>/resion/. |
| test_workalendar_internal-0.0.1-py3-none-any.whl | 0/0 | source-reviewed | good | Weekday calculation and CLI only; sdist build hook prints a message. No network, process-launch, or payload behavior in the shipped source. |
| pafex-2.3-py3-none-any.whl | 1/0 | source-and-facts-reviewed | purgatory | The config loader calls pickle.loads before testing the result type. Relocated the unsupported hostile package claim to a suspicious unsafe-deserialization capability; current result is 0H/1S. |
| Gooba-Client.jar | 3/2 | pending-manual-review | pending |  |
| workcalender-17.1.0.dev0.tar.gz | 0/2 | source-and-facts-reviewed | good | Weekday calculation and a print-only Hatch hook. Name spelling, toolkit description, and unpublished-test claims are retained as neutral metadata. Current result is 0H/0S; pool change is not yet applied. |
| test_workalendar_internal-0.0.2.tar.gz | 0/0 | source-reviewed | good | Weekday calculation and CLI only; sdist build hook prints a message. No network, process-launch, or payload behavior in the shipped source. |
| database.ser | 0/2 | source-bytes-and-facts-reviewed | bad | Java object stream containing HashSet/TiedMapEntry/LazyMap/ConstantTransformer/AspectJ caching-map descriptors, JSP command source, and an application webapps target. Added a hostile serialized JSP implant composite. filefacts identifies the stream as JSP because of embedded source; no deserialization executed. |
| @conduitops-logview-archive-1.0.1.tgz | 3/4 | install-chain-reviewed | bad | postinstall invokes install.js, decodes XOR/Base64 registry from lib/toolchain.json, and silently spawns npm install under vendor/. Static decoded registry is http://139.196.94.195:8080/dl/npm/. Existing three hostile findings span install-hook and hidden-payload staging directories. Remote stage has not been fetched or executed. |
| @elfhkry666-baileys-0.3.24.tgz | 6/1 | pending-manual-review | pending |  |
| suggestedtests-0.1.2-py3-none-any.whl | 0/1 | pending-manual-review | pending |  |
| moveworks_capi_starter-0.0.0-py3-none-any.whl | 0/3 | source-and-facts-reviewed | good | Shipped code only returns a dummy-package description. Summary, example author, and dummy-version text do not establish impersonation. These observations now live in metadata; current result is 0H/0S. Pool change is not yet applied. |
| @pisell-pisellos-2.3.176.tgz | 4/1 | pending-manual-review | pending |  |
| @elfhkry666-baileys-0.3.23.tgz | 6/1 | pending-manual-review | pending |  |
| phonemeprobe-0.1.0-py3-none-any.whl | 0/1 | source-and-facts-reviewed | purgatory | Public functions fetch caller-selected URL, stage source in a hidden temporary directory, create a ModuleType, register sys.modules, then exec(compile(source,...)) and invoke run(). No fixed hostile endpoint or automatic import-time payload in the reviewed source. One meaningful suspicious execution signal; do not pad counts. |
| ttsweaver-0.1.0-py3-none-any.whl | 0/1 | source-and-facts-reviewed | purgatory | Public functions fetch caller-selected URL, stage source in a hidden temporary directory, create a ModuleType, register sys.modules, then exec(compile(source,...)) and invoke run(). No fixed hostile endpoint or automatic import-time payload in the reviewed source. One meaningful suspicious execution signal; do not pad counts. |
| soundsocket-0.1.0-py3-none-any.whl | 0/1 | source-and-facts-reviewed | purgatory | Public functions fetch caller-selected URL, stage source in a hidden temporary directory, create a ModuleType, register sys.modules, then exec(compile(source,...)) and invoke run(). No fixed hostile endpoint or automatic import-time payload in the reviewed source. One meaningful suspicious execution signal; do not pad counts. |
| ttsdock-0.1.0-py3-none-any.whl | 0/1 | source-and-facts-reviewed | purgatory | Public functions fetch caller-selected URL, stage source in a hidden temporary directory, create a ModuleType, register sys.modules, then exec(compile(source,...)) and invoke run(). No fixed hostile endpoint or automatic import-time payload in the reviewed source. One meaningful suspicious execution signal; do not pad counts. |
| acousticpack-0.1.0-py3-none-any.whl | 0/1 | source-and-facts-reviewed | purgatory | Public functions fetch caller-selected URL, stage source in a hidden temporary directory, create a ModuleType, register sys.modules, then exec(compile(source,...)) and invoke run(). No fixed hostile endpoint or automatic import-time payload in the reviewed source. One meaningful suspicious execution signal; do not pad counts. |
| modelworks-0.1.0-py3-none-any.whl | 0/1 | source-and-facts-reviewed | purgatory | Public functions fetch caller-selected URL, stage source in a hidden temporary directory, create a ModuleType, register sys.modules, then exec(compile(source,...)) and invoke run(). No fixed hostile endpoint or automatic import-time payload in the reviewed source. One meaningful suspicious execution signal; do not pad counts. |
| ttsprobe-0.1.0-py3-none-any.whl | 0/1 | source-and-facts-reviewed | purgatory | Public functions fetch caller-selected URL, stage source in a hidden temporary directory, create a ModuleType, register sys.modules, then exec(compile(source,...)) and invoke run(). No fixed hostile endpoint or automatic import-time payload in the reviewed source. One meaningful suspicious execution signal; do not pad counts. |
| benchworks-0.1.0-py3-none-any.whl | 0/1 | source-and-facts-reviewed | purgatory | Public functions fetch caller-selected URL, stage source in a hidden temporary directory, create a ModuleType, register sys.modules, then exec(compile(source,...)) and invoke run(). No fixed hostile endpoint or automatic import-time payload in the reviewed source. One meaningful suspicious execution signal; do not pad counts. |
| phonemeforge-0.1.0-py3-none-any.whl | 0/1 | source-and-facts-reviewed | purgatory | Public functions fetch caller-selected URL, stage source in a hidden temporary directory, create a ModuleType, register sys.modules, then exec(compile(source,...)) and invoke run(). No fixed hostile endpoint or automatic import-time payload in the reviewed source. One meaningful suspicious execution signal; do not pad counts. |
| asrloom-0.1.0-py3-none-any.whl | 0/1 | source-and-facts-reviewed | purgatory | Public functions fetch caller-selected URL, stage source in a hidden temporary directory, create a ModuleType, register sys.modules, then exec(compile(source,...)) and invoke run(). No fixed hostile endpoint or automatic import-time payload in the reviewed source. One meaningful suspicious execution signal; do not pad counts. |
| hookgantry-0.1.0-py3-none-any.whl | 0/1 | source-and-facts-reviewed | purgatory | Public functions fetch caller-selected URL, stage source in a hidden temporary directory, create a ModuleType, register sys.modules, then exec(compile(source,...)) and invoke run(). No fixed hostile endpoint or automatic import-time payload in the reviewed source. One meaningful suspicious execution signal; do not pad counts. |
| konnektive-one-1.6.1.tgz | 3/0 | pending-manual-review | pending |  |
| update.ps1 | 0/1 | source-and-facts-reviewed | purgatory | Hardcoded HTTPS ZIP download into TEMP, extract, recursively select first EXE, Start-Process. No payload bytes supplied in this sample; one suspicious download-to-launch chain is confirmed. |
| brookworker-0.1.0-py3-none-any.whl | 2/0 | source-and-facts-reviewed | purgatory | Download helper writes job.py; public run() stages a manifest and launches a Python child with an importlib loader. Review also found module-name references inconsistent with from-import bindings in several variants; presence of the chain does not establish successful execution. Generic hostile composites relocated to suspicious capability rules. |
| badgertask-0.1.0-py3-none-any.whl | 0/0 | source-and-facts-reviewed | purgatory | Download helper writes job.py; public run() stages a manifest and launches a Python child with an importlib loader. Review also found module-name references inconsistent with from-import bindings in several variants; presence of the chain does not establish successful execution. Generic hostile composites relocated to suspicious capability rules. |
| My 2FA KeyX.exe | 0/0 | binary-review-in-progress | pending | Valid CA signature does not resolve behavior. Go function/callee facts show GenerateTwoFAcode performs HTTP fetch/read, Base64 decoding, AES-GCM helper use, file writes, Rundll32 and command-launch helpers. GetCont fetches a Telegram URL and calls Ethereum key-to-address routines. Needs call-path/disassembly review; current scan has no suspicious/hostile finding. |
| brambletask-0.1.0-py3-none-any.whl | 0/0 | source-and-facts-reviewed | purgatory | Download helper writes job.py; public run() stages a manifest and launches a Python child with an importlib loader. Review also found module-name references inconsistent with from-import bindings in several variants; presence of the chain does not establish successful execution. Generic hostile composites relocated to suspicious capability rules. |
| larchworker-0.1.0-py3-none-any.whl | 2/0 | source-and-facts-reviewed | purgatory | Download helper writes job.py; public run() stages a manifest and launches a Python child with an importlib loader. Review also found module-name references inconsistent with from-import bindings in several variants; presence of the chain does not establish successful execution. Generic hostile composites relocated to suspicious capability rules. |
| 0d23bcb2e85eba59d7b40cdaef8ad8290834caf4ac00260f567cf5d037e78932 | 3/1 | pending-manual-review | pending |  |
| chutes-build-win32-x64-2.0.1.tgz | 0/0 | pending-manual-review | pending |  |
| kkodiihpgodmdankclfibbiphjkfdenh.crx | 0/0 | pending-manual-review | pending |  |
| ferretqueue-0.1.0-py3-none-any.whl | 2/0 | source-and-facts-reviewed | purgatory | Download helper writes job.py; public run() stages a manifest and launches a Python child with an importlib loader. Review also found module-name references inconsistent with from-import bindings in several variants; presence of the chain does not establish successful execution. Generic hostile composites relocated to suspicious capability rules. |
| chutes-build-win32-x64-2.0.2.tgz | 0/1 | pending-manual-review | pending |  |
| 1a7f0e2e962a6e6c80b08e77d88dfa50ec8ce2d1f1efd4dd26d3fb14b94d4399 | 4/0 | pending-manual-review | pending |  |
| sedgehaul-0.1.0-py3-none-any.whl | 2/0 | source-and-facts-reviewed | purgatory | Download helper writes job.py; public run() stages a manifest and launches a Python child with an importlib loader. Review also found module-name references inconsistent with from-import bindings in several variants; presence of the chain does not establish successful execution. Generic hostile composites relocated to suspicious capability rules. |
| deathstar.mipsel | 3/1 | pending-manual-review | pending |  |
| deathstar.m68k | 3/1 | pending-manual-review | pending |  |
| flintqueue-0.1.0-py3-none-any.whl | 2/0 | source-and-facts-reviewed | purgatory | Download helper writes job.py; public run() stages a manifest and launches a Python child with an importlib loader. Review also found module-name references inconsistent with from-import bindings in several variants; presence of the chain does not establish successful execution. Generic hostile composites relocated to suspicious capability rules. |
| d872e02c03b4896fd58eea4adfc8dd62342661808595f456f64cf1d3cee43a25 | 3/1 | pending-manual-review | pending |  |
| d959381329171033019f0407a82f5ae23760f4a596940a7635592093792be8c5 | 3/1 | pending-manual-review | pending |  |
| deathstar.powerpc | 3/1 | pending-manual-review | pending |  |
| deathstar.mips | 3/1 | pending-manual-review | pending |  |
| 2026-10-22_10d87b737c2d16241303c64382407644_amadey_darkgate_elex_icedid_smoke-loader_stop | 5/3 | pending-manual-review | pending |  |
| fontus-0.0.2-py3-none-any.whl | 1/0 | source-and-facts-reviewed | purgatory | CLI collects font families, host and OS details, caches JSON, and posts it to an overridable default trycloudflare endpoint. No secret source or import-time exfiltration established. Corrected hostile verdict to suspicious. |
| fontus-0.0.1-py3-none-any.whl | 1/0 | source-and-facts-reviewed | purgatory | CLI collects font families, host and OS details, caches JSON, and posts it to an overridable default trycloudflare endpoint. No secret source or import-time exfiltration established. Corrected hostile verdict to suspicious. |
| hklfajkfkbojpmjjlehhhheklagilfab.crx | 0/1 | pending-manual-review | pending |  |
| scdn-jquery-0.1.6.tgz | 3/1 | pending-manual-review | pending |  |
| @axon-web-icons-1.0.1.tgz | 1/0 | source-and-facts-reviewed | purgatory | Entrypoint prints hostname/user/cwd/platform locally and exports an empty object; actual console banner declares dependency-confusion PoC. Generic host survey moved to capability tier; new code-call banner fact supports a suspicious disclosed-PoC composite without claiming network exfiltration. |
| @ppa-web-components-ppa-searchform-0.1.0.tgz | 0/0 | source-reviewed | good | Archive contains only package.json and README.md; no scripts, dependencies, or executable payload. |
| hhmdehebknkbhlfgnapckcmgkalhmcjp.crx | 0/1 | pending-manual-review | pending |  |
| watchmen-cli-win32-x64-3.0.0.tgz | 0/0 | pending-manual-review | pending |  |
| @bobfrankston-mailx-store-web-0.1.133.tgz | 0/1 | pending-manual-review | pending |  |
| @majapisoftwares-router-0.2.0.tgz | 1/2 | pending-manual-review | pending |  |
| github.com-benr00t3d-go-cgo-pkgsite-probe-v0.0.25.zip | 0/2 | pending-manual-review | pending |  |
| @zervonex-baileys-3.0.8.tgz | 3/0 | pending-manual-review | pending |  |
| ichfadkdnkechpkpebiikjcfkhkljmji.crx | 0/1 | pending-manual-review | pending |  |
| nix-update | 4/0 | pending-manual-review | pending |  |
| coderabbit-0.9.1.tgz | 0/0 | pending-manual-review | pending |  |
| github.com-benr00t3d-go-cgo-pkgsite-probe-v0.0.24.zip | 0/2 | pending-manual-review | pending |  |
| github.com-benr00t3d-go-cgo-pkgsite-probe-v0.0.23.zip | 0/2 | pending-manual-review | pending |  |
| micbejknmlmdembjamkhplmdnfccfihk.crx | 0/0 | pending-manual-review | pending |  |
| nibcomahncdgfpomleflglbefefieape.crx | 0/2 | pending-manual-review | pending |  |
| ogljdkanllnomgimpifhdcolfnninpia.crx | 0/1 | pending-manual-review | pending |  |
| pdedgfkkkpopgnbfjeoifakhacbbcekj.crx | 0/1 | pending-manual-review | pending |  |
| ok_script-2.0.11-py3-none-any.whl | 0/0 | pending-manual-review | pending |  |
| 0c76358cf582c52e.js | 2/0 | payload-decoded-static | bad | Statically decoded Base64 then XOR-28. Hidden stage appends a full-viewport Security check iframe, max-z-index overlay and remote /embed/ fallback hosts, forwarding the visited hostname. Domains include cloudflare-check.net and 94.26.90.126. Existing original-file coverage has two hostile encoded-execution findings; decoded overlay coverage still needs assessment. |
| 6baed65e86355ac0.js | 2/0 | payload-decoded-static | bad | Statically decoded Base64 then XOR-28. Hidden stage appends a full-viewport Security check iframe, max-z-index overlay and remote /embed/ fallback hosts, forwarding the visited hostname. Domains include cloudflare-check.net and 94.26.90.126. Existing original-file coverage has two hostile encoded-execution findings; decoded overlay coverage still needs assessment. |
| install_panel.sh | 0/4 | pending-manual-review | pending |  |
| ok_script-2.0.12-py3-none-any.whl | 0/0 | pending-manual-review | pending |  |
| syncrify-publiclink.py | 0/2 | pending-manual-review | pending |  |
| zapret-discord-youtube-1.10.2.rar | 0/2 | pending-manual-review | pending |  |
| cmdly-0.2.1.tgz | 0/0 | pending-manual-review | pending |  |
| rewards.apk | 0/2 | pending-manual-review | pending |  |
| git-span-win32-x64-1.1.47.tgz | 0/0 | pending-manual-review | pending |  |
| trustlint-2.2.0.tgz | 0/0 | pending-manual-review | pending |  |
| ok_script-2.0.15b2-py3-none-any.whl | 0/0 | pending-manual-review | pending |  |
| ok_script-2.0.15b3-py3-none-any.whl | 0/0 | pending-manual-review | pending |  |
| ok_script-2.0.15-py3-none-any.whl | 0/0 | pending-manual-review | pending |  |
| github.com-benr00t3d-go-cgo-pkgsite-probe-v0.0.29.zip | 0/2 | pending-manual-review | pending |  |
| github.com-benr00t3d-go-cgo-pkgsite-probe-v0.0.31.zip | 0/2 | pending-manual-review | pending |  |
| aapbdbdomjkkjkaonfhkkikfgjllcleb.crx | 0/0 | pending-manual-review | pending |  |
| zzhelloworld_socktest-0.1.3.gem | 0/0 | pending-manual-review | pending |  |
| zzhelloworld_socktest-0.1.2.gem | 0/0 | pending-manual-review | pending |  |
| _ HW Trial Transcripts, Court Proceedings, Sentencing Reports, Forfeiture Hearings and Other Files  - ECF Files-20261022T084700Z-1-001.zip | 0/0 | pending-manual-review | pending |  |
| @stefanosala-vc-cli-linux-x64-0.1.0.tgz | 0/0 | source-reviewed | good | Manifest-only archive; declared vc-cli binary is absent. No executable payload or lifecycle hook. |
| goeaopneeaonhlmjefodnafebimicoal.crx | 0/1 | pending-manual-review | pending |  |
| claudecord-0.4.2-py3-none-macosx_10_12_x86_64.whl | 0/0 | pending-manual-review | pending |  |
| hjbpbhkcjlfnbgdliojnclpooogodifa.crx | 0/1 | pending-manual-review | pending |  |
| virussign.com_0ba27def95a1c705e6f9dedd9e28c100.vir | 0/0 | pending-manual-review | pending |  |
| kcdocgobebmfpffcpodenggpgkpdddfc.crx | 0/1 | pending-manual-review | pending |  |
| @gowri48-npmpublish-2.1.7.tgz | 0/0 | pending-manual-review | pending |  |
| f5cfe0cf4f22c4ca.js | 1/0 | pending-manual-review | pending |  |
| cmcjiebfifgdlmfdkjjnmihchgmpeccl.crx | 0/1 | pending-manual-review | pending |  |
| foremerge-win32-x64-0.6.0.tgz | 0/0 | pending-manual-review | pending |  |
| virussign.com_84a15af3dd065f5ce6683c78a6287f00.vir | 0/0 | pending-manual-review | pending |  |
| pjpmebofipgpjaincgoboibbmicccbne.crx | 0/0 | pending-manual-review | pending |  |
| 2156893662-docs_offline_iframe_api_bin.js | 0/0 | pending-manual-review | pending |  |
| virussign.com_0f3a0b504c4a1ff46e1b2fe8b31ad0c0.vir | 0/0 | pending-manual-review | pending |  |
| virussign.com_0d2ac483ce3e2190c146c9ad18913750.vir | 0/0 | pending-manual-review | pending |  |
| cd578333a4be96988080597063b8e35a46452b578f5f70abf2f81374924bc45e | 1/3 | source-reviewed | purgatory | Suppresses stdout/stderr, obtains native Python argc via ctypes, and with argc==1 runs a .so-named sidecar through runpy.run_path. Sidecar is absent; do not infer its behavior. |
| anubis-0.9.9.1mc1.21.11.jar | 0/0 | pending-manual-review | pending |  |
| a13e3e4525e28ff8.js | 2/1 | pending-manual-review | pending |  |
| myui.1.2.4.nupkg | 2/0 | pending-manual-review | pending |  |
| AutoHarp-fabric26.1.jar | 2/2 | pending-manual-review | pending |  |
| mega-code-dev-0.5.2.tgz | 0/0 | pending-manual-review | pending |  |
| @lightdash-cli-2.618.0.tgz | 0/0 | pending-manual-review | pending |  |
| suppa-mcp-2-1.43.0.tgz | 1/1 | pending-manual-review | pending |  |
| 3a580c3d7bc86e63.js | 1/0 | pending-manual-review | pending |  |
| mdlkdelnchilkeedllnnjfigkhhadlff.crx | 0/0 | pending-manual-review | pending |  |
| @chatunity-baileys-1.2.2.tgz | 0/2 | pending-manual-review | pending |  |
| animatecss-tailwind-presets-1.0.0.tgz | 3/5 | pending-manual-review | pending |  |
| animatecss-tailwind-luminary-2.0.6.tgz | 3/5 | pending-manual-review | pending |  |
| wafaction1.msi | 0/0 | pending-manual-review | pending |  |
| hochhggfcmeejhlnflabcpligajohjne.crx | 0/2 | pending-manual-review | pending |  |
| bfpmblbobcdklnmfabbolldpjbpkhekn.crx | 0/2 | pending-manual-review | pending |  |
| ok_script-2.0.10-py3-none-any.whl | 0/0 | pending-manual-review | pending |  |
| tadashi.arm64 | 2/2 | pending-manual-review | pending |  |
| tadashi.arm4 | 3/2 | pending-manual-review | pending |  |
| tadashi.arm6 | 3/2 | pending-manual-review | pending |  |
| bot_riscv64 | 1/4 | pending-manual-review | pending |  |
| claudecord-0.4.0-py3-none-macosx_10_12_x86_64.whl | 0/0 | pending-manual-review | pending |  |
| claudecord-0.4.1-py3-none-macosx_10_12_x86_64.whl | 0/0 | pending-manual-review | pending |  |
| potassium-1.21.4.jar | 3/1 | pending-manual-review | pending |  |
| mjmpnjpfkipaimjhlnhpfbeoneldoikk.crx | 0/1 | pending-manual-review | pending |  |
| mfnmnnnjideiagjciobfhnhejohinfok.crx | 0/1 | pending-manual-review | pending |  |
| hfacplbfjfkdkggcnojgmokaiighpecb.crx | 0/1 | pending-manual-review | pending |  |
| gieoofpplpbfeobmbdloommpkfaoppoj.crx | 0/1 | pending-manual-review | pending |  |
| enokbmlgjjknfhhbhiiclafheenpdlhj.crx | 0/1 | pending-manual-review | pending |  |
| geajflohnkhfpckifecaehhibnembamc.crx | 0/1 | pending-manual-review | pending |  |
| jgmcmdfkmcpgakbabkhgkpponillmphl.crx | 0/1 | pending-manual-review | pending |  |
| cgbiphmkbnlgpddfcjjfnmneiipmeomg.crx | 0/1 | pending-manual-review | pending |  |
| phoiedjgigaabadlfkbmpjajhnnigpjd.crx | 0/0 | pending-manual-review | pending |  |
| pbgbkaiaeaoehbphelhidlkjjfefcfdf.crx | 1/3 | pending-manual-review | pending |  |
| ipigeepajccobadajloohomohdmfigkn.crx | 0/1 | pending-manual-review | pending |  |
| claudecord-0.3.3-py3-none-macosx_10_12_x86_64.whl | 0/0 | pending-manual-review | pending |  |

## Latest verification

The x-improve follow-up is recorded in [improvements.md](improvements.md). Six original samples were rescanned; five original/negative-control cases checked both JavaScript wrapper rules. Final full validation passed: hostile 2797/2797, suspicious 1757/1757, notable 8441/8441, baseline 1316/1316. No exceptions or threshold overrides were added. No Hopper labels were moved in the x-improve pass.

The ledger retains 36 samples with manual evidence notes and 104 awaiting deeper manual review. Partial reviews are distinguished from finalized pool changes.
