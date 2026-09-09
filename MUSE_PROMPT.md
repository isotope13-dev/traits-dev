Triage these vetted-benign false positive(s):
- /data/gauntlet-fp/86eb2fd13be74347e8e33fa166e7984c44ea57ee274d968b77fd0b933e32cfc9/wine-dwproton-11.0-12-x86_64.tar.xz — hostile: 0, suspicious: 7
  - S objectives/command-and-control/infrastructure/ip-port::hardcoded-c2-ip-port — Hardcoded external IP:port likely used as C2
    members: /data/gauntlet-fp/86eb2fd13be74347e8e33fa166e7984c44ea57ee274d968b77fd0b933e32cfc9/wine-dwproton-11.0-12-x86_64.tar.xz!!wine-dwproton/usr/lib/wine/i386-windows/wineps.drv, /data/gauntlet-fp/86eb2fd13be74347e8e33fa166e7984c44ea57ee274d968b77fd0b933e32cfc9/wine-dwproton-11.0-12-x86_64.tar.xz!!wine-dwproton/usr/lib/wine/i386-windows/wusa.exe, /data/gauntlet-fp/86eb2fd13be74347e8e33fa166e7984c44ea57ee274d968b77fd0b933e32cfc9/wine-dwproton-11.0-12-x86_64.tar.xz!!wine-dwproton/usr/lib/wine/x86_64-windows/wusa.exe
  - S objectives/credential-access/dump/process::lsass-memory-target — LSASS memory access target
    members: /data/gauntlet-fp/86eb2fd13be74347e8e33fa166e7984c44ea57ee274d968b77fd0b933e32cfc9/wine-dwproton-11.0-12-x86_64.tar.xz!!wine-dwproton/usr/lib/wine/x86_64-windows/wineboot.exe
  - S objectives/evasion/indicator-removal/logs::fsctl-delete-usn-journal — Deletes NTFS change journal
    members: /data/gauntlet-fp/86eb2fd13be74347e8e33fa166e7984c44ea57ee274d968b77fd0b933e32cfc9/wine-dwproton-11.0-12-x86_64.tar.xz!!wine-dwproton/usr/include/wine/windows/winioctl.h
  - S objectives/evasion/masquerade/brand/product::unity-masquerade-hollow-gui — Unity masquerade as GUI binary with missing UI/graphics imports
    members: /data/gauntlet-fp/86eb2fd13be74347e8e33fa166e7984c44ea57ee274d968b77fd0b933e32cfc9/wine-dwproton-11.0-12-x86_64.tar.xz!!wine-dwproton/usr/lib/wine/i386-windows/atiadlxx.dll, /data/gauntlet-fp/86eb2fd13be74347e8e33fa166e7984c44ea57ee274d968b77fd0b933e32cfc9/wine-dwproton-11.0-12-x86_64.tar.xz!!wine-dwproton/usr/lib/wine/x86_64-windows/atiadlxx.dll
  - S objectives/evasion/masquerade/version-resource/python-dll::spoofed-metadata-conflict — Trusted vendor metadata but high-entropy code/data (potential spoofing)
    members: /data/gauntlet-fp/86eb2fd13be74347e8e33fa166e7984c44ea57ee274d968b77fd0b933e32cfc9/wine-dwproton-11.0-12-x86_64.tar.xz!!wine-dwproton/usr/lib/wine/i386-windows/actxprxy.dll, /data/gauntlet-fp/86eb2fd13be74347e8e33fa166e7984c44ea57ee274d968b77fd0b933e32cfc9/wine-dwproton-11.0-12-x86_64.tar.xz!!wine-dwproton/usr/lib/wine/i386-windows/colorcnv.dll, /data/gauntlet-fp/86eb2fd13be74347e8e33fa166e7984c44ea57ee274d968b77fd0b933e32cfc9/wine-dwproton-11.0-12-x86_64.tar.xz!!wine-dwproton/usr/lib/wine/i386-windows/dispex.dll, /data/gauntlet-fp/86eb2fd13be74347e8e33fa166e7984c44ea57ee274d968b77fd0b933e32cfc9/wine-dwproton-11.0-12-x86_64.tar.xz!!wine-dwproton/usr/lib/wine/i386-windows/ieproxy.dll, /data/gauntlet-fp/86eb2fd13be74347e8e33fa166e7984c44ea57ee274d968b77fd0b933e32cfc9/wine-dwproton-11.0-12-x86_64.tar.xz!!wine-dwproton/usr/lib/wine/i386-windows/l3codecx.ax, /data/gauntlet-fp/86eb2fd13be74347e8e33fa166e7984c44ea57ee274d968b77fd0b933e32cfc9/wine-dwproton-11.0-12-x86_64.tar.xz!!wine-dwproton/usr/lib/wine/i386-windows/mfh264enc.dll, … +41
  - S objectives/execution/exploit/parser-confusion::empty-semicolon-path-parameter — Empty semicolon path parameter
    members: /data/gauntlet-fp/86eb2fd13be74347e8e33fa166e7984c44ea57ee274d968b77fd0b933e32cfc9/wine-dwproton-11.0-12-x86_64.tar.xz!!wine-dwproton/usr/include/wine/windows/winnt.h, /data/gauntlet-fp/86eb2fd13be74347e8e33fa166e7984c44ea57ee274d968b77fd0b933e32cfc9/wine-dwproton-11.0-12-x86_64.tar.xz!!wine-dwproton/usr/lib/wine/i386-windows/browseui.dll, /data/gauntlet-fp/86eb2fd13be74347e8e33fa166e7984c44ea57ee274d968b77fd0b933e32cfc9/wine-dwproton-11.0-12-x86_64.tar.xz!!wine-dwproton/usr/lib/wine/i386-windows/d3d10.dll, /data/gauntlet-fp/86eb2fd13be74347e8e33fa166e7984c44ea57ee274d968b77fd0b933e32cfc9/wine-dwproton-11.0-12-x86_64.tar.xz!!wine-dwproton/usr/lib/wine/i386-windows/d3dx9_24.dll, /data/gauntlet-fp/86eb2fd13be74347e8e33fa166e7984c44ea57ee274d968b77fd0b933e32cfc9/wine-dwproton-11.0-12-x86_64.tar.xz!!wine-dwproton/usr/lib/wine/i386-windows/d3dx9_25.dll, /data/gauntlet-fp/86eb2fd13be74347e8e33fa166e7984c44ea57ee274d968b77fd0b933e32cfc9/wine-dwproton-11.0-12-x86_64.tar.xz!!wine-dwproton/usr/lib/wine/i386-windows/d3dx9_26.dll, … +28
  - S objectives/lateral-movement/smb::remote-drop-or-enum — Remote share drop or enumeration
    members: /data/gauntlet-fp/86eb2fd13be74347e8e33fa166e7984c44ea57ee274d968b77fd0b933e32cfc9/wine-dwproton-11.0-12-x86_64.tar.xz!!wine-dwproton/usr/include/wine/windows/lmaccess.h

