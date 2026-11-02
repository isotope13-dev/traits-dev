// Benign control: installer registers its own declared package.
// Never executed; structural control only.
import { promises as fs } from 'node:fs';
import { homedir } from 'node:os';
import { join } from 'node:path';
const PACKAGE_NAME = '@example/helper-mcp';
export async function runInit() {
  const cfgPath = join(homedir(), '.config', 'Claude', 'claude_desktop_config.json');
  const cfg = { mcpServers: {} };
  cfg.mcpServers['helper'] = {
    command: 'npx',
    args: ['-y', PACKAGE_NAME],
    env: {},
  };
  await fs.writeFile(cfgPath, JSON.stringify(cfg, null, 2));
}
