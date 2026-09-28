# Keyboard collection, input handling, and synthesis

This pass implements [200 rule moves](keylog-routing-moves.csv), including an
audit of the receiving hook leaf and neighboring input capabilities. The
admissions and tie-breaks are in [TAXONOMY.md](../../TAXONOMY.md). Classification
remains an inference about probable capability; runtime execution is not a
prerequisite.

| Directory | Before | After | Boundary |
|---|---:|---:|---|
| objectives/collection/keylog/capture | 193 | 53 | Legacy remainder; known acquisition methods leave. |
| objectives/collection/keylog/hook | 59 | 59 | Keyboard interception with collection context; generic hooks leave as specific collectors arrive. |
| objectives/collection/keylog/polling | 3 | 9 | Key-state polling. |
| objectives/collection/keylog/device | 11 | 17 | Device/HID acquisition. |
| objectives/collection/keylog/terminal | 13 | 14 | Terminal input collection. |
| objectives/collection/multi-source | 8 | 17 | Independently required acquisition sources. |
| objectives/exfiltration/stealer/input | 34 | 48 | Input export, independent of acquisition technique or transport. |
| objectives/exfiltration/stealer/multi-source | 29 | 30 | Independently required keyboard and screen export. |
| micro-behaviors/ui/window/hook | 0 | 19 | Generic window-hook mechanics. |
| micro-behaviors/hardware/input/keyboard/hook | 41 | 12 | Keyboard-specific interception. |
| micro-behaviors/hardware/input/event | 40 | 73 | General input interfaces, state, and event handling. |

All receiving categories are strictly leaves within 85. The pass removes one
cap violation: the catalog has **153 oversized directories**. It adds breadth
without adding depth or exceptions. Mouse `synthesis` is consolidated into the
existing `simulate` subject; composites spanning keyboard and mouse go to input
events. The old `mouse/robot` observation actually references MouseInfo, so it
moves to pointer information and the empty leaf is retired.

## Why these boundaries are more exact

`SetWindowsHookEx`, hook chaining/removal, and HookOn/HookOff names do not select
a keyboard hook. A keyboard hook type or independent keyboard context supplies
that specificity. pyHook, pyWinhook, iohook, rdev, and generic pynput imports also
support input beyond keyboards. Keyboard-specific subscriptions remain with
keyboard listeners or hooks. System Events `key down` commands generate input;
they are not keyboard collection.

Input device paths and event-name filtering identify device access interests,
not necessarily keyboard collection. Compiler invocations, temporary log name
construction, log filename templates, formatted headings, window-text queries,
and thread startup each follow their own subject. Their consumers retain exact
references. `mouseStates` remains general mouse-state evidence, without claiming
cursor position. The GUI class-name pattern includes SunAwtFrame, so it belongs
in window identification rather than WebView/browser identity.

Local logging follows acquisition mechanism. Explicit input delivery belongs
in stealer/input. Independently required clipboard or screen acquisition can
justify collection/multi-source; optional graphics/window context cannot.
Generic event-value `send` or `write` operations alone are not remote theft.

## Preservation and one detection correction

The baseline contains **118,795 definitions**. The migration proof checks the
moved cohort and its explicit and broad consumers: **386 protected definitions**.
Effective scopes, criticality, confidence, exclusions, mappings, and conditions
are preserved except for the following deliberately tested correction. ID and
description changes clarify the observations; they do not hide findings by
lowering criticality. The manifest records a normalized effective-definition
hash and identifies the changed exclusion.

A focused control exposed an existing self-exclusion in `key-down-lower`:
`event.{0,20}key down` also matches `Events" to key down`. Requiring the whole
word `event` retains the descriptive-text exclusion while allowing the actual
System Events command. Positive automation and negative descriptive-text
controls cover the change.

[Directory-consumer membership](keylog-routing-directory-consumers.csv) records
**76 affected references in 70 consumers**. Directory references follow their
newly precise subjects; historical mixed memberships are not recreated with
aliases. Existing exact references follow every move and rename. No `needs` or
proximity setting is changed. A directory can supply several matching child
IDs, so corpus checks complement structural preservation; relocation alone is
not evidence that every consumer's outputs are identical.

Independent concurrent edits are recorded in
[keylog-concurrent-changes.json](keylog-concurrent-changes.json). They are not
credited to this migration or overwritten to force whole-tree equality.

