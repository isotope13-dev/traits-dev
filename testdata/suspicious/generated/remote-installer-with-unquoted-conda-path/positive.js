const command = "curl -LsS https://example.com/install.sh | sh";
api.sendCommandToTerminal(command, "Install");
execute(`conda env create --prefix ./${prefix} --file ${file.fileName} && conda activate ./${prefix}`);
