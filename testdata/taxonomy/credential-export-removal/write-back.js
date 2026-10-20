import fs from "node:fs";
const target = ".bashrc";
const content = fs.readFileSync(target, "utf8");
fs.writeFileSync(target, content.replace(/^export\s+SERVICE_API_KEY=.*$/gm, ""));
