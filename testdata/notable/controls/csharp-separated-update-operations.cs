// A documentation-style updater example lists a download helper and a process
// launch helper in separate methods. Their co-occurrence does not establish a
// staged-file activation chain.
using System.Diagnostics;
using System.Net;

class UpdaterReference {
    static void FetchUpdate(string url, string path) {
        new WebClient().DownloadFile(url, path);
    }
// Separation is intentionally greater than the local-chain window.
// update helper documentation
// update helper documentation
// update helper documentation
// update helper documentation
// update helper documentation
// update helper documentation
// update helper documentation
// update helper documentation
// update helper documentation
// update helper documentation
// update helper documentation
// update helper documentation
// update helper documentation
// update helper documentation
// update helper documentation
// update helper documentation
// update helper documentation
// update helper documentation
// update helper documentation
// update helper documentation
// update helper documentation
// update helper documentation
// update helper documentation
// update helper documentation
// update helper documentation
// update helper documentation
// update helper documentation
// update helper documentation
// update helper documentation
// update helper documentation
// update helper documentation
// update helper documentation
// update helper documentation
// update helper documentation
// update helper documentation
// update helper documentation
// update helper documentation
// update helper documentation
// update helper documentation
// update helper documentation
// update helper documentation
// update helper documentation
// update helper documentation
// update helper documentation
// update helper documentation
// update helper documentation
// update helper documentation
// update helper documentation
// update helper documentation
// update helper documentation
// update helper documentation
// update helper documentation
// update helper documentation
// update helper documentation
// update helper documentation
// update helper documentation
// update helper documentation
// update helper documentation
// update helper documentation
// update helper documentation
// update helper documentation
// update helper documentation
// update helper documentation
// update helper documentation
// update helper documentation
// update helper documentation
// update helper documentation
// update helper documentation
// update helper documentation
// update helper documentation
// update helper documentation
// update helper documentation
// update helper documentation
// update helper documentation
// update helper documentation
// update helper documentation
// update helper documentation
// update helper documentation
// update helper documentation
// update helper documentation
    static void LaunchUpdate(string path) {
        var temp = System.Environment.GetEnvironmentVariable("TEMP");
        Process.Start(new ProcessStartInfo(path) { UseShellExecute = false });
    }
}
