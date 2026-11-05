const child = spawn("npm", ["install", "impit@latest", "--no-audit"]);
const flags = ["--disable-blink-features=AutomationControlled"];
chromium.launch({args: flags, ignoreDefaultArgs: ["--enable-automation"]});
