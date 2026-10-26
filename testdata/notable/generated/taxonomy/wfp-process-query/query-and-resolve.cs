using System.Diagnostics;
static unsafe class Query {
    static void Resolve() {
        foreach (Process candidate in Process.GetProcesses()) {
            string path = candidate.MainModule.FileName;
            fixed (char* filename = path) {
                Windows.Win32.PInvoke.FwpmGetAppIdFromFileName0(filename, null);
            }
        }
    }
}
