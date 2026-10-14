Diagnostic-upload pooling must spare nested helper actions
===============================================================

`gha-secret-diagnostic-upload` pools its legs across archive members, so a
monorepo with a composite helper action under `.github/actions/`, an
unrelated curl, a temp dotfile, and an upload elsewhere convicted a whole
repository of "Action uploads a hidden temporary diagnostic payload". The
composite now carries the same `nested-action-manifest-path` unless-guard
as its siblings: repo-internal helper actions are not the published action
the rule is about.

Run `python3 testdata/gha-diagnostic-upload-pooling/check.py
<scratch-directory>`. `published-action-positive.zip` (root composite
action exfiltrating to a hidden temp file) must report the hostile;
`nested-helper-negative.zip` (helper action plus unrelated QA upload
shapes) must report no hostile at all.
