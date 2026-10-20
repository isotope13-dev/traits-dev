Source: [NVISO, Keystrokes in Disguise](https://blog.nviso.eu/2026/10/16/keystrokes-in-disguise-forensic-analysis-of-a-digispark-hid-device/).

The article publishes a Digispark sketch that sends Win+R, types a hidden
PowerShell execution-policy bypass and IEX/DownloadString command, and sends
Enter. `digispark.cpp` reproduces the published demonstration; the Python and
keyboard-script fixtures express the same technique with different HID APIs,
destinations, flag order and command aliases. These are static scan fixtures.

Two hostile findings describe separate results: Run-dialog injection carrying
a download-eval expression, and that injected payload carrying hidden-window
and policy-bypass options. The latter joins predicates at the same output
call or STRING directive. Generic output APIs, hidden windows, policy flags,
USB identifiers and the publisher's demonstration domain do not independently
establish an attack. The Python output receiver must originate from a keyboard
layout constructor; an arbitrary file write is insufficient.

Controls cover browser-only automation, downloads without evaluation, missing
Run/Enter events, distant events, comments, prose, unrelated payload literals,
ordinary commands without HID injection, and flags in unrelated strings or
separate output calls. A flag-free injected payload receives only the execution
finding. The output-pattern atoms remain notable and in their capability homes.

Run `python3 testdata/hid-command-injection/check.py [path-to-cleave]` from any
directory. The checker scans fixtures and asserts findings and severity without
executing their contents.

The [German version](https://blog.nviso.eu/2026/10/20/verborgene-tastenanschlage-forensische-analyse-eines-digispark-hid-gerats/)
publishes the same sketch. Submission variants now cover `DigiKeyboard.println`,
CircuitPython layout output ending in LF, and DuckyScript `STRINGLN`, without a
separate Enter operation. These preserve the article's Windows target while
varying the device implementation. The submission and download-eval predicates
must start at the same output operation. An unrelated line output cannot submit
the command; Run-dialog context and the existing payload/concealment gates remain
required for hostile findings.

The [Digispark implementation](https://github.com/digistump/DigistumpArduino/blob/master/digistump-avr/libraries/DigisparkKeyboard/DigiKeyboard.h)
inherits Arduino `Print`; its ASCII table maps LF to Enter. The
[CircuitPython US layout](https://github.com/adafruit/Adafruit_CircuitPython_HID/blob/main/adafruit_hid/keyboard_layout_us.py)
also maps LF to Enter, but does not map CR to Enter, so a CR-only output is a
negative control. Hak5 documents `STRINGLN`'s terminating Enter in its
[DuckyScript reference](https://docs.hak5.org/hak5-usb-rubber-ducky/duckyscript-tm-quick-reference).
Additional controls cover plain `STRING` without Enter, unrelated line outputs,
file writes ending in LF, commented sketches, missing Run events and browser
automation.

The article discloses no malicious hashes, package coordinates or endpoints.
`nviso.eu` is the author's demonstration destination; `Net.WebClient` is a .NET
type. They are excluded from the threat-feed indicator files.
