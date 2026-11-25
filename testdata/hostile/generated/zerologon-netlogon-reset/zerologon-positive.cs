// Positive C# Zerologon pattern
using System.Runtime.InteropServices;
class ZerologonExploit {
    enum NETLOGON_SECURE_CHANNEL_TYPE { WorkstationSecureChannel = 2 }
    [DllImport("logoncli.dll")] static extern int I_NetServerReqChallenge();
    [DllImport("logoncli.dll")] static extern int I_NetServerAuthenticate3();
    [DllImport("logoncli.dll")] static extern int I_NetServerPasswordSet2();
}