- /data/gauntlet-fp/770d12b0493622a3b822c50f3ba6388a2b60df4bd00183f374677a003767ec99/OpenShell-v0.0.114-0.20260825170443-38a94931ffa5.zip — hostile: 0, suspicious: 6
  - S micro-behaviors/fs/chmod/executable/dangerous::chmod-777 — World-writable+executable permissions (777)
    members: /data/gauntlet-fp/770d12b0493622a3b822c50f3ba6388a2b60df4bd00183f374677a003767ec99/OpenShell-v0.0.114-0.20260825170443-38a94931ffa5.zip!!OpenShell-38a94931ffa52f85b493094bcd46ab988016293b/examples/spiffe-token-exchange-demo/podman/spire/start-agent.sh, /data/gauntlet-fp/770d12b0493622a3b822c50f3ba6388a2b60df4bd00183f374677a003767ec99/OpenShell-v0.0.114-0.20260825170443-38a94931ffa5.zip!!OpenShell-38a94931ffa52f85b493094bcd46ab988016293b/examples/spiffe-token-exchange-demo/podman/spire/start-server-oidc.sh, /data/gauntlet-fp/770d12b0493622a3b822c50f3ba6388a2b60df4bd00183f374677a003767ec99/OpenShell-v0.0.114-0.20260825170443-38a94931ffa5.zip!!OpenShell-38a94931ffa52f85b493094bcd46ab988016293b/examples/spiffe-token-exchange-demo/podman/start-gateway.sh
  - S objectives/anti-analysis/sandbox-detect/suite::evasion-checks — Evasion checks detected (usernames/hostnames/paths)
    members: /data/gauntlet-fp/770d12b0493622a3b822c50f3ba6388a2b60df4bd00183f374677a003767ec99/OpenShell-v0.0.114-0.20260825170443-38a94931ffa5.zip!!OpenShell-38a94931ffa52f85b493094bcd46ab988016293b/crates/openshell-driver-vm/scripts/openshell-vm-sandbox-init.sh
  - S objectives/command-and-control/dropper/execution/payload::hidden-dir-execution — Execute from hidden directory
    members: /data/gauntlet-fp/770d12b0493622a3b822c50f3ba6388a2b60df4bd00183f374677a003767ec99/OpenShell-v0.0.114-0.20260825170443-38a94931ffa5.zip!!OpenShell-38a94931ffa52f85b493094bcd46ab988016293b/e2e/mcp-conformance/client-through-openshell.sh, /data/gauntlet-fp/770d12b0493622a3b822c50f3ba6388a2b60df4bd00183f374677a003767ec99/OpenShell-v0.0.114-0.20260825170443-38a94931ffa5.zip!!OpenShell-38a94931ffa52f85b493094bcd46ab988016293b/e2e/python/test_sandbox_venv.py
  - S objectives/evasion/kernel-hide/ebpf::bpf-map-create-syscall — BPF map creation syscall
    members: /data/gauntlet-fp/770d12b0493622a3b822c50f3ba6388a2b60df4bd00183f374677a003767ec99/OpenShell-v0.0.114-0.20260825170443-38a94931ffa5.zip!!OpenShell-38a94931ffa52f85b493094bcd46ab988016293b/crates/openshell-supervisor-process/src/sandbox/linux/seccomp.rs
  - S objectives/evasion/kernel-hide/keywords::hidden-object-identifiers — Hidden-object identifiers (hide_pid/name/port) common in kernel rootkits
    members: /data/gauntlet-fp/770d12b0493622a3b822c50f3ba6388a2b60df4bd00183f374677a003767ec99/OpenShell-v0.0.114-0.20260825170443-38a94931ffa5.zip!!OpenShell-38a94931ffa52f85b493094bcd46ab988016293b/crates/openshell-driver-vm/src/driver.rs
  - S objectives/execution/exploit/parser-confusion::empty-semicolon-path-parameter — Empty semicolon path parameter
    members: /data/gauntlet-fp/770d12b0493622a3b822c50f3ba6388a2b60df4bd00183f374677a003767ec99/OpenShell-v0.0.114-0.20260825170443-38a94931ffa5.zip!!OpenShell-38a94931ffa52f85b493094bcd46ab988016293b/crates/openshell-supervisor-network/src/l7/path.rs

