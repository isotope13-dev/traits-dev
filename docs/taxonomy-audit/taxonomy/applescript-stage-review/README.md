# AppleScript staging review

The last 42 rules in the legacy script-staging directory were reviewed and moved by their evidence and likely operation. Matching conditions, scopes, confidence values and references were preserved.

- Temporary script paths, URL strings, fragmented options, compilation text, helper names and calls are observations of those subjects. A URL or a helper name alone does not prove a download or its eventual use. `load script` by itself is not proof that a loaded object ran.
- Generic build, folder and username text no longer identifies a C2 module or establishes a file drop. Combinations with shell calls are suspicious shell-execution profiles; download, compilation and load references without invocation are suspicious module-loading profiles.
- Meeting-lure acquisition, curl-driven script execution, TCC-modification plus helper calls, and curl piped into a shell remain objectives. Their descriptions report the combined clues without attributing a family or requiring direct data-flow proof.
- Shell-related profiles were split from the crowded execution-API directory into `metadata/file/profile/shell-execution`, including its existing shell-selection/process-launch sibling. A focused HTTP-download profile groups URL and option combinations without claiming a completed fetch.

Unsupported technique metadata was removed when the reclassified evidence did not substantiate it. The former legacy script-staging directory has no YAML rules or live YAML references.
