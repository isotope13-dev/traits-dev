using System;
using System.IO;
public static class Maintenance {
    public static void RemoveTraces() {
        File.Delete(Environment.ExpandEnvironmentVariables(@"%LOCALAPPDATA%\Microsoft\CLR_v4.0\UsageLogs\PatchMyPC-ScriptRunner.exe.log"));
        string folder = Environment.ExpandEnvironmentVariables(@"%WINDIR%\Prefetch");
        foreach (string trace in Directory.GetFiles(folder, "PATCHMYPC-SCRIPTRUNNER.EXE-*.pf")) File.Delete(trace);
    }

}