- /data/gauntlet-fp/8224525de78d20906885d22eb5d28d518f45a15ba78722f657eddfa378c9e278/MiniMax Code Setup 3.0.58.exe — hostile: 0, suspicious: 4
  - S objectives/command-and-control/remote-command/control::websocket-message-function-exec--new-function-event-data — new Function built from message event data
    members: /data/gauntlet-fp/8224525de78d20906885d22eb5d28d518f45a15ba78722f657eddfa378c9e278/MiniMax Code Setup 3.0.58.exe!!$PLUGINSDIR/app-64.7z, /data/gauntlet-fp/8224525de78d20906885d22eb5d28d518f45a15ba78722f657eddfa378c9e278/MiniMax Code Setup 3.0.58.exe!!$PLUGINSDIR/app-64.7z!!resources/app.asar, /data/gauntlet-fp/8224525de78d20906885d22eb5d28d518f45a15ba78722f657eddfa378c9e278/MiniMax Code Setup 3.0.58.exe!!$PLUGINSDIR/app-64.7z!!resources/app.asar!!out/_next/static/chunks/7115-683b86e53060f113.js, /data/gauntlet-fp/8224525de78d20906885d22eb5d28d518f45a15ba78722f657eddfa378c9e278/MiniMax Code Setup 3.0.58.exe!!$PLUGINSDIR/app-arm64.7z, /data/gauntlet-fp/8224525de78d20906885d22eb5d28d518f45a15ba78722f657eddfa378c9e278/MiniMax Code Setup 3.0.58.exe!!$PLUGINSDIR/app-arm64.7z!!resources/app.asar, /data/gauntlet-fp/8224525de78d20906885d22eb5d28d518f45a15ba78722f657eddfa378c9e278/MiniMax Code Setup 3.0.58.exe!!$PLUGINSDIR/app-arm64.7z!!resources/app.asar!!out/_next/static/chunks/7115-683b86e53060f113.js
  - S objectives/evasion/file-hiding/dotfile-create::hidden-staging-file — Hidden file in staging directory
    members: /data/gauntlet-fp/8224525de78d20906885d22eb5d28d518f45a15ba78722f657eddfa378c9e278/MiniMax Code Setup 3.0.58.exe!!$PLUGINSDIR/app-64.7z, /data/gauntlet-fp/8224525de78d20906885d22eb5d28d518f45a15ba78722f657eddfa378c9e278/MiniMax Code Setup 3.0.58.exe!!$PLUGINSDIR/app-64.7z!!resources/app.asar, /data/gauntlet-fp/8224525de78d20906885d22eb5d28d518f45a15ba78722f657eddfa378c9e278/MiniMax Code Setup 3.0.58.exe!!$PLUGINSDIR/app-64.7z!!resources/app.asar!!node_modules/@mavis/local-runtime/assets/skills/pdf/scripts/make.sh, /data/gauntlet-fp/8224525de78d20906885d22eb5d28d518f45a15ba78722f657eddfa378c9e278/MiniMax Code Setup 3.0.58.exe!!$PLUGINSDIR/app-arm64.7z, /data/gauntlet-fp/8224525de78d20906885d22eb5d28d518f45a15ba78722f657eddfa378c9e278/MiniMax Code Setup 3.0.58.exe!!$PLUGINSDIR/app-arm64.7z!!resources/app.asar, /data/gauntlet-fp/8224525de78d20906885d22eb5d28d518f45a15ba78722f657eddfa378c9e278/MiniMax Code Setup 3.0.58.exe!!$PLUGINSDIR/app-arm64.7z!!resources/app.asar!!node_modules/@mavis/local-runtime/assets/skills/pdf/scripts/make.sh
  - S objectives/evasion/indicator-removal/cleanup::windows-indicator-removal — Windows indicator and defense removal
    members: /data/gauntlet-fp/8224525de78d20906885d22eb5d28d518f45a15ba78722f657eddfa378c9e278/MiniMax Code Setup 3.0.58.exe!!$PLUGINSDIR/app-64.7z, /data/gauntlet-fp/8224525de78d20906885d22eb5d28d518f45a15ba78722f657eddfa378c9e278/MiniMax Code Setup 3.0.58.exe!!$PLUGINSDIR/app-64.7z!!resources/app.asar, /data/gauntlet-fp/8224525de78d20906885d22eb5d28d518f45a15ba78722f657eddfa378c9e278/MiniMax Code Setup 3.0.58.exe!!$PLUGINSDIR/app-64.7z!!resources/app.asar!!node_modules/@mavis/local-runtime/assets/skills/docx/scripts/env_check.ps1, /data/gauntlet-fp/8224525de78d20906885d22eb5d28d518f45a15ba78722f657eddfa378c9e278/MiniMax Code Setup 3.0.58.exe!!$PLUGINSDIR/app-64.7z!!resources/app.asar!!node_modules/@mavis/local-runtime/assets/skills/docx/scripts/setup.ps1, /data/gauntlet-fp/8224525de78d20906885d22eb5d28d518f45a15ba78722f657eddfa378c9e278/MiniMax Code Setup 3.0.58.exe!!$PLUGINSDIR/app-arm64.7z, /data/gauntlet-fp/8224525de78d20906885d22eb5d28d518f45a15ba78722f657eddfa378c9e278/MiniMax Code Setup 3.0.58.exe!!$PLUGINSDIR/app-arm64.7z!!resources/app.asar, … +2
  - S objectives/evasion/security-bypass/llm/override::llm-safety-bypass — LLM safety bypass prompt
    members: /data/gauntlet-fp/8224525de78d20906885d22eb5d28d518f45a15ba78722f657eddfa378c9e278/MiniMax Code Setup 3.0.58.exe!!$PLUGINSDIR/app-64.7z, /data/gauntlet-fp/8224525de78d20906885d22eb5d28d518f45a15ba78722f657eddfa378c9e278/MiniMax Code Setup 3.0.58.exe!!$PLUGINSDIR/app-64.7z!!resources/app.asar, /data/gauntlet-fp/8224525de78d20906885d22eb5d28d518f45a15ba78722f657eddfa378c9e278/MiniMax Code Setup 3.0.58.exe!!$PLUGINSDIR/app-64.7z!!resources/app.asar!!node_modules/@google/genai/dist/index.cjs, /data/gauntlet-fp/8224525de78d20906885d22eb5d28d518f45a15ba78722f657eddfa378c9e278/MiniMax Code Setup 3.0.58.exe!!$PLUGINSDIR/app-64.7z!!resources/app.asar!!node_modules/@google/genai/dist/index.mjs, /data/gauntlet-fp/8224525de78d20906885d22eb5d28d518f45a15ba78722f657eddfa378c9e278/MiniMax Code Setup 3.0.58.exe!!$PLUGINSDIR/app-64.7z!!resources/app.asar!!node_modules/@google/genai/dist/node/index.cjs, /data/gauntlet-fp/8224525de78d20906885d22eb5d28d518f45a15ba78722f657eddfa378c9e278/MiniMax Code Setup 3.0.58.exe!!$PLUGINSDIR/app-64.7z!!resources/app.asar!!node_modules/@google/genai/dist/node/index.mjs, … +16

