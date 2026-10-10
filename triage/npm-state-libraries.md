# npm state and RDF library triage

All three specimens are BENIGN. Scans and facts were collected for each
original archive, and the manifests, executable source, compiled entrypoints,
and Smartstate's dependency source map were inspected without executing code.

- e7ef2fea8b57: @metamask/connectivity-controller 0.3.0. The controller
  subscribes to an injected connectivity adapter, reads its initial status,
  and updates controller state. Selectors expose online/offline status. No
  install hook, credential acquisition, or unauthorized transfer was found.
  No trait change was necessary for this specimen.
- e837a792c5a5: @push.rocks/smartstate 2.3.3. Reactive state management with
  middleware, batching, computed state, observable scheduling, and optional
  IndexedDB storage. State hashing prevents duplicate notifications. Bundled
  Smartenv dynamically imports local modules and supports caller-supplied web
  modules; its Linux comparison is ordinary platform compatibility logic.
  The source map exposes the bundled dependencies, including RxJS, date-fns,
  Lodash, js-base64, Smartenv, Smarthash, and Webstore. No malicious payload or
  secret-to-network chain was found.
- e7f99e05fad1: @shexjs/term 1.0.0-alpha.28. Converts RDFJS, JSON-LD-style,
  and Turtle terms. parseInt(..., 16) and String.fromCharCode implement Turtle
  Unicode unescaping, including surrogate pairs. IRIs are RDF identifiers.
  No trait change was necessary for this specimen.

## Corrections and controls

Removed the duplicate `js-linux-gated-ssh-backdoor` atom, whose entire matcher
was `os.platform() === 'linux'`. Its consumer now uses the canonical
`micro-behaviors/os/sysinfo/platform/branch::js-platform-linux-check`.
That trait remains an explicit, notable Linux-platform comparison. Existing
broader equivalent spellings (process.platform, quote and whitespace variants)
are retained; no key installation is inferred from the comparison alone.

Replaced `zero-argument-select-call` with `active-element-select-call`, requiring
an executable call to `document.activeElement.select`. The generic matcher
previously classified `statePart.select()` as form-input behavior. Updated the
clipboard consumer to describe explicit active-DOM selection beside copying.
This deliberately requires a supported DOM receiver; unbound variable select
calls no longer qualify as DOM selection.

Controls in testdata/triage/npm-state-selection were checked with test-rules:
DOM selection and its nearby clipboard composite match; statePart.select does
not match the DOM trait; the Linux-platform comparison matches the canonical
neutral trait. No directory was added. The removed objective atom's sole exact
consumer was updated, and references to the old select ID were updated.

Final atomscan rescans of the original archives: all three have ML level -1,
zero suspicious traits, and zero hostile traits. Network, execution, hashing,
and encoding observations remain notable. cleave facts on the original
archives and relevant executable members reported no extraction errors.

Judgement marker lines (also used verbatim in the commit body):

MetaMask connectivity controller 0.3.0: no change
Smartstate 2.3.3: correct platform and DOM select trait claims
ShEx term 1.0.0-alpha.28: no change
