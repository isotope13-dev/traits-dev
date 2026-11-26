// Project initializer: creates a restrictive Codex config and only warns when an
// existing one grants full access. Nothing here sets the sandbox to full access.
import fs from 'fs-extra';
import path from 'path';

export async function initCodexConfig(projectPath) {
  const warnings = [];
  const localConfigPath = path.join(projectPath, '.codex', 'config.toml');
  if (await fs.pathExists(localConfigPath)) {
    const existing = await fs.readFile(localConfigPath, 'utf-8').catch(() => '');
    if (/sandbox_mode\s*=\s*"danger-full-access"/.test(existing)) {
      warnings.push(
        '.codex/config.toml uses sandbox_mode = "danger-full-access": Codex can write anywhere. ' +
          'Edit it to "workspace-write" to tighten it.',
      );
    }
  } else {
    await fs.writeFile(localConfigPath, 'sandbox_mode = "workspace-write"\napproval_policy = "on-request"\n', 'utf-8');
  }
  return warnings;
}
