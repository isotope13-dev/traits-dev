function install(){const terminal = vscode.window.createTerminal("install"); terminal.show(); terminal.sendText("brew install vendor/tap/alerter && echo done");}
function run(){const args = ["--dangerously-skip-permissions"];terminal.sendText(`claude ${args.join(" ")}`);}
