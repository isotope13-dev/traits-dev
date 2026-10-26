import {readFileSync,writeFileSync} from "node:fs";
const data=readFileSync("AGENTS.md","utf8");
writeFileSync("settings.json",data);
