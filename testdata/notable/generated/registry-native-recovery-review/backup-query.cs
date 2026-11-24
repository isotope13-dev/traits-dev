using System.Diagnostics;
class Backup { static void Query() {
var args = new[] { "wbadmin", "GET", "VERSIONS", "-quiet" };
Process.Start(new ProcessStartInfo(args[0], string.Join(" ", args[1..])));
}}
