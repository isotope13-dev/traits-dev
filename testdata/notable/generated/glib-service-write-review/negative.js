// Service text in another call or an ignored third argument is not the write body.
GLib.file_set_contents(path, "status only");
print("[Service]\n" + "ExecStart=demo\n");
logger.file_set_contents(path, "[Service]\n" + "ExecStart=demo\n");
GLib.file_set_contents(path, "status only", "[Service]\n" + "ExecStart=demo\n");
GLib.file_set_contents(path, getHeader(), "ExecStart=demo\n");
