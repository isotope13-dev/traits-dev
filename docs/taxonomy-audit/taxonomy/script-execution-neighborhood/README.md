# Script execution neighborhood review

Seven MSBuild identifiers were renamed to match their observations: a
WebClient context, APC and memory-write references, a shellcode project
invocation, XML API references, a FreeSWITCH-cache-or-7-Zip name, and
shellcode-template text. Their conditions and severities are unchanged. The
three FTP-banner consumers were checked for the renamed alternatives.

Eleven legacy script-evaluation rules moved to interpreter-input execution,
remote-command dispatch, scheduled-task persistence, network code evaluation,
file execution, and supporting facts. WMI process creation now has a shared
mechanism directory for the existing JavaScript rule and the moved VBScript
rule. Consumers that previously selected the broader `create/exec` directory
retain the JavaScript WMI rule explicitly. The VBScript WMI call is now also
visible to positive selectors for the broader process-creation category;
selectors for shell creation do not gain the merely textual hidden-PowerShell
profile. The FTP interpreter-input directory selectors cover the moved Mach-O
rules, but those FTP composites apply to script types, not Mach-O files.

Twenty-two generic source, URL and evaluation observations also moved out of
the remote-code leaf, reducing it from 82 to 60 rules. The conditions and
non-technique defaults of all 82 original rules were compared, and both legacy
ancestor consumers retain the 22 moved alternatives; each uses the URL-construction
directory only because its five current members are exactly the former
alternatives. Review those consumers before adding members. A contract-resolved
browser loader moved from network to the existing blockchain source category.
The network evaluator leaf has 68 rules; blockchain has eight. No cap changed.
