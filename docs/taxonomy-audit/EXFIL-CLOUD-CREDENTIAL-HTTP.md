# AWS credential upload follows the source

`aws-shared-credentials-http-exfil` required evidence that AWS shared
credential contents enter an HTTP request body. Its source is specific, so it
belongs in `objectives/exfiltration/stealer/cloud/`; HTTP is only the channel.
The composite moved intact from `objectives/exfiltration/http/upload/python.yaml`
to `stealer/cloud/python-aws-credentials.yaml`. Its ID, matcher references,
scope, file type, criticality, confidence, and ATT&CK mapping are unchanged.
The one supply-chain consumer now references the canonical cloud-source ID.

The PyPI consumer now declares `tar`, `whl`, and `pyproject.toml` among its
eligible outer/member types. A focused test showed the old type list rejected
a `.tar.gz` package before evaluating its members. The test package still does
not match the full chain: its Python code uses `Path.read_text()`
and passes the result through `json=`, while the source atom currently requires
`open(...).read()` flowing into `data=` or a `Request` body. That is a separate
coverage gap; the taxonomy move does not claim to fix it or weaken the matcher.

The moved rule matches the hostile `kcli-controls/aws-upload.py` sample and
does not match the benign `aws-unrelated-body.py` control. Five hostile and
five benign fixture expectations now require or forbid the canonical cloud
source feature, respectively, instead of the former transport path. Full soft
validation and refreshed taxonomy counts are recorded in the current plan
snapshot.
