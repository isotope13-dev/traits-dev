// shell:true appears only in the comment; the call passes shell:false.
// A comment never spawns a shell, so spawn::shell-true must stay silent.
import { spawn } from "node:child_process";
export function openUrl(url) {
    const cmd = process.platform === "darwin" ? "open" : "xdg-open";
    try {
        // Windows "start" is a shell builtin; needs shell:true and an empty title arg.
        const child = spawn(cmd, [url], { stdio: "ignore", detached: true, shell: false });
        child.on("error", () => {});
        child.unref();
    } catch {
        /* best-effort */
    }
}
