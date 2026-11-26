const f = { $nin: [1, 2] }; const q = { status: { $nin: ["x"] } };
await fetch("https://api.example.net/v1/q", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(f) });
