// Test harness: the Codex CLI is launched against a loopback mock provider
// through launch overrides; the files written are unrelated fixture config.
import { writeFileSync, mkdirSync } from "node:fs";
import { join } from "node:path";
const home = join(process.cwd(), "tmp", "codex-home");
mkdirSync(join(home, ".codex"), { recursive: true });
writeFileSync(join(home, ".codex", "config.toml"), '[projects."/work"]\ntrust_level = "trusted"\n');
export const overrides = [
  'model_provider="mock"',
  `model_providers.mock={name="mock",base_url="http://127.0.0.1:${process.env.MOCK_PORT}/v1",wire_api="responses"}`,
];
