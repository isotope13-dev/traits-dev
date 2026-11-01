# ClickFix remote-command review

The former remote-command leaf mixed delivery lures, execution, persistence and generic fragments. Its rules now live by their supported subjects:

- WebClient/archive and Node/archive launch evidence is grouped with network acquisition and process launch; the descriptions no longer assert a ZIP or executable filename that the conditions do not require.
- Reconstructed Rundll32/WebDAV execution and browser clipboard delivery live with those behaviors. A headless conhost, WebDAV path and DLL export argument are recorded as a combined profile because no Rundll32 invocation is required by that rule.
- The Node Run-key/script-host command remains a persistence finding; its Run-key and script-host supporting evidence is a registry profile.
- URL paths, command arguments, task XML references, credential-manager commands, archive flags and verification comments live with those observations. Combinations of remote task XML and DLL exports, or cmdkey and Regsvr32 references, do not by themselves establish task creation or a complete UNC execution chain.

The UNC XML option pattern was corrected to match an actual UNC path; it had an erroneous literal-pipe expression. The task-option matcher still recognizes either `/xml` or `/tn`, so its descriptions state an option reference rather than asserting task creation. The remote-command legacy leaf is removed; other ClickFix branches remain.

Network-related process combinations use a separate process network profile sibling, keeping the existing process-launch profile directory below the review target.
