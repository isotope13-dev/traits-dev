# MSBuild module-loader retirement

The final 22 rules in `dropper/module-load` moved to build configuration,
XML and source observations, compiler or module-loading behaviors, reflective
payload activation, MSBuild proxy execution, and process-injection objectives.
The legacy module-load namespace has no remaining YAML rules or live YAML
references.

An XML inline-task declaration with WebClient and either a download or process
reference remains a suspicious profile; it does not require both a download
and a launch. The MSBuild shellcode-template combination now reports
suspicious, since a template reference does not establish execution. An inline
task with APC and process-memory-write references remains an injection
objective without claiming the more specific early-bird sequence. Generic
build, source and API facts no longer inherit the MSBuild abuse technique.

The three FTP-banner consumers replace their legacy directory selector with
exactly its 22 former members. The broad hosts-file consumer keeps those
alternatives, using its existing process-injection selector for the one member
already covered. A rule-by-rule comparison verified the original match
conditions and other effective defaults. No directory cap was changed.
