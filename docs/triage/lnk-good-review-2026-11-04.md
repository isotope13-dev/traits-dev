# LNK mislabeled-good review, 2026-11-04

Preliminary static review found `37f5d8444cd7`, a PDF-named shortcut that
runs a WSH script from a WebDAV-over-TLS share, and `d72f571d6dd4`, a
spreadsheet-named shortcut that builds a VBScript downloader, executes the
downloaded PowerShell script with a hidden window and bypassed execution
policy, and removes the VBScript. Both are bad endpoint artifacts. Preliminary
scans report multiple hostile observations for the WebDAV shortcut, but were
run while another rule file was malformed; both samples need complete fresh
scans and validation before labels or moves are recorded.

`03d424960de6` is an executable shortcut example that joins two variables
into `mshta` and starts a remote stage using an example-domain URL. The
existing rule suppresses all example-domain URLs, including this executable
proof of concept. Removing that suppression exposed a separate false positive:
an otherwise similar shortcut whose launched variables do not match the
assignments still triggered both hostile findings. The suppression was
restored pending a match that verifies variable binding; this sample is not
yet ready to move.

The other shortcut samples remain under review.
