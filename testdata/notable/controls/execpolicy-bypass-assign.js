const { execFile } = require("child_process");
const policy = { executionPolicy: "bypass", windowStyle: "hidden" };
execFile("powershell.exe", ["-ExecutionPolicy", policy.executionPolicy, "-WindowStyle", policy.windowStyle, "-File", "C:\\Users\\Public\\run.ps1"]);
