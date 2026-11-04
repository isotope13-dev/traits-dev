# XML bad-label review, 2026-11-04

The snapshot contains 40 files. Direct investigation supports **4 bad, 36 good**. Both skills have been applied; final validation/disposition recording follows below. XML queue membership does not determine scanner routing: originals include XML, SVG, JScript-dominant scriptlet markup and Android binary XML.

## Attack documents

* `11852a34d6f6`: QuickTime media-link overflow input. The RTSP source attribute contains a 10,000-byte uninterrupted x86 NOP run (10,807 NOP bytes overall), rather than a normal media URL. This is an executable exploit/PoC document, not a document discussing an overflow. Further script reconstructs an invisible remote iframe from decimal character strings. Added a hostile QuickTime/RTSP/NOP-overflow finding; no successful exploitation on a particular version is claimed.
* `124a5dea8fcd`: SVG automatically reconstructs a Base64 ZIP on DOMContentLoaded, creates a hidden download anchor, clicks it, and redirects the viewer to a shipping website. Its supplied filename presents a PDF-like name with padding before `.zip`. Independently decoded the ZIP: it contains one 1,884,149-byte JavaScript file whose PDF-like name uses nonbreaking-space padding before `.JS`. Static identifier shortening reduces the script to 2,412 characters without executing it. Reconstructing its literal arrays yields a hidden WScript.Shell PowerShell launch with execution-policy bypass, a remote Invoke-RestMethod stage piped into an obfuscated IEX spelling, then script self-deletion. The browser delivery code plus embedded attack implementation establishes bad. Added a hostile SVG hidden automatic download/disguised archive finding. This reports the implemented delivery chain; it does not assert that every target interpreter accepts the unusual identifier characters or that a remote stage remains available.
* `1a6935ac33a7`: Atom feed with an injected script. Statically decoded its comma-separated hexadecimal values plus arithmetic offset; the result creates a remote 1×1 iframe and gates reinsertion with a visit cookie. The surrounding loader reconstructs the code with fromCharCode and executes it through window.eval. Added a hostile finding combining the encoded iframe/1px property sequences and the decoder/eval context. Coverage is the reviewed arithmetic-offset representation, not all possible encodings. The feed's otherwise ordinary content does not neutralize the injected attack code.
* `f5a80b08d46b`: registered JScript scriptlet. It queries running cmd.exe command lines through WMI as a duplicate-run guard, then silently launches a document-named shortcut from a document/ZIP-like path using WScript.Shell.Run with window style zero. Added a hostile scriptlet/guard/hidden document-shortcut launcher finding. It does not claim network exfiltration or registry persistence that this file does not implement.

Both cleave and atomscan now detect all four exact originals (`/var/tmp/xml-payload-controls2.log`). The current file selectors include SVG and JavaScript where actual identification requires them; adding an XML-only rule would have left two originals undetected. Original fixtures and ordinary media-link/feed/foreground-scriptlet/ZIP-export controls are under `testdata/{hostile,notable,baseline}/generated/xml-payload-review/`. No engine feature was added.

Static analysis artifacts are under `/var/tmp/xml-decoded/`. The reconstructed staged command's remote address is evidence of download/evaluation; it was not contacted. No JavaScript, PowerShell or downloaded payload was executed.

## Benign supporting files

The other 36 were reviewed individually through their XML elements, attributes, text, resource chunks and referenced implementations. They include Windows SDK event metadata and schemas, build/IDE filters and settings, Android colors/selectors/vector/bitmap resources, UI layouts, binding redirects, logging configuration, OPML notes, XMP and Office metadata, ordinary SVG artwork/diagrams and a sitemap. Their parent malware/offensive projects do not establish attack functionality in these standalone files.

Five Android binary XML files were independently walked to EOF: declared sizes and every chunk bound are consistent; decoded string pools identify vector drawing paths, colors/state selectors or bitmap attributes, with no manifest receiver, executable script or embedded attack stage. The upgrade-report XSLT's JavaScript only expands/collapses report rows and toggles plus/minus icons. The ImageSnap Xcode scheme selects the normal executable and `-t 1` launch arguments, with no hidden pre/post action. The builder UI's execute-related control labels are data declarations rather than an implementation of the referenced actions.

Notable edge cases remain visible without a hostile inference:

* `29ea5c129ad0` maps Android FileProvider's filesystem root. Added a notable configuration observation; this file does not supply the manifest/export state or an external URI grant, so no actual disclosure is asserted.
* `5b5a3a9953eb` is a standalone worksheet part with ordinary multiplication/SUM formulas and an autoLoad OLE relationship. Broadened the existing notable auto-load observation to XML parts. The referenced relationship and object bytes are absent, so no malicious embedded object is inferred from a generated ProgID.
* `66e8f2c7cd2a` is a SOAP WSMA `sh run` request with a redacted password. It supplies no network endpoint, authentication-bypass delivery path or exploit wrapper. An administrative configuration query alone is not an exploit.
* `dc0a85807395` is a small SVG with a direct document hyperlink and ordinary click-to-open text. It implements no automatic redirect, credential collection or executable payload; an unreviewed remote page is not silently imported into this artifact's verdict.

All matching trait descriptions were reviewed. Full reports/facts for every original are under `/var/tmp/xml-final-review/xml/<prefix>/`; the final batch log is `/var/tmp/xml-final-review-rerun.log`. Final validation and Hopper recording remain necessary before checking the TODO item.


## Final verification and recording

The Python directory walk includes one hidden `.idea` library file omitted by the initial rg file count; the complete snapshot has **40 files**, all scanned and reviewed. All eighty final original checks agree with the direct-review dispositions: four hostile originals and thirty-six benign originals with no suspicious/hostile findings.

Full validation passed (`/var/tmp/xml-sfra-final-validation.log`): 3,319 hostile, 2,096 suspicious, 9,641 notable and 1,420 baseline fixtures. `git diff --check` passed. Hopper successfully recorded all forty individual dispositions; every response reports zero absent and zero failed. Review is complete: **4 bad, 36 good**. Earlier pending notes are chronological.


The SVG delivery finding also covers other document extensions and bracket-notation download/click calls. A hostile DOCX-name/bracket-call variant passes alongside the ordinary archive-export control. Final validation passed after this improvement: 3,320 hostile, 2,096 suspicious, 9,641 notable and 1,420 baseline fixtures (`/var/tmp/xml-variant-final-validation.log`).
