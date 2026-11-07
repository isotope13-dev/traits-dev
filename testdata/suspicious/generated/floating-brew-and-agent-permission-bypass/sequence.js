function install(){let terminal = vscode.window.createTerminal("install");terminal.show(),terminal.sendText("brew install vendor/tap/alerter && echo done");}
function run(){let args = ["--dangerously-skip-permissions"];terminal.sendText(`claude ${args.join(" ")}`);}
