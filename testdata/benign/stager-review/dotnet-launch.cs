using System.Diagnostics;
class Example {
    static void Main() {
        var info = new ProcessStartInfo("utility");
        info.ArgumentList.Add("--version");
        Process.Start(info).WaitForExit();
    }
}
