// Local dev server for the settings page.
const r = await fetch("http://127.0.0.1:1997/api/status", { method: "GET" });
console.log(await r.json());
