# .NET banking collector and ScreenConnect review

Verdicts are based on recovered code and configuration, not external labels
or scanner scores. No specimen was executed. Initial and final atomscan JSON,
full cleave facts (including decoded text), resolved IL listings, carved
resources and mutation results were retained under the session scratch
directory, bad-triage.

| SHA-256 prefix | Identification | Verdict |
| --- | --- | --- |
| 0468597b0d8f | SPDR16 banking-page keylogger and managed EXE prepender | MALICIOUS |
| b80d07610b81 | ScreenConnect.WindowsClient.exe 25.2.4.9229 | BENIGN |
| 13f8cfe4648b | ScreenConnect.WindowsFileManager.exe 25.2.4.9229 | BENIGN |

## Collector: execution and hostile effects

The CLR entry point, token 0x0600003b, runs the
MicrosoftWindowsProfileSecurity.WindowsSecurity form. Resolved CIL, including
exception handlers and branch targets, was recovered for every managed method.
No method body failed to decode. Short method names obscure purpose, but the
code itself is readable IL; this is not an encrypted Amadey/Rhadamanthys
payload inferred from the collector-assigned filename.

- Form1_Load (RVA 0x22d4) copies/installs the collector under the user's Documents
  directory and writes HKCU CurrentVersion\Run. It creates hidden/system
  directories, extracts the cpm, pdm and keeper managed resources, and starts
  timers and keyboard/mouse hooks.
- Browser timer methods iSCT_T, fSCT_T, gCSCT_T and oSCT_T enumerate Internet
  Explorer, Firefox, Chrome and Opera. They compare MainWindowTitle with a
  list of Iranian bank/payment, card-detail and recharge-page titles. This
  selects financial activity rather than indiscriminate UI event handling.
- gH_KD (RVA 0x3f8c) gates recording on the browser/page state, reads
  KeyEventArgs.KeyValue, tests Char.IsDigit, and writes digits through the
  stored StreamWriter. Enter, Backspace and Tab receive explicit log labels.
- E_M (RVA 0x42c0), subscribed to mouse activity, writes a click label and calls
  CS_M (RVA 0x4058). The latter captures the desktop using CopyFromScreen.
  E_M scales the image to 400 by 400, saves JPEG data under a .dll filename,
  reads it back and reverses its bytes. F_FC similarly closes and reverses the
  keystroke file. These are concealed captured data, not actual DLLs.
- sTT (RVA 0x4ef4) reconstructs SMTP host, sender, recipient and password by
  indexing two keyboard-character alphabets. Constant evaluation recovers
  smtp.gmail.com, port 587, SSL enabled and an identical sender/recipient
  mailbox. The password is 57 characters; it is intentionally omitted here.
  It enumerates capture directories, attaches their files to MailMessage,
  includes machine/user/OS/core-count information, and invokes SmtpClient.Send.
  It marks sent directories with STF.dll. The timer interval is 360000 ms.
- cpm and pdm are executable infectors. cpm traverses fixed drives other than
  the Documents volume; pdm targets removable drives. They enumerate EXEs,
  reject already marked files, read the collector and original host, then
  write collector bytes, 96 backticks, and original host bytes. They delete
  the original and move the replacement into its path.
- keeper restarts the collector and maintains its Run entries. Its cRTMTT
  method removes its own Run value while regedit/taskmgr is present, restoring
  it afterward. This is concealment; those process-name references do not
  prove that it terminates either tool.
- The submitted file is itself infected: the collector's mapped raw image ends
  at 0x14200 (82432), followed by 96 backticks and a native host at 0x14260.
  Form1_Load checks the delimiter and restores/starts the host. The native
  host's PDB names RFTMP; its ordinary runtime imports account for several
  apparent debugger/API-resolution leads. No process injection or AV-killing
  behavior was inferred merely from those imports or the INJ directory name.

Concrete financial input interception, concealed screenshots, automatic email
delivery and modification of other executables justify MALICIOUS independently
of the queue's family labels.

## ScreenConnect: purpose, launch paths and limits

Both binaries declare version 25.2.4.9229 and Connectwise, LLC. Cleave verifies
their Authenticode content digests and signer cryptography, and both have CLR
strong-name signatures. The complete 10520-byte trailing region in each file
is its WIN_CERTIFICATE table; neither has bytes after that table. Signature
integrity is supporting evidence, not the verdict or a claim about current
certificate revocation/trust.

