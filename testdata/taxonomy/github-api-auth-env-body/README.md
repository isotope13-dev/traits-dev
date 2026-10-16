# GitHub API auth vs credential-body exfiltration controls

A GitHub Action (modeled on agilepathway/label-checker) sends its workflow
token as an `Authorization` header to `api.github.com` while the request
body carries only repository coordinates. The engine's file-level flow
candidates fire on the co-occurrence, but no credential enters the body, so
`credential-environment-http-body` must stay silent. Serializing the token
itself into a body sent to a third-party collector still convicts.

`cases.json` and `check.py` exercise both cases against ordinary Cleave
JSON analysis.

Run with:

```sh
python3 testdata/taxonomy/github-api-auth-env-body/check.py --cleave cleave
```
