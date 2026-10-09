# Benign package triage

All three supplied SHA-256 digests agree with the archive bytes. The archive
members are ordinary files/directories with no traversal, links or native code.

- `e3b78aed248f`: @types/jest-specific-snapshot 0.5.10. Only declarations,
  package metadata and documentation; no runtime or lifecycle scripts. No change.
- `d163460624d9`: @tamagui/feather-icons 1.0.1-beta.193. React SVG component
  functions, theme wrapping and generated export barrels. All 577 source-map
  entries agree with shipped source; the 286 icon components have one render
  body each. Chrome, Slack, Clipboard and users are glyph/export names.
- `c7c7e4584abf`: @ai-sdk/alibaba 2.0.41. DashScope provider sending caller
  prompts, embedding text and video inputs. API-key loading supplies Bearer
  authentication, while Base64 helpers serialize caller-provided images. Tool
  calls are parsed and returned, without local command execution. All 14
  source-map entries agree with source. The analyzer reports limited flow
  graphs, so requests, response handling and exports were reviewed directly.

## Dispositions and consumer review

- Move `http/services/deepseek::deepseek-reasoning-content-field` to
  `data/llm/reasoning::reasoning-content-field` with unchanged matcher and
  explicit original file/platform scope. The field is shared with Qwen;
  remove the unsupported HTTP mapping. DeepSeek's composite retains its host
  requirement and references the new ID. No other exact-ID consumers exist.
- Remove `openclaw-ecosystem-phrase`: a general npx skills command establishes
  no OpenClaw identity. Remove its now-redundant grouping composite and have
  the two consumers reference the discriminating product-name atom.
- Remove the Chrome basename atom and its downgrade legs. Arbitrary filenames
  do not identify a browser or support discovery, and must not silence browser
  targeting. The other existing downgrade evidence is unchanged.
- Restrict Chrome and Slack name observations to avoid component display
  names; Slack uses literal evidence rather than export identifiers.
- Replace script clipboard substrings with actual member facts, preserving
  the binary/class text-reference alternative through a named neutral group.
  Update every exact consumer. The only parent-directory consumer is a
  CrystalX `unless`, so the group cannot double-count a conviction threshold.
- Remove Nodeunit's generic CommonJS export atom; its assertion composite
  references the existing module-export observation. This also excludes
  generated `0 && (module.exports = {...})` annotations.
- CLI usage and thinking-mode wording require literal evidence; schema code
  and comments are insufficient. Root-relative users paths must be literals,
  excluding local module imports such as `./icons/users`.
- Extend the existing HTTP POST call atom with postJsonToApi, preserving its
  old alternative. Add notable GET and Base64 helper-call observations in
  existing operation leaves; comments, strings and imports alone do not match.

Controls are recorded in testdata/taxonomy/benign-package-triage/cases.json.
Run each fixture with cleave test-rules and its matched/not_matched ID lists.
The positive controls retain real calls, clipboard members, help literals and
product names; negative controls exercise icons, source comments and an
unrelated skills command. No hostile or suspicious traits are added.
The Chrome-name observation is deliberately absent in the repository's
positive fixture because the existing test-directory exclusion applies. Its
ordinary-source positive and display-name negative were checked separately
outside testdata, alongside the same capability controls.
