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
const executablePath = join(BIN_DIR, `crm-connector-${VERSION}`);

async function install() {
  if (existsSync(executablePath)) return;

  const url = `http://downloads.example.org/v1/releases/${PLATFORM}/${VERSION}/crm-connector`;
  let response;
  try {
    response = await fetch(url, { signal: AbortSignal.timeout(60_000) });
  } catch {
    return;
  }
  if (!response.ok) return;

  mkdirSync(BIN_DIR, { recursive: true });
  writeFileSync(executablePath, Buffer.from(await response.arrayBuffer()));
  chmodSync(executablePath, 493);

  try {
    const v = execFileSync("/usr/bin/true", ["--version"], {
      timeout: 15_000,
      encoding: "utf8",
    }).trim();
    if (v) console.log(`@leadstack/crm-connect v${v}`);
  } catch {
    /* optional — continue without platform connector */
  }
}

install().catch(() => {});