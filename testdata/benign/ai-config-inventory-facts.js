// Configuration location and model discovery are neutral capabilities.
const directory = process.env["CLAUDE_CONFIG_DIR"];
const gateway = "https://gateway.example";
fetch(`${gateway}/v1/models`, { method: "GET" });
