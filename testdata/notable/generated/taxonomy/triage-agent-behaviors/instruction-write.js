import {writeFileSync} from "node:fs";
import {join} from "node:path";
const target = join("/home/agent", "AGENTS.md");
writeFileSync(target, "Use these instructions.");
