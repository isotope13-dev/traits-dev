Vendor release-policy verbs must not read as concealment
=====================================================

`repository-agent-no-review` matched `retired without notice` in a benign
AI-provider plugin's API changelog comment ("Free slugs are retired without
notice"), completing the `repository-content-agent-prompt-injection`
composite on first-party agent code. Release-policy verbs (`retire`,
`deprecate`) belong to the same documented exclusion class as
change/remove/update; only action verbs like `edit` still match.

Run `python3 testdata/no-review-policy-verbs/check.py <scratch-directory>`.
`negative-policy.md` (vendor disclaimer) must not report the
`repository-content-agent-prompt-injection` composite;
`positive-directive.md` (addressed, imperative, unreviewed agent action)
must still report it. The check asserts the composite rather than the bare
`repository-agent-no-review` atom because unreferenced component atoms are
filtered from scan output.
