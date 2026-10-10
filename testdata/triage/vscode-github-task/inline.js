const api = require("vscode");
const task = new api.Task({}, 1, "setup", "tools", new api.ShellExecution("npx -y github:example/alternate"));
api.tasks.executeTask(task);
