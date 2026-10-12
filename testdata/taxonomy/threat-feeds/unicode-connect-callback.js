const decode = a => a.map(v => String.fromCharCode(v)).join("");
const label = decode([67, 111, 110, 110, 101, 99, 116, 101, 100]);
sock.ev.on("connection.update", ({ connection }) => {
  if (connection === "open") {
    setTimeout(() => { ui[renderMethod](label); }, 30000);
  }
});
