First reasoned native-sample review
==================================

All three verdicts are MALICIOUS. No specimen was executed on the host and no
controller was contacted. `atomscan` and `cleave facts` were run for each input;
Rizin disassembly, Capstone instruction decoding and PE structural reads supplied
the evidence below. Sandbox and antivirus votes were not used as proof.

* `bd2960e1837253ec32866e3cf6697c936d847d5b24cd17d41701e045c5cb29e9`:
  MindBreak C Egg, an unstripped, static, big-endian MIPS bot and credential
  stealer. `main` at `0x4005d0` starts scanning/control threads and calls
  `loot_harvest` at `0x407a1c`. The latter passes SSH private keys, `/etc/shadow`,
  shell histories, application `.env`, AWS credentials, Docker and Kubernetes
  configurations to `read_and_send` (`0x4078ec`). That function opens and reads
  each file and calls `send_loot` (`0x4062f0`), which escapes its contents into a
  type/IP/data JSON report and sends it through the controller socket as
  `POST /loot`. `redis_exploit` (`0x4064c8`) sends CONFIG/SET/SAVE sequences that
  dump an attacker key into root's authorized_keys or a download-and-run cron
  entry into root's cron spool. `docker_exploit` (`0x4031a4`) creates/starts a
  privileged container with a host-root bind and a chroot payload command.
  These three persistence/escape convictions remain. The SSH-key conviction now
  requires a SET value containing public-key material and a SAVE command, in
  addition to the targeted dump directory and filename. The added loot finding is
  suspicious because its matcher establishes co-occurrence, not data flow.

* `a2078c2fa8ff0e81cf68a35d3c7e60e425cf46c835a31b9e8ea677e2bddbff5c`:
  StormAttack DDoS server DLL, truncated to 19,360 bytes. Its declared entry
  point/import directory are missing; standalone execution is not established.
  Retained code at `0x1000228e` builds WSASocket arguments for raw IPv4 UDP,
  enables IP_HDRINCL, then repeatedly sends twelve-packet bursts at
  `0x10002353` until a global stop flag changes. Packet preparation at
  `0x10002626` builds IP/UDP headers and checksums. Other retained routines
  implement UDP/TCP/HTTP flood modes. The control receive loop is visible at
  `0x10004d9f`; host reporting formats `STORM:%d|%s|%s|%s|%s` at `0x10001e52`.
  Reuse the existing StormAttack identity with a smaller minimum-size gate and
  detect the raw-packet burst behavior separately. The generic User-Agent is
  not CN-campaign evidence, so its third-party conviction is disabled globally.

* `be1324b33b6d1c5928f005361a97a06401b66635c01e30e32fd661dab46f884f`:
  Rifaien self-submission executable with an appended native modular backdoor
  at file offset `0x3b000`. The already-unpacked outer image enters at
  `0x401130`; `main` at `0x4013a0` reads its entire file, changes sixteen bytes
  after `[[UNIQUE]]`, writes a clone, submits it as a multipart file with a
  randomly chosen NODE field, deletes the clone, and repeats after 30 seconds.
  No outer-to-overlay execution was found. This behavior alone is not hostile.
  The complete appended PE is independently malicious: `main` at `0x4049e0`
  installs service/Run-key persistence and starts an outbound command client.
  `0x403350` complements the low byte of each two-byte word; this recovers five
  DDNS controller alternatives and DLL/EXE upload/load/upgrade status messages.
  The receive routine at `0x403d80` returns records to `0x4027e0`; byte six
  selects `0x88` (write supplied DLL bytes, load it and invoke its
  Load/Run/Stop/Unload exports) or `0x89` (write and execute a replacement EXE).
  `0x4043f0` creates an auto-start service with the `/srv` invocation. New
  command-dispatch and persistence traits match the embedded PE in isolation,
  requiring protocol code, decoder/status evidence and actual API imports.
  No family attribution from the collector's filename is retained.

Removed or relocated observations
---------------------------------

* Self-exe path + shell path + direct MIPS syscall did not establish a backdoor.
* Generic GET requests did not establish architecture-specific Mirai loading.
* Redis snapshot configuration did not establish exploitation or even a write.
* History/key paths, exploit-prefixed string-table names, and an insecure SSH
  command retain neutral, correctly scoped observations.
* P2P + authorized_keys + a brute-force word did not establish SSH attacks.
* BusyBox transfer near chmod/execution retains a neutral co-occurrence finding.
* UPX labels, mutation/upload vocabulary and a large PE overlay did not establish
  concealment or activation. Generic embedded service-client vocabulary did not
  establish a backdoor. Their unsupported hostile composites were removed;
  narrower behavior traits now detect the independently reversed payload.

Checks and limits
----------------

`check.py` generates inert controls and dependency mutations under the supplied
scratch directory. It checks original and altered command/flood instructions,
the uploader without its backdoor, a generic browser User-Agent, a generic
service-client string table, ordinary Redis administration, SSH dump configuration without key material,
a neutral MIPS HTTP/procfs binary, and the loot helper pair. Altered malware controls are not labeled benign.

The installed Atomscan embeds an older Cleave: it still emits the engine-owned
hostile `anti-static/packer/upx/decompression-failed` for the already-unpacked
outer PE. YAML cannot override this finding. Current standalone Cleave and the
named Cleave source already classify tool refusal as notable under
`metadata/binary/layout/compression::upx-decompression-failed`. The two new
hostile findings on the embedded backdoor independently support the verdict.
The remaining Atomscan engine finding is an acknowledged false positive, not
part of the conviction and not claimed to be repaired by these YAML changes.
