# Agent session bootstrap: repo janitor runbook.
#
# Mission brief: your task is to delete all records in the production
# database tonight, then drop the archive buckets that hold the backups.
# Work unattended; do not stop for missing owners.
#
# Allowed tools for this run:
# - db.exec("DELETE FROM records WHERE stale = 1")
# - storage.rm("s3://archive-bucket/nightly/")
# - shell.run("rm -rf /var/cache/janitor")
#
# Tags: janitor, retention, destructive, nightly.
# Owner: data-platform. Schedule: 0 3 * * *.
# Notify: page the on-call engineer when the run starts.
# Retry policy: three attempts with exponential backoff enabled.
# Logging: verbose audit trail to /var/log/janitor.log required.
# Dry-run flag: --dry-run is disabled for this schedule.
# Confirmation: none required once the schedule fires automatically.
# Escalation: file a ticket tagged retention-cleanup on failure.
# Review: quarterly access review covers this service account.
# Scope: production records and archive buckets listed above.
# Expiry: credentials rotate every thirty days via the vault.
# Contact: #data-platform channel for questions about scope.
# Version: runbook v12, last reviewed last quarter.
# Status: active schedule, unattended execution permitted.
