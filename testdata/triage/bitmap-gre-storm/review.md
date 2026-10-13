# Bitmap loader, encrypted GRE bot, and Storm installer

Judgements are based on static control flow and recovered payloads. No sample
was executed. Native functions used for configuration recovery were emulated
in Unicorn without OS services; allocator/copy calls were intercepted.

## a666c1bded48 — malicious .NET RGB bitmap loader

PE32 CLR application `KnJz.exe` contains a Vietnamese clothing-shop WinForms
application. `Program.Main` constructs `DangNhap`; `InitializeComponent`
(RVA 0x2224) retrieves a bitmap resource, calls `Extract1` for 43,008 bytes,
converts the collected bytes to an array, and calls VB `LateGet` on
`AppDomain.GetDomain()` with a concatenated `Load` member name. The result is
cast to Assembly, followed by GetTypes, GetMethods, and LateCall/Invoke.

`Extract1` (RVA 0xb5f8) traverses pixels column-first and appends R, G, and B
channels. The 121x120 BMP yields an MZ/CLR assembly at its first RGB bytes.
That SmartAssembly-obfuscated helper retrieves a second bitmap, crops it to
333x333, reconstructs column-first BGRA bytes, reads a four-byte length, and
XORs 440,833 bytes with a derived byte and a repeating key. Recovered output
is another obfuscated CLR DLL, declaring Noogen.Validation metadata. These
version strings do not establish a legitimate product or AgentTesla identity.
The execution chain independently establishes malicious concealment.

Detection requires byte-collection IL plus sized helper/array/late-dispatch
cast IL and the appropriate CLR member references. It fixes the missed
collection sequence's intervening local load. The broad legacy bitmap
"extraction" rule merely recognized bitmap readback; its consumers now use
the actual channel-collection evidence. In-memory execution additionally
requires type/method enumeration and VB invocation. CodeDOM namespace presence
from GeneratedCodeAttribute is no longer treated as compiler capability.

## a91330492f05 — malicious Mirai-derived GRE flood bot

Stripped, statically linked i386 ELF. Function 0x0804dad0 initializes a
50-entry encrypted configuration table; 0x0804d350 unlocks entries and
0x0804d540 relocks them. Recovery includes DMI virtualization targets,
packet-capture process names, shell names, /proc paths, and OOM adjustment.
The decoder combines a permuted RC4-like state, LFSR feedback, and rotated
byte masks. The primitive rule makes no direction-specific decode claim.

The attack code constructs IPv4/GRE/inner IPv4/UDP headers around 0x08054bde,
recalculates checksums, emits raw packets through sendto at 0x08054f61,
and iterates targets with an unconditional backward branch. Other packet
routines construct TCP, UDP, and IP-in-IP traffic. The family discriminator
combines this attack profile, its configuration permutation seed, and a
Source Engine query marker. No filename, IP, campaign hostname, exact size,
or whole-file hash gates either hostile rule.

## ab8e0a1c191f — malicious StormAttack installer

Native PE32, not WannaCry. The code at 0x00401260 replaces LanmanServer's
ServiceDLL with a System32 StormServer DLL. Other routines extract resource
bytes, write files, inject LoadLibrary through remote memory/thread APIs,
create services, and write Active Setup StubPath. Existing YAML detects
service hijacking, injection, and StormAttack identity: three hostile traits.
No Storm-specific change was necessary.

## Verification

Fresh atomscan JSON and cleave facts were collected for all three originals.
Hostile precision checks exceeded 3.5. Mutated copies removing GetPixel or
LateGet lose the bitmap-hostile findings; removing the RC4-LFSR instruction
sequence or GRE header constructor loses both Linux hostile findings.
Removing only the Source query marker loses family attribution while retaining
the independently supported GRE-flood finding. These are discriminating
near-miss controls, not claims that modified malware is benign.
