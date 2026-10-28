GLib.file_set_contents(path, "[Unit]\nDescription=service\n[Service]\n" + "ExecStart=/usr/bin/curl https://example.invalid/health\n");
