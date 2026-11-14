fetch("https://updates.example.invalid/status", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ version: "1.2.3", channel: "stable" })
});
