# ESM export trailer vs appended encoded payload controls

Bundlers and transpilers end ESM output with a single long
`export { ... }` line. In a wallet SDK bundle (modeled on
@dynamic-labs-wallet/core) that line is an identifier list, not an
encoded payload, so `appended-encoded-exec` must stay silent even though
the module legitimately encodes key material and uses dynamic execution
elsewhere. A long Base64 line appended after ordinary code and executed
via `eval(Buffer.from(...))` still convicts.

`cases.json` and `check.py` exercise both cases against ordinary Cleave
JSON analysis.

Run with:

```sh
python3 testdata/taxonomy/esm-export-trailer-appended/check.py --cleave cleave
```
