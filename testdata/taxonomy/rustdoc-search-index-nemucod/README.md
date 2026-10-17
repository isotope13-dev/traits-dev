# Rustdoc search index vs Nemucod numeric encoding controls

Rustdoc's generated `search-index.js` (new `JSON.parse` format) stores
item-kind codes in long numeric arrays such as `"t":[13,13,...]`. Those
runs resemble Nemucod concatenated char-code encoding but are generated
documentation data with no decoder, so the Nemucod trait must stay silent.
A concatenated char-code string decoded via `String.fromCharCode` still
convicts.

`cases.json` and `check.py` exercise both cases against ordinary Cleave
JSON analysis. The search-index fixture is a trimmed excerpt of a real
rustdoc output (deltae 0.3.0).

Run with:

```sh
python3 testdata/taxonomy/rustdoc-search-index-nemucod/check.py --cleave cleave
```
