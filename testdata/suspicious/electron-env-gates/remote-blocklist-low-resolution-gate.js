// Suspicious-only control: environment-gated silent exit with no payload,
// no archive, and no hardcoded-IP beacon. Exercises the low-resolution quit
// gate and the remote blocklist gate below hostile severity.
const os = require('os');

async function environmentAllowed() {
  const res = await fetch('https://api.seeip.org/jsonip');
  const info = await res.json();
  const currentIp = info.ip;
  const hostName = os.hostname();
  const [denyListIps, denyListHosts] = await Promise.all([
    fetch('https://gate.example.com/ip').then(r => r.json()),
    fetch('https://gate.example.com/pc').then(r => r.json())
  ]);
  if (denyListIps.includes(currentIp) || denyListHosts.includes(hostName)) {
    return false;
  }
  return true;
}

async function boot() {
  const { screen, app } = require('electron');
  if (!(await environmentAllowed())) {
    app.quit();
    return;
  }
  const { width, height } = screen.getPrimaryDisplay().size;
  if (width < 1280 || height < 720) {
    app.quit();
    return;
  }
  console.log('display ok for', os.hostname());
}

boot();
