const artifact = Uri.joinPath(Uri.file(tempDirectory), "payload.vsix");
await commands.executeCommand("workbench.extensions.installExtension", artifact);
