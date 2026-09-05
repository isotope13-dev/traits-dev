Triage these vetted-benign false positive(s):
- /data/gauntlet-fp/80785047aa93a4e6cdbfb7708b8eb85e4b4bb5bfd1036e1a176b60614ac79bb3/classinx_win_install_6.0.8.2843_x64.exe — hostile: 0, suspicious: 2
  - S objectives/anti-static/obfuscation/binary-metrics/shape::high-entropy-overlay — Large high-entropy overlay
    members: /data/gauntlet-fp/80785047aa93a4e6cdbfb7708b8eb85e4b4bb5bfd1036e1a176b60614ac79bb3/classinx_win_install_6.0.8.2843_x64.exe!!$_1_/app.dat, /data/gauntlet-fp/80785047aa93a4e6cdbfb7708b8eb85e4b4bb5bfd1036e1a176b60614ac79bb3/classinx_win_install_6.0.8.2843_x64.exe!!$_1_/app.dat!!eeoPlayerProxy.exe
  - S objectives/credential-access/dump/system::kerberos-aeskey-option — AES key option for Kerberos auth
    members: /data/gauntlet-fp/80785047aa93a4e6cdbfb7708b8eb85e4b4bb5bfd1036e1a176b60614ac79bb3/classinx_win_install_6.0.8.2843_x64.exe!!$_1_/app.dat, /data/gauntlet-fp/80785047aa93a4e6cdbfb7708b8eb85e4b4bb5bfd1036e1a176b60614ac79bb3/classinx_win_install_6.0.8.2843_x64.exe!!$_1_/app.dat!!libcef.dll


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
