// Positive control: a real shell:true spawn option must still match
// spawn::shell-true after the tree-sitter tightening.
import { spawn } from "node:child_process";
export function runAudit(cwd) {
    const child = spawn("npm audit --json", { cwd, shell: true, stdio: ["ignore", "pipe", "pipe"] });
    return child;
}
