var shell = new ActiveXObject("Shell.Application");
var folder = shell.Namespace(0);
folder.CopyHere("archive.zip");
