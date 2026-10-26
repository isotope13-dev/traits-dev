using System.Diagnostics;
Process.Start(new ProcessStartInfo("launchctl", $"load -w {path}") { UseShellExecute = false });
