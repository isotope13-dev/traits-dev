# First reasoned review: SDL / managed-game APIs and two native loaders

Static review of the three supplied SHA256s. No sample was executed. Initial
`atomscan --no-update --mode slow --follow=none -f json` reports and full
`cleave facts` dumps were collected for all samples and the flagged game
components. Rizin x86/x64 disassembly, PE parsing, and dnfile/dncil IL decoding
were used to trace effects independently of the reported trait names and ML
scores. Full reports and disassembly are in the task scratch directory;
`check.py` builds reproducible inert controls without distributing specimens.

## Judgments and execution evidence

**61e865f3702b12ce4a26c5a90b9de99a12c65ffc228455eb3390ce54af1eab15 — BENIGN.**
This is tModLoader 2026.08.3.0 for Terraria 1.4.4.9, identifying build commit
c9545cf27d56c456321e1896274c02adf67d0140. Its launch scripts select a platform,
install the requested .NET runtime from Microsoft, and launch the game.

* SDL2.dll is exactly the official SDL 2.28.2 Windows x64 release binary:
  SHA256 76f7d265a3efaba658cbf5cf5ff078a4ad46f25160f961575041d1ca34e932c3.
  Compared the actual DLL bytes with the member in
  [SDL's official release archive](https://github.com/libsdl-org/SDL/releases/download/release-2.28.2/SDL2-2.28.2-win32-x64.zip).
  At VA 0x36b5bd96c it installs a WH_KEYBOARD_LL hook (type 13). At
  0x36b5c876f it loads cfgmgr32.dll and resolves notification APIs. At
  0x36b5c8916 it posts WM_QUIT (0x12) to its device-notification thread.
  These are input/device-event operations, not a loaded DLL handed to a hook
  in a victim process. API co-occurrence did not establish injection.
* tModLoader.dll IL method 0x06000c19, Player.LoadPlayerFromStream, decrypts
  supplied player-save bytes with RijndaelManaged and feeds BinaryReader and
  Player.Deserialize. AchievementManager.Load/LoadExistingAchievements
  decrypt local achievement BSON. Resource access separately serves embedded
  PNGs, translations and mod templates, not an encrypted executable stage.
* Utils.OpenFolderXdg (0x06001047) starts xdg-open with CreateNoWindow.
  UIModSources.IsCompatibleDotnetSdkAvailable (0x06002b4d) captures output of
  `dotnet --list-sdks`. TerrariaSteamClient.Launch (0x06002e36) starts the
  game's Steam helper with a pipe. The two Process.Kill sites stop the tServer
  child on menu cancellation/disconnection. These operations are unrelated to
  resource decryption; the old suspicious resource-stage profile invented a link.
* MonoMod.Core 1.3.2 WindowsSystem.PatchData (0x0600017c, RVA 0x7040)
  changes page permissions, copies a patch and flushes its instruction cache.
  FlushInstructionCache (0x0600017f) explicitly passes GetCurrentProcess.
  This implements local detours for mods; cache flushing plus memory/context
  APIs does not establish cross-process injection or evasion.
* BusyBox's error at file 0x813c3 is referenced at VA 0x464a50 after a failed
  CRT _spawnve call at 0x464a20. A failed shell launch is ordinary process
  behavior. The batch launcher uses BusyBox to run ScriptCaller.sh.
* Basic.Reference.Assemblies.Net80 contains 163 embedded .NET reference
  assemblies (net80.Microsoft.CSharp, Microsoft.Win32.Registry, etc.). Its
  API vocabulary is compiler reference material.

**db29cdd3f495b9414d911d62fcbeffa8dec4ea8710508a188a47f0598db30b49 — MALICIOUS.**
A damaged StormAttack / Shtormec-style native loader, not a demonstrated
GoldenEye/WannaCry encryptor. Entry VA 0x402674 is the MFC startup. Its dispatcher
0x401cb0 selects mode 3 from DWORD 0x404120: 0x401900 writes an HKLM Active Setup
StubPath under a generated GUID, reads its own image, patches and writes a copy
(fwrite at 0x401b26), then relaunches that copy (0x401b7e). Cleanup 0x401390
constructs COMSPEC `/c del` with its own short path and `> nul`, and calls
CreateProcessA at 0x4014b8 and ResumeThread at 0x4014d9.

Alternative mode 1 calls resource extractor 0x402460 and overwrites
LanmanServer's ServiceDLL at 0x40133e with the StormServer.dll path. The injector
0x401150 creates a calc/notepad/IE child, allocates and writes its DLL path into
that child, resolves Kernel32!LoadLibraryA and passes that returned export plus
the remote path to CreateRemoteThread at 0x40123d. Mode 2 installs an automatic
service. These are retained code capabilities, not claims they all ran.

The resource directory/data at file 0x5000..0xec60 is erased (zero nonzero bytes),
so the resource DLL cannot be recovered by the loader. Appended sections carry
unrelated library/string fragments; their presence does not restore a working
DDoS or C2 payload. Code at 0x1000..0x289a has SHA256
98f975dd8b8d9f2e6da736754ef8f87a112e7f7e5f4d104b3f5e385e525c70c4.
The live persistence/self-copy/cleanup path and retained service-hijack/injection
code justify the judgment despite damage. Success on a specific Windows system
was not demonstrated. Microsoft's
[Shtormec description](https://www.microsoft.com/en-us/wdsi/threats/malware-encyclopedia-description?Name=Backdoor%3AWin32%2FShtormec.A)
corroborates the StormServer.dll/LanmanServer replacement and IE injection;
its other payload claims are not attributed to this damaged specimen.

**9f3c76ccea9dcd3a60f98c83833f1954cddfd78898f80656f4e6a53afcf09b00 — MALICIOUS.**
A myRunner / QQpass-lineage association hijacker and mailbox-controlled launcher.
The PE identifies myRunner.exe/HanSoft; those labels alone did not establish the
judgment. Function 0x4061b0 creates the machine-wide EXE open-command key, strips
the wrapper's extension (0x406302..0x406307), appends `"%1" %*`, and writes the
handler through 0x4045c0/RegSetValueExA. It similarly interposes on text files.
Function 0x4054f0 can read its own path/image, write a copy and vary appended
padding. 0x406820 manipulates the TIMPlatform/TIMP1atform replacement paths.
These are deceptive execution interposition, not ordinary file associations.

The POP3 client 0x402d80 authenticates and retrieves messages. Handler 0x408f30
passes retrieved attachments to the decoding/extraction helper, reads a nine-byte
header (0x409084), requires an X tag at 0x40909f, searches the path for its last
dot and tests its preceding digit (0x4090b4..0x4090d4). Depending on that test it
stores a versioned item in the registry or launches the staged path through
WinExec at 0x40913c. This was missed because the old instruction pattern required
a short stack displacement and a .text section; this build uses a long
displacement and an unnamed code section.

The QQ propagation path is also present: 0x409c80 selects one of ten executable
lure names, invokes the self-copy helper at 0x409da1, then calls file-send
automation at 0x409db3. Function 0x409770 locates the QQ send-file dialog,
sets the selected path with WM_SETTEXT and activates its buttons using
WM_COMMAND. Long filler overlay bytes and a small nearly blank RWX section
complicate file layout; no decryption/unpacking is needed to recover these paths.
No file-encrypting ransom behavior was found. Both supplied tria.ge pages were
inaccessible; their reported scores were not used as proof.

## Rule changes and scope audit

* Retire the two generic hostile unsigned-hook/loader API composites. The
  equivalent imported/named API observations already exist as notable traits in
  micro-behaviors/ui/window/hook. Keep the specifically contextual loader rule.
* Retire code-injection-flush and its generic helper. Individual cache, memory
  and context capabilities remain. Inline the same prerequisites and exclusions
  into the only retained exact consumer, ntdll-hotpatch, rather than granting it
  an unconditional match or broadening its previous exemption behavior.
* Retire the resource/crypto/hidden-process co-occurrence objective. Its existing
  notable resource/crypto surface and process atoms retain every supported fact.
  A same-file bucket does not establish a resource-to-process relationship.
* Relocate the shell-spawn failure diagnostic to process/create/shell/native at
  notable severity. Preserve the exploit composite's exact reference to it;
  remove the unsupported hostile inference from that diagnostic plus /bin/sh.
* Relocate the SQLite format string from a database capability to
  metadata/binary/layout/embedded::sqlite-format-header-reference. Preserve the
  original text matcher and native file/platform scopes. It detects an embedded
  reference, not a working parser or a database operation. Update three exact
  consumers. Three old SQLite-directory consumers now use the explicit
  sqlite-api-or-format-reference union, preserving their header alternative.
  The destination's broad layout/binary ancestor consumers are generic layout
  suppressors; all supplied specimens and inert PE controls already carry
  independent layout metadata. None acquired a new suppression in these checks.
* Extend the existing X-tag instruction observation with short/long stack-LEA
  encodings and separately scoped .text/unnamed atoms. The original composite ID
  remains its consumer interface. Pattern operands vary; no filename, host,
  campaign URL, exact size or hash gates the behavioral loader detection.
  No instruction-directory ancestor consumers were found.

## Verification

`check.py SCRATCH_DIR MAILBOX_SAMPLE` passed 13 cases: original/renamed loader,
removed X gate, removed RETR command, both stack-displacement variants in both
section layouts, missing-X and missing-dot controls, ordinary hook/cache APIs,
failed shell launch with /bin/sh, and SQLite reference presence/absence. Inert
PE entry points immediately return; signature bytes are unreachable test data.
The mailbox objective's test-rules precision is 10.9 (authoring floor 3.5).

Final atomscan rescans cover all three supplied paths and SDL2, MonoMod.Core and
BusyBox in isolation. tModLoader and its components have zero hostile and zero
suspicious traits. The StormAttack loader retains four hostile/one suspicious
findings. myRunner has four hostile/two suspicious findings, including the newly
recognized POP3 loader path. Source scores are not used as behavioral evidence.