The WindowsClient entry point is token 0x060003eb, RVA 0x1843c. Main dispatches
explicit RunFile, RunFileElevated, StartService, Rerun and RunRole arguments.
For normal sessions it parses an argument URI/query or ClickOnce ActivationUri,
applies ClientLaunchParametersConstraint, and creates SocketEndPointManager
with the resulting parameters. Missing parameters raise an ArgumentException.
RunRole uses a named-pipe endpoint. The client creates its GUI, notification
icon, endpoint/event handlers, input and display processing, file-transfer
handlers, clipboard and sound components. These match remote support/client
functionality. The debugger-attached branch opens a TraceForm; it does not
gate execution to evade analysis.

The FileManager entry point is token 0x06000006, RVA 0x20a0. It creates a shell
file-open dialog rooted at ProfilesDirectory. Its hooks are current-thread
WH_GETMESSAGE/WH_CALLWNDPROCRET and UI event hooks, used to customize shell
views, context menus and drawing. OnFileOk obtains the selected shell item and
calls Process.Start with UseShellExecute=true. It is an interactive local file
browser helper, not a standalone RAT or a keylogger. No network client,
hardcoded relay, command polling, stealth persistence or download execution
was recovered from its methods.

Both assemblies reference ScreenConnect.Core and ScreenConnect.Windows;
WindowsClient additionally references ScreenConnect.Client. The dependencies
were not present beside these standalone samples. Retrieval of the matching
vendor distribution was attempted: the release CDN returned HTTP 403 and the
two historical download hostnames did not resolve. The current
[vendor download page](https://www.screenconnect.com/download) requires license
access. Consequently, no unavailable DLL is represented as analyzed. No
payload URL or session endpoint is embedded in either supplied file; the HTTP
URLs in their signature data are DigiCert certificate/CRL/OCSP references.
The vendor also documents the normal client ZIP/session workflow in its
[2025.4 release notes](https://docs.connectwise.com/ScreenConnect_Documentation/ScreenConnect_release_notes/ScreenConnect_2025.4_Release_notes).

There is no concrete hostile behavior or supplied hostile deployment
configuration in these two files. BENIGN describes these artifacts; their
remote-administration capabilities remain notable. External RiskWare,
RemoteAdmin and Unwanted labels, and association with an abusive deployment,
plausibly explain their presence in the malware queue without making the
stock components intrinsically malicious.

## Detection changes and boundary checks

Three hostile composites now cover bank-page keylogging, combined input/screen
capture with SMTP attachment-send code, and managed executable prepending.
Their required facts describe target selection, input-to-writer IL, attachment
send IL, two array-write loops around a delimiter, and executable
traversal/replacement references. Tokens/field indices vary; no hash, exact
file size, mailbox, dropped filename or campaign path gates these detections.

The ScreenConnect client-service/client/file-manager identities now inspect
OriginalFilename rather than treating every reference to those components as
the component itself. Core/Windows assembly references are retained under
metadata/import/package, and the certificate subject under
metadata/signed/certificate/subject. Product-specific signer classification
also requires ScreenConnect product metadata. Existing consumers were updated.

The former LZMA detections at 0x3cb8f in WindowsClient straddled MethodDef
metadata fields: Name_StringIndex=0x5d98, signature index and parameter-list
index. There is no compressed payload at that address. Sized-header matching
now requires zero high size bytes and the range decoder's initial zero.
The three raw header observations moved to metadata/file/magic/numbers;
explicit consumers retain their corresponding references.

Imaging namespace and generic Save member references now live with import
and symbol metadata. PNG format reference remains in image encoding and is
notable. Managed GetKeyboardState is no longer downgraded to baseline.

check.py passed 15 controls: all three supplied specimens; collector mutations
removing bank targets, digit recording, hook installation, SMTP and byte
splicing independently; three genuinely decompressible sized LZMA streams;
three implausible-size near misses; and the CLR table lookalike. The two
ScreenConnect specimens must have zero hostile/suspicious findings. The
collector must retain all three new hostile behaviors.

Run the reproducible controls with the three original paths and a scratch
output directory:

    python3 testdata/taxonomy/dotnet-bank-screenconnect/check.py \
      --collector <0468597b0d8f sample> \
      --client <b80d07610b81 sample> \
      --file-manager <13f8cfe4648b sample> --output <scratch directory>

