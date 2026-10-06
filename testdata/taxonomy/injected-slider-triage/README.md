Reasoned review of SHA-256 659d9faec2f8, d60633f19be7 and 8a69b1cdcb8d
(prefixes identify the full sample hashes supplied in the task).

The XML is a benign Circutor EDS command-injection verification payload:
its unconditional event runs `id` through a semicolon breakout and writes
one local marker. This establishes probe syntax, not destructive intent.

The JavaScript samples are Slider Revolution 6.0.4 and 6.5.2 with appended
NDSW/Parrot TDS loaders. Isolated execution with an intercepted XHR and eval
confirmed: an external referrer and no cookies enable an asynchronous GET
to a PHP proxy with a randomized id; responses containing ndsx are evaluated.
Same-host referrers and visitors with cookies issue no request. No live
endpoint or response payload was fetched. Both stripped UI portions scan
with zero hostile or suspicious traits.

Corroboration: https://blog.sucuri.net/2022/06/analysis-massive-ndsw-ndsx-malware-campaign.html
This corroborates the loader family and mechanism, not these exact hashes.

Changes distinguish switch labels from object keys, animation masks from
redaction, UI action dispatch from model decisions, comparisons from writes,
substring arguments from parseInt's radix, nested callback flags from listener
capture flags, and ternary property accesses from CSS height declarations.

Placement changes:
- Retire the unconsumed Bpoorman short-key schema rules: arbitrary short keys
  do not establish family identity or a useful standalone capability. The
  original crd matcher also mistook switch case labels for object keys.
- Generic decision switches move from data/llm/decision to control-flow/dispatch.
  Consumers of action dispatch use the existing canonical action-switch trait.
- NDSW identity moves from command-and-control/dropper to
  well-known/malware/downloader/parrot-tds. Library compromise independently
  requires the library registry, HTTP wrapper and concealed-response dispatch.
- Retired approximate function(E)/eval callback atom uses the existing direct
  eval-call observation for unobfuscated family variants.

The JSON cases record positive and near-miss controls. Full-sample scans,
stripped-library controls and hostile precision traces are recorded in the
session scratch directory. No dependency-fetch findings apply to these files.

XML command declarations live under data/config/schema; they describe an
execution configuration, without asserting that a process has been created.
