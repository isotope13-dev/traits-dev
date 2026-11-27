const terminal = vscode.window.createTerminal({ name: "Build" });
terminal.show();
terminal.sendText("cargo build");
