const command = "echo ready";
JSON.stringify({ command: "echo first" });
JSON.stringify({ "command": "echo second" });
JSON.stringify({ command });
// A command key is ordinary serialization, without any tasking endpoint.
