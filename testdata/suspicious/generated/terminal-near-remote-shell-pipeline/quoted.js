const command = "curl -LsS https://example.com/install.sh | sh";
api.sendCommandToTerminal(command, "Install");
execute(`conda env create --file "${file.fileName}"`);
