import os from "node:os";
import path from "node:path";
import { writeFileSync } from "node:fs";

const LABEL = "example.docs.preview";

// Writes a launchd plist for a documentation preview server the user starts
// by hand. Nothing here enables or starts the agent.
export function writePreviewPlist(binary) {
  const plist = `<plist version="1.0"><dict>
  <key>Label</key><string>${LABEL}</string>
  <key>ProgramArguments</key><array><string>${binary}</string></array>
  <key>RunAtLoad</key><true/>
</dict></plist>`;
  writeFileSync(path.join(os.homedir(), "Library", "LaunchAgents", `${LABEL}.plist`), plist);
}
