Pipenv 11.10.4 release-diff triage
================================

Verdict: benign, ordinary compatibility fix; no supply-chain compromise.

The supplied SHA-256 b624be67e9e24063975bdf30f5386ce7d3c5ba938cb8cddc9bbbdecc488141f5
matches PyPI's pipenv-11.10.4-py3-none-any.whl metadata:
https://pypi.org/pypi/pipenv/11.10.4/json

Comparison control: pipenv-11.10.3-py3-none-any.whl, fetched from
https://files.pythonhosted.org/packages/ed/a3/6c51d36006a563798021f954fd10a9baeb9592f8dabbb162ff0595e309cf/pipenv-11.10.3-py3-none-any.whl

Only two shared members changed: __version__.py and _compat.py. The latter
imports sys and replaces six.PY2 with sys.version_info < (3, 5), choosing the
older tempfile._mkstemp_inner signature for Python 3.4 too. Five dist-info
members move to the new version directory; 1,020 shared members are identical.
Both CacheControl serializers, safety.zip and distlib/util.py are unchanged.

CacheControl writes cc=2 zlib-compressed JSON HTTP-response cache records,
including Base64 body/header values and Vary fields. Its legacy cc=1 reader
unpickles the original data directly. Its cc=2 reader decompresses data into
json.loads. Neither passes decompressed data into pickle.loads. Both return
HTTPResponse objects after checking Vary headers. safety.zip bundles the
vulnerability checker and dependencies; distlib/util.py supplies packaging,
archive and subprocess utilities. Neither gained code in this release.

The retired decompressed-config composite conflated adjacent methods. Its
hostile consumer additionally pooled unrelated archive findings and inferred
a caller-resolved config path without evidence. A project name plus ordinary
serialization/reflection also does not prove a compromised wheel. Remove
those unsupported objective classifications; preserve exact decompressor-to-
pickle argument flow as notable capabilities and caller-frame co-occurrence
as a notable leaf-scoped composite. No package identity suppressor is added.
The separate package rules requiring disguised config staging/bootstrap remain.

Controls in expectations.toml exercise zlib assignment flow, direct gzip flow,
independent cache formats, and caller-frame inspection with compressed pickle.
The latter is observable capability, not proof of attacker intent.
