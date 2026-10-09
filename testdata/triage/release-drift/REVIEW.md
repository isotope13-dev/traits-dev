# Release comparison triage

All three samples are benign; the reported evidence is unchanged in the
immediately preceding upstream artifact. The earlier judged artifact was not
identified in the request, so these comparisons use the immediate predecessor.

* Tekton plumbing: Go proxy v0.0.0-20201021134219-08c5b6a958b2 versus
  v0.0.0-20201021153918-6b7e894737b5. Only go.mod/go.sum change: an upstream
  google/go-licenses dependency update. addpermissions.py is unchanged. It
  fetches the project's Boskos YAML, parses the nested configuration, and grants
  caller-selected users the documented GCP roles through gcloud argv. Default
  yaml.load is a deserialization hazard, not evidence of a dropper or C2.
* Boost skill CLI: PyPI wheels 1.2.187 versus 1.2.188. updatediff.py is
  byte-identical. Changes implement retryable quarantine and honest reporting
  when agent symlinks cannot be removed. The override phrase is an illustrative
  module docstring; added lines are passed to injectscan for defensive review.
  The installed producer retains two delimiter quotes in that docstring's
  literal value, despite exclude_docstrings. Recognize this scanner module by
  its product-specific documentation title, rather than package/filename.
* Rask.Wasm: NuGet 0.23.1-alpha.0.248 versus 0.23.1-alpha.0.264, repository
  commits 8cd5678dbb4a4649b01ae13ed2a0c9bd250cf1d3 versus
  306ffbb7eb93b8b2d43602315ae54adce1277d81. All target files are byte-identical.
  Task implementation source is unchanged; compiled assemblies carry release
  metadata differences. Changed runtime source implements event batching,
  lifecycle navigation and UI behavior. The Tailwind task downloads a pinned,
  SHA-256-checked compiler into a cache, then builds CSS. WASM tasks stage
  scoped assets. Rizin confirms managed task assemblies, not native payloads.

## Trait corrections

Move YAML/HTTP proximity into YAML serialization, notable, explicitly claiming
co-occurrence rather than source-to-sink flow. Move task registration plus a
pre-compilation target into build-manifest metadata, notable, without claiming
the target invokes the task on every build. Property-expanded AssemblyFile
paths are named for that evidence, rather than assuming package ownership. Remove their unsupported attack
mappings. Add a notable gcloud IAM command-literal observation. Existing direct
remote execution and explicit unsafe YAML rules are unchanged.

Replace the bare analyze_untrusted_content helper-name suppression with the
recognized Boost review-gate identity; a helper name alone proves no defense.

No consumers reference either moved local ID. Exact and ancestor selectors
were reviewed. The neutral destinations are existing rule-bearing leaves.

## Controls

http-yaml.py and build-task.targets must expose the relocated notable traits;
local-yaml.py and task-only.targets must not. override-doc.py must not expose
an override trait; override-live.py and assigned-triple-prompt.py must retain
code-embedded override detection. These include live prompt constants so the
scanner exception cannot become a blanket Python or triple-quote exclusion.

## Judgement summaries

Tekton plumbing: unchanged YAML; classify HTTP/parser co-occurrence
Boost skill CLI: unchanged defensive docstring; recognize review gate
Rask.Wasm: unchanged build hooks; classify task declarations as notable

Focused controls passed: both relocated observations positive, both near misses
negative; commented declarations excluded; documentation excluded; ordinary and triple-quoted prompt literals
retained. Full specimen rescans report no hostile or suspicious YAML findings.
