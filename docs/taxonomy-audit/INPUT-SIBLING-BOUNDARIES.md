# Direct input devices, notifier hooks, CSS export, and touch

The [34-rule manifest](input-siblings-moves.csv) completes the next sibling
cleanup identified in the [keyboard audit](KEYLOG-INPUT-BOUNDARIES.md). The
placement contracts are in [TAXONOMY.md](../../TAXONOMY.md). This pass removes
three alternative or mixed technique leaves without adding depth.

| Leaf | Before | After | Disposition |
|---|---:|---:|---|
| collection/keylog/evdev | 8 | 0 | Retired; direct-device collection, neutral input handling, or input export. |
| collection/keylog/kernel | 6 | 0 | Retired; notifier collection joins hook, primitives follow capabilities. |
| collection/keylog/css-selector | 11 | 0 | Retired; input export or neutral selectors, routes, paths, and form handling. |
| collection/keylog/device | 17 | 9 | Direct keyboard-device acquisition; no database labels or touch coordinates. |
| collection/keylog/hook | 59 | 60 | Adds notifier interception with mapped key-buffer exposure. |
| collection/keylog/capture | 53 | 54 | Adds a key-record store whose acquisition mechanism is unspecified. |
| collection/touch | 0 | 1 | Remotely tasked touch-coordinate collection. |
| exfiltration/stealer/input | 48 | 54 | Adds CSS input oracles/receiving service and QNX keylog delivery. |

Paths omit the objectives prefix. All receivers are strict leaves within 85.
The device/evdev overlap is resolved rather than retained as two reasonable
homes. The catalog still has **153 oversized directories**; this sibling cleanup
improves semantics without claiming another cap violation was resolved.

## Decisions

Direct input-event device collection belongs in device, including evdev. Its
pathname glob does not independently imply reading, and an unpack format does
not require keyboard-event filtering. A key-code/character format string is not
itself a file write. QNX device references were particularly misleading under
evdev; the combined keylog/socket delivery rule now follows the information it
sends. The send atom specifically pairs named keylog flushing with a socket
send, so it retains its input-export meaning without asserting C2.

Kernel keyboard notifiers intercept input. The complete notifier/key-map/buffer
exposure composite belongs with hooks; its header, event-code test, array names,
copy-to-user operation, and character-device command retain their own subjects.
A device node is not necessarily a keyboard. A hex-encoded keyboard path remains
a path observation; encoding alone does not establish its purpose.

CSS field-value conditional resource requests and the corresponding character-
log receiving service belong in input export. Their original evidence strength
is preserved: relocation does not add runtime or data-flow proof. Selectors with
unspecified/local image URLs, parameterized routes, an IP-indexed buffer, and a
stylesheet pathname remain neutral capabilities. The former demo-page rule only
requires a password field, attribute-setting context, and `/bad.css`; its new
name and form-input home stop asserting keylogging from those observations.

Database/table names naming keyboard records are keyboard labels. `TypedText`
alone names typed content, not necessarily a database column. Their combined
store signature supports recorded keyboard data but leaves the acquisition
method unspecified; it cannot earn a direct-device home. It remains in the
explicitly documented capture remainder pending its mechanism/recording audit.

Raw touch reading and coordinate decoding are input-device capabilities. A
remotely tasked agent with those capabilities supports touch collection. Touch
positions do not establish keystrokes without keyboard mapping evidence. The
new touch category is registered in the validator and documented alongside the
other collection sources; it is not a cap exception.

## Preservation and consumer review

The pre-move catalog contains **118,795 definitions**. Pre-write normalization
checks the whole catalog. The final proof protects **66 moved or affected
consumer definitions** and preserves every effective matcher, scope, exclusion,
confidence, criticality, mapping, and threshold. Twenty-one descriptions and
20 local IDs were clarified. No detection condition changes were required.
No identical atomic if-body overlaps touched this migration cohort.

[Directory membership changes](input-siblings-directory-consumers.csv) cover
**32 references in 30 consumers**. Collection-wide references shed generic
primitives and completed exports. Input-export consumers acquire the source-
appropriate rules. No compatibility aliases recreate the mixed memberships,
and no proximity or `needs` settings change. Whole-corpus and focused checks
complement structural comparison because a directory reference can contribute
several child findings to a threshold.

The final proof records any outside edits separately in
[input-siblings-concurrent-changes.json](input-siblings-concurrent-changes.json).
At this checkpoint the post-baseline drift list is empty. Changes predating this
batch's baseline may still explain small differences from the preceding shared-
tree snapshot.

## Remaining work

The keylog/capture remainder has 54 rules. Its build/package classifiers, form
observation, accessibility surfaces, intent strength, and identity exceptions
still require individual review; passing the cap is not semantic certification.
The device leaf's remaining HID classifiers also need benign-control review,
especially combinations whose callback/device context leaves keyboard type
optional. Known-method classifiers should not be left in capture merely to
avoid checking their consumers.

The next over-cap collection leaves remain activity/browser and monitor/tracking.
The six-rule surveillance, 29-rule monitor/capture, and three-rule sweep
remainders retain their previously documented source/control ambiguities.

## Validation

The rebuilt CLI passes **1,840/1,840 verdict fixtures** with `validate --soft`.
`make validate` retains **77 diagnostics**, including the **153-directory** cap
backlog. The input suite covers **30 assertions across 15 fixtures**; the source
routing suite adds **38 assertions across 19 fixtures**. All **68 assertions**
pass. New controls distinguish remote/local CSS resources, an input path from
an event record, local keylog storage from socket delivery, a notifier from a
key-buffer collector, and raw touch reading from a remotely tasked collector.

The initial touch fixture was a shell script, outside the existing composite's
source/binary scope. The corrected Java control actually invokes getevent and
reads coordinate records, and overlaps the remote-collector rule's Java scope;
its negative result is not a file-type exclusion. No coverage settings were
changed to accommodate the test. Fixture contents are scanned from temporary
locations outside testdata-path suppressors and never executed.

The validator build used the existing isolated Cargo workspace with local
filefacts/stng dependency overrides; the shared checkout's manifest and lockfile
were not changed. The only engine edit in this pass registers the documented
touch collection category. Reproduce focused checks with:

```sh
python3 scripts/check-input-source-routing.py
python3 scripts/check-stealer-source-routing.py
```
