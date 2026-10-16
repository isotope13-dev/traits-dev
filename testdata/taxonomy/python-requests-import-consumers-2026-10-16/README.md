# Python Requests import-consumer controls

This 25-specimen matrix checks the seven current `metadata/import/python/requests`
reference consumers and the Pastebin URL-to-fetch boundary. It retains their
source positives and import-only controls. Pastebin marker detection remains a
separate URL fact; fetch detection requires the URL to flow into argument 0 of
the same `requests.get` call.

The positive routes the URL through `FETCH_URL = STAGE_URL` and places 60
numbered comment lines before the call, so the fetch rule cannot depend on
`near_lines`. The matrix rejects URL-plus-import without a fetch, a GET to an
unrelated host, POST-only use, and imports without a Pastebin request. The
former weak `pastebin-fetch-capability` and unused `paste-service-raw-url`
composites are retired: module imports and broad client capabilities do not
establish a fetch, while the individual URL marker remains observable.

Run the matrix with:

```sh
python3 scripts/check-taxonomy-cases.py \
  --cleave ../cleave/target/release/cleave \
  --cases testdata/taxonomy/python-requests-import-consumers-2026-10-16/cases.json
```
