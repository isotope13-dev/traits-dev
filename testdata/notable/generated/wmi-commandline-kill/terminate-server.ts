import { execFile } from "child_process";
const cmd = "Get-WmiObject Win32_Process | ? { $_.CommandLine -like '*server.js*' } | % { $_.Terminate() }";
execFile("pwsh", ["-c", cmd]);