- /data/gauntlet-fp/7e6d7bc77517883fef116b0ef49880b810373ee46cb54bbb026a9811ea2abdd2/unsloth-2026.8.19-py3-none-any.whl — hostile: 0, suspicious: 4
  - S micro-behaviors/communications/http/llm::go-template-system-then-llama2-system — Go template appends Llama-2 system after .System
    members: /data/gauntlet-fp/7e6d7bc77517883fef116b0ef49880b810373ee46cb54bbb026a9811ea2abdd2/unsloth-2026.8.19-py3-none-any.whl!!unsloth/ollama_template_mappers.py
  - S objectives/command-and-control/dropper/execution/payload::hidden-dir-execution — Execute from hidden directory
    members: /data/gauntlet-fp/7e6d7bc77517883fef116b0ef49880b810373ee46cb54bbb026a9811ea2abdd2/unsloth-2026.8.19-py3-none-any.whl!!studio/backend/tests/test_llama_cpp_start_failure_classification.py
  - S objectives/credential-access/files/hdf5-external::sensitive-worker-file-target — Sensitive runtime file target
    members: /data/gauntlet-fp/7e6d7bc77517883fef116b0ef49880b810373ee46cb54bbb026a9811ea2abdd2/unsloth-2026.8.19-py3-none-any.whl!!studio/backend/tests/test_permission_mode.py
  - S objectives/persistence/system/cron/job::cron — Cron job persistence indicator
    members: /data/gauntlet-fp/7e6d7bc77517883fef116b0ef49880b810373ee46cb54bbb026a9811ea2abdd2/unsloth-2026.8.19-py3-none-any.whl!!studio/backend/tests/test_trc_approval_cache.py


