# PDF mislabeled-bad review — 2026-11-04

Reviewed all 40 snapshot entries with Cleave and Atom, PDF text and object inspection, link and attachment inspection, and rendered pages where text extraction was insufficient. Hopper confirmed 3 bad, 35 good and 2 inconclusive.

`84326ee78871` has a page-open URI action containing a `mailto:` traversal to a Windows executable. Both scanners now identify that exploit attempt; a traversal-modified control clears. `4520ec4fc371` and `b529074b3a3a` present an Acrobat-themed protected-file prompt whose open link downloads a ZIP from unrelated hosts. A new finding combines the shared decoded drawing-template evidence and archive URI in both scanners. A control with the archive link replaced and its unused PDF object removed clears. The template match depends on the observed glyph encoding and may miss differently encoded or redesigned lures.

`ba1355c5e24c` is inconclusive because its quotation/password document points to a shortened URL whose destination was not available for offline review. `4780861a188a` is inconclusive because its payroll-themed prompt contains a QR-style image that could not be decoded despite inspecting the embedded image and rendered page; its destination and behavior remain unknown.

The remaining entries include ordinary manuals, diagrams, forms, books, blank PDFs and inert text. Two large documents have gaps among their numbered PDF objects, but their pages and other reachable objects were readable and contained ordinary educational material. Extracted links and objects did not establish hostile behavior in those samples.

Both scanners were checked against the new detections and altered controls. Full `make validate` passed: 3270 hostile, 2088 suspicious, 9437 notable and 1396 baseline fixture checks.
