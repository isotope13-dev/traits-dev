const rows = db.prepare("SELECT origin_url, username_value FROM logins").all();
const historyPath = `${process.env.HOME}/.bash_history`;
const history = fs.readFileSync(historyPath, "utf8");
console.log(rows.length, history.length);
