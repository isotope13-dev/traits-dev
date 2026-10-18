# EasyEyes runtime second review

The archive SHA256 is
`67135d53944a837b714830a9296bebb083b40bc600010cda98807c8d642076ad`.
It is `@easyeyes_threshold/runtime` version `1.20261015.57781`, a browser
psychophysics experiment runtime. The archive remains **MALICIOUS** because
its delivered JavaScript includes an independently harmful SweetAlert2 routine.
This judgment concerns shipped behavior, not the experiment authors' intent.

## Execution evidence

Both supplied HTML entry points load `js/threshold.min.js` as an ES module.
Its asynchronous module initializer executes the SweetAlert2 routine before
experiment scheduling. The routine requires a Russian browser language and a
current page host ending in `.ru`, `.su`, `.by`, or `.xn--p1ai`. It stores the
first-visit date under `swal-initiation`. A later initialization more than
three days afterward schedules a 500 ms callback that disables pointer input
on the document body, appends looping audio sourced from
`https://flag-gimn.ru/wp-content/uploads/2021/09/Ukraina.mp3`, then schedules a
playback attempt 2500 ms later. Playback rejection is ignored. Browser autoplay
policy may reject the audio; that does not prevent the preceding input lock.
This is conditional sabotage, unrelated to conducting an experiment.

`trace-regional.py <threshold.min.js>` extracts and evaluates only that exact
routine using QuickJS and mocked DOM, storage, timers, and audio. It performs
no network access. `regional-trace.json` records nine controls: new visit,
exactly three days, more than three days, all four eligible suffixes, another
language, another suffix, and an eligible-looking nonterminal suffix. The
sabotage effects follow the gate in each case.

The source map recovers 63 initial modules, including Sentry, experiment
state, PsychoJS, and Pixi. The remaining bundle was inspected directly after
formatting. Other dynamic execution belongs to logging expression evaluation,
rendering helpers, and bundled library functionality. Decoded Unicode layers
include localization and embedded document/UI text. Minification, encodings,
media capture/calibration, data export, and HTTP requests were retained as
neutral capabilities, rather than used as malware evidence.

The three separately fetched GitHub assets are **BENIGN** frontend chunks.
`behaviors` wires page events, form requests, logout storage cleanup and page
updates. `code-view` implements repository-file UI, clipboard actions, editing,
and user-triggered raw-file download through fetch/Blob/object URL.
`app-runtime` reports browser errors and page/event telemetry to configured
collectors, using sendBeacon/fetch, and maintains browser session state.
They were reached through a GitHub license page; that fetch relationship is
not an execution or dependency path from EasyEyes. They have no hostile or
suspicious findings after review. Content hashes and retained hostile IDs are
recorded in `scan-results.json`.

## Trait changes and coverage

- Tighten extension-ID collection names to exclude image `externalIDs`, and
  require a browser namespace for the downloads API, excluding Tone.js queues.
- Retire the bare `is-ready` malware marker: it was a PsychoJS CSS class. The
  WSHRAT composite reuses the existing POST-specific protocol observation;
  its original multi-command fixture still matches.
- Replace quoted English-word matches for TypeScript annotations with actual
  type-annotation nodes, under source declarations. Calibration verification
  code is no longer described as a shell command instruction.
- Move PluginArray/MimeTypeArray references from anti-analysis to browser type
  references, stylesheet-URL/fetch proximity to HTTP resources, deployment-host
  references to cloud HTTP services, frame embeds to HTTP resources, and the
  generic remote/encoded URL alternatives to URL endpoints. Their consumers
  retain the same named alternatives and scopes. No flow is inferred from
  proximity alone.
- Move the small-JS high-entropy-string metric to string populations and the
  whitespace ratio to text shape. These describe analyzed units, including
  decoded child units, rather than implying the outer bundle is small.
- Move the XOR/modulo/indexing umbrella from cryptography to arithmetic:
  required evidence does not establish a cipher. The arithmetic leaf audit
  also relocates a precision/result function-name matcher to function names;
  operation detection and naming no longer share a feature.
- Retire the unconsumed reverse-string bundle aggregator and generic Client
  token as attack evidence. Remove the generic constructor-return helper from
  numeric obfuscation. The renamed split-decoder rule now states its actual
  two-fragment decoder-name concealment requirement; this intentionally also
  detects name assembly without that unrelated constructor helper.
- Inline HTTP COM alternatives in the WSH execution consumer, preserving its
  conjunction while removing an HTTP-only finding from shell creation.
- Give the existing json-ts identity composite notable criticality, consistent
  with its required identity evidence, after retiring its generic suppressor
  consumer.

These are targeted moves, not leaf splits. Other source rules remain in their
existing leaves. Exact references and ancestor selectors were reviewed;
intent is no longer inferred from the relocated neutral observations. No
sample filename, package allowlist, or campaign URL gates a conviction.

Run `python3 testdata/taxonomy/easyeyes-second-review/run.py` for focused
positive and near-miss controls. It copies fixtures outside test-named paths
so test exclusions cannot manufacture passing negatives. Debug evaluation
also verifies low-tier and pure-OR findings filtered by the scan renderer.
