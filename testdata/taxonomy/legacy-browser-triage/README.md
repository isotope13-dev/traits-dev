# Legacy browser triage fixtures

All three original specimens are HTML, despite their collector names.

* BadJoke.RJump is a Portuguese Windows Update results page with an appended
  browser prank. Its independent trailing script passes syntax checking,
  starts a 10 ms string callback, increases the displacement variable by 0.1
  per tick and calls self.moveBy with two random coordinates. The earlier
  legacy JScript error handler is invalid in a modern JavaScript parser, but
  that does not invalidate the separate trailing script. Verdict: MALICIOUS,
  with suspicious prank/UI-abuse traits rather than exploit or theft claims.
* Exploit.JS.Agent.ut uses Dean Edwards Packer. Static token substitution
  reconstructs a NCTAudioFile2 SetFormatLikeSample overflow (CVE-2007-0018).
  It fills 50 roughly 4 MiB heap blocks with NOPs and a 334-byte x86 payload,
  then passes 5200 bytes of 0x0c to the ActiveX method. Disassembly shows a
  PEB walk, PE export ROR13 resolver, LoadLibraryA and GetProcAddress, a
  URLDownloadToFileA call saving to ..\v, and WinExec on that same path,
  followed by ExitProcess. The payload URL is an executable download on a
  long qqsafe-qqservices-themed domain. Verdict: MALICIOUS. Its traits use
  control/API identity and reusable shellcode words, not that domain.
* WindowBomb.d is a Big5 forum page with two injected Netscape-bomb replies.
  Each script literally begins with <p><br>; raw-text script parsing retains
  these tags, causing SyntaxError at '<'. The body onload handler therefore
  cannot call WindowBomb. The alert and popup bomb snippets establish attack
  intent but do not establish successful denial of service. Verdict:
  MALICIOUS, with two suspicious malformed-code findings and no hostile traits.

Scripts were syntax-checked with JavaScriptCore through a bounded Python
harness. Browser APIs were stubbed; no native shellcode was executed. The
jitter callback produced increasing displacements; the reconstructed exploit
passed 5200 bytes to its stubbed trigger. Rizin decoded the native payload.
The Windows Update script host and payload domain failed DNS resolution;
no dependency or downloaded executable was available to inspect.

The adjacent cases.json records positive and near-miss expectations. Controls
cover ordinary timer/UI markup, method-only ActiveX use, local image sources,
Arabic prose and Big5 prose. The image and username-field relocations preserve
matchers and scopes and update all exact YAML consumers. No YAML parent
selectors consume the moved image or username observations. The PEB word
observation moves from payload/header to current-process information, with
its exact consumers updated and the second packed-dictionary ordering added.
The existing Packer and encoded-URL facts remain valid encoding observations.
The Arabic-script matcher now requires multiple word pairs; random valid
UTF-8 fragments inside Big5 data no longer identify its language as Arabic.

Vulnerability reference: https://www.kb.cert.org/vuls/id/292713
