# HTML metadata review

## Samples and judgments

- `a60f8d431b42ced7cf0fdf36eaa33a5c47f5f20a38d8cfe3a63abe122d59bb76`:
  **BENIGN**, 8,280-byte HTML “Command Summary for sed” from the claimed
  “sed & awk, Second Edition” reference. Full content describes sed's labels,
  branching, pattern/hold space, substitutions and file read/write commands.
  These are prose and markup, not executed commands. Book provenance is a
  document claim, not independently authenticated.
- `bef140a1a96994029153dca8c00b1750b9a5a764fb9db2dc68d7bb40e8a29e8a`:
  **BENIGN**, 92-byte HTML with a “504 Gateway Time-out” heading and the
  message “The server didn't respond in time.” No original response URL or
  failed upstream payload is available, so the upstream site is unassessed.

Both hashes were verified. Entire byte streams and parsed tags/attributes were
reviewed. Neither has scripts, executable attributes, forms, redirects,
embedded objects, styles, resource links, comments, character entities,
unexpected control bytes, appended payloads, or encoded blobs. The sed page's
only attribute is `class="option"` on a span. Thus rendering displays text
without a code-execution path or external resource request. There are no URLs
or dependencies to fetch. `cleave facts` confirms no symbols, literals,
references, archives or extraction errors; no decoded layers are reported.
The facts extractor's `ShellCmd` tags on prose mentioning sed do not imply
execution.

Queue reputation does not outweigh the actual content. Possible explanations
are incidental documentation collected with a hostile artifact, a source
mislabel, or, for the timeout page, collecting an error response from a
flagged location. These are hypotheses: the source's actual reason and original
deployment context are unknown. The verdicts apply to the supplied bytes.

## Trait correction and preservation

`metadata/package/documentation/page::static-html-shell` moves to
`metadata/document/html::html-root-at-start`. Its anchored HTML-root regex,
byte range, file types, platforms, confidence and baseline criticality are
unchanged. An opening tag proves neither static content nor documentation;
HTML document structure is the nearest supported taxonomy home, rather than
package documentation. The target is an existing admitted leaf. All exact YAML
consumers and the live Windows SDK/SVN mapping were updated. Twenty-six
ancestor-directory references select the old atom: all occur in exclusion or
downgrade lists. Twenty-five retain their old scope by adding the exact new root ID
alongside its documentation selector, rather than selecting all HTML metadata.
One deliberate coverage correction removes the bare-root exclusion from the
Unicode token-splicing rule: HTML markup does not explain a bidi control
splitting an ASCII token. The new `spliced.html` fixture checks that this
suspicious content is detected inside an HTML root. No exclusions broaden.
Other source rules remain in place:

- `documentation-page-heading`
- `mkdocs-material-page`
- `docusaurus-docs-source`
- `webpack-docs-chunk-global`
- `readme-run-application-instruction`
- `static-documentation-html-page`
- `docusaurus-docs-bundle`
- `documentation-web-page`

The two new notable traits describe document content, without claiming server
communication, sed execution, or benign intent: a command-summary heading and
a 504 gateway-timeout heading. They do not use sample filenames or tool names.

## Focused controls

Run `python3 testdata/triage/html-document-metadata/check.py`.
Seven controls cover a renamed-tool command summary, timeout spelling variants,
an active script page with the same root markup, commented headings, prose
without headings, and a fragment with both heading claims but no initial root.
The root atom is checked through `test-rules`: the engine may strip unreferenced
baseline findings after matching. New content observations are checked in scan
output. Fixtures are copied away from the testdata directory so intentional
test-path exclusions cannot hide the Unicode control. Matcher/scope equality with the old root atom was independently checked.
Both supplied samples were rescanned with `atomscan --no-update --mode slow`;
only accurate metadata remains, with zero suspicious or hostile traits.

The full validator identified one score-only expectation affected by relocation:
`adobe-password-blob.html` scores 273 instead of 274. Its score floor follows
the new taxonomy; both required hostile traits and the existing hostile and
suspicious count floors remain unchanged. No detection requirement was removed.