## Duplicate and validator findings

Two identical atomic matcher bodies touch the moved cohort:

- `/proc/bus/input/devices`: native ELF/C/C++ coverage and Rust coverage have
  different confidence, platforms, and mappings.
- The `stty` command pattern: native and PHP coverage differ in platforms,
  mappings, and exclusions.

Both pairs now share their proper technique leaf. They remain separate because
naively unioning file types would change effective settings or exclusions. A
validator should distinguish **overlapping equivalent definitions to merge**
from **identical bodies with disjoint coverage or differing settings to review**.
It should report those differences rather than encourage a lossy merge. The
Rust `CGEvent.tapCreate` reference and native `CGEventTapCreate` interface also
remain distinct: their matcher spellings and scopes differ.

A useful additional warning would detect positive/exclusion overlap, with a
concrete witness: the System Events example demonstrates a real self-exclusion.
Simple overlapping words alone are insufficient because legitimate exclusions
intentionally narrow broad matchers.

## Remaining precision work

The 53-rule capture remainder still needs individual review. Passing the cap
does not certify its semantics. In particular, Gradle dependency/ProGuard
patterns can describe benign native-hook applications, and the hostile
`bundled-native-global-keylogger` currently requires process startup plus generic
window-hook lifecycle APIs without keyboard specificity. It remains explicitly
unresolved instead of being silently demoted or treated as a reviewed hook
collector. Some hook/HTTP composites likewise lack a required keyboard-specific
source; they were not moved to stealer/input on their names alone.

The next over-cap collection siblings are activity/browser and monitor/tracking.
Their review should separate browser-owned history/state, user interaction,
neutral event handling, local collection, and export. The existing six-rule
surveillance, 29-rule monitor/capture, and three-rule sweep remainders also need
source/control-role review. No legacy bucket is reopened for new ambiguous rules.

Follow-up: the [34-rule sibling pass](INPUT-SIBLING-BOUNDARIES.md) implements
the device/evdev, kernel-notifier, CSS export, and touch cleanup below. The table
retains the findings at this checkpoint; the capture remainder is still open.

The wider sibling audit identified these concrete follow-ups:

| Existing leaf | Finding | Next disposition |
|---|---|---|
| device vs evdev | Both contain direct device acquisition; evdev also contains QNX device/send evidence that is not Linux evdev. | Consolidate true device collection under device, move event paths/decoding to capabilities, and route the QNX keylog stream to stealer/input. Preserve explicit consumers. |
| device | Android database/table/column names do not identify a device acquisition method; touch coordinates are not typed keys. | Classify database/keyboard labels by their subjects; review the store composite independently. Separate touch observation/control from keyboard collection. |
| kernel | Header, array, and device-node creation atoms are generic capabilities. The objective combines a keyboard notifier and exposed key buffer. | Route primitives to their subjects and classify the notifier collection by interception mechanism rather than kernel execution context alone. |
| css-selector | Several composites explicitly fetch remote URLs selected by field values; server routes and an IP-indexed buffer are generic primitives. | Route probable field export to stealer/input; keep selectors, routes, and buffers neutral. Do not classify a demo stylesheet filename as capture by itself. |
| capture | Form-value observation, accessibility text events, keyboard declarations, build packaging, and identity exceptions share one leaf. | Separate field collection from key events; test benign GUI/native-hook packages before repairing intent-bearing Gradle classifiers. Multi-source admission must require independent datasets. |

See the follow-up manifest for completed dispositions. Capture classifiers and
remaining device/HID inference strength still need review.

## Validation result

`make validate` still fails with **77 diagnostics**, including **153 oversized
directories**. The final `validate --soft` run passes **1,840/1,840 verdict
fixtures**. The existing source-routing suite passes **38 assertions across 19
controls**; the new input-routing suite passes **14 assertions across six
controls**. Controls are scanned from temporary locations outside fixture-path
suppressors and are never executed. The final preservation proof passes for all
386 protected definitions, with eight external changes recorded separately.
Thirty-six descriptions were clarified, including 23 local ID changes.

Reproduce focused checks with:

```sh
python3 scripts/check-input-source-routing.py
python3 scripts/check-stealer-source-routing.py
```

The passing controls support these changes; they do not certify the unresolved
classifiers or erase the remaining strict-validation backlog.
