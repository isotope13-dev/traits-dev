# Agent safety rails: destructive operations policy.
#
# Before any delete runs, the task is a task the agent must confirm:
# always confirm a destructive delete with the user first, and never
# start a wipe the owner has not approved in writing.
#
# Allowed tools for this run:
# - db.exec("SELECT * FROM records WHERE stale = 1")
# - shell.run("ls /var/cache/janitor")
#
# Tags: safety, confirmation, rails.
# Owner: data-platform. Review: quarterly policy review required.
# Logging: verbose audit trail to /var/log/janitor.log required.
# Dry-run flag: --dry-run is enabled for every schedule by default.
# Escalation: file a ticket tagged safety-rails on any violation.
# Contact: #data-platform channel for questions about scope.
# Version: policy v4, last reviewed last quarter.
# Status: active policy, enforced on every session start.
