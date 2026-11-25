const addr = await fetch("https://mail.example.test/api/addresses", { method: "POST" });
const mail = await fetch("https://mail.example.test/api/inbox/" + addr.id);
