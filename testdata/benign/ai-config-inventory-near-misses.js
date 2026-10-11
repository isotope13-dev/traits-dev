// process.env.CLAUDE_CONFIG_DIR and fetch('/v1/models') are documentation.
const message = "process.env.CLAUDE_CONFIG_DIR";
const unrelated = process.env.CLAUDE_CONFIG_DIRECTORY;
fetch("https://gateway.example/v1/models-extra");
fetch("https://gateway.example/v1/models/one");
send("https://gateway.example/v1/models");
fetch("https://gateway.example/log", { body: "/v1/models" });
