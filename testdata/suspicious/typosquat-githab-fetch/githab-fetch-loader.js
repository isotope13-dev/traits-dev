// Install helper: fetches the CLI release notes from a lookalike host.
const res = await fetch("https://githab.com/acme/cli/releases/latest/notes.json");
console.log(await res.text());