Success: 0 hostile findings and normally 0 suspicious findings. At most 1 suspicious finding is
acceptable, and only when it accurately describes genuinely unusual behavior in the benign sample.
Every remaining finding must accurately describe observed behavior, regardless of its criticality.

Use the findings above as the initial worklist. Repair traits containing any misleading or
inaccurate findings, regardless of criticality, following the relevant parts of TAXONOMY.md and
RULES.md.
Use `cleave facts` and `cleave test-rules` on representative extracted files; facts are faster
and more reliable than text searches. Extract archives once and group equivalent `src`/`dist`,
`.js`/`.ts`, architecture, and bundled-library variants.

Make the smallest defensible change and preserve useful detection. Base exceptions on strong,
generalizable evidence. Give traits specific IDs and descriptions that tell an analyst what
behavior was observed and why it matters.

Make all planned changes before measuring each sample:

  /data/rectifier/bin/cleave analyze <sample>

Run this at least once after editing and before finishing. Inspect findings at every criticality,
not only those that affect the QA count gate. If the success counts are not met or any finding is
misleading or inaccurate, make the next complete set of changes before analyzing again.

Before finishing, you MUST run:

  make -C /data/rectifier/traits-dev validate CLEAVE=/data/rectifier/bin/cleave

Fix every error and rerun until it passes. Rectifier performs the authoritative rescan.
