const editor = require("vscode");
const command = `npx --yes github:example/renamed-project#${revision}`;
const task = new editor.Task({}, editor.TaskScope.Workspace, "setup", "tools", new editor.ShellExecution(command));

if (context.globalState.get("installed-revision") !== revision) { showWelcome(); }
