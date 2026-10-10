const editor = require("vscode");
const command = `npx --yes git+https://github.com/example/renamed-project#${revision}`;
const task = new editor.Task({}, editor.TaskScope.Workspace, "setup", "tools", new editor.ShellExecution(command));
editor.tasks.executeTask(task);
