# Security-tool triage controls

These files are scan inputs. Do not execute them. `expected.json` lists the
required and absent traits; the same files were also scanned from an isolated
scratch directory to avoid test-directory exclusions.

The live skill, Perl relay, bash relay, and executable SSTI string retain their
attack findings. The audit quotes a prohibited override; the Go generator
returns formatted payload text without executing it. The stdout helper retains
a notable observation of collecting subprocess output.

Placement corrections:

- Subprocess stdout assigned to a result field: C2 tasking to process stdio.
- JVM trust-all names and configuration: security bypass to TLS verification.
- Webshell panel labels: backdoor self-label to terminal UI terminology.
- Autostart configuration with an IPv4 URL: persistence to service configuration.

Consumer references were updated. Additional intent composites retain their
other required evidence. Full rescans of Agent Toolkit CLI 1.42.0, Judges
3.79.0, and CyberStrikeAI 1.7.6 yielded zero hostile or suspicious findings.
The fetched Meta Muse installer was separately scanned before and after.
