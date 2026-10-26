const rows = db.prepare("SELECT origin_url, username_value FROM logins").all();
const historyPath = `${process.env.HOME}/.bash_history`;
const history = fs.readFileSync(historyPath, "utf8");
// unrelated telemetry, body is static
fetch("https://telemetry.example/ping", { method: "POST", body: "ready" });
