# Legacy process-name review

The `metadata/file/string/process-name` leaf contained names rather than evidence of process activity. Named iOS and Windows components, Smartmontools, Zabbix, Tomcat, JBoss and WebLogic now reside with their identities in `well-known/`. A name match alone still does not establish that the software runs or is targeted.

`qmgr` is ambiguous without further context, so it remains a neutral service-name reference. `updater.exe` is a generic filename reference; it and the adjacent updater-name observation now live together in the updater-path sibling. The original matchers, scopes, criticalities and consuming rules are preserved; five named binary observations have a one-byte minimum, which is implied by their nonempty matchers, and the legacy leaf has been removed.
