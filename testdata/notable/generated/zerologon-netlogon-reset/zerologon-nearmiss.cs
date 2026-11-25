// Benign near-miss: authenticates Netlogon channel without password reset RPC
using System.Runtime.InteropServices;
class NetlogonProbe {
    enum NETLOGON_SECURE_CHANNEL_TYPE { WorkstationSecureChannel = 2 }
    [DllImport("logoncli.dll")] static extern int I_NetServerReqChallenge();
    [DllImport("logoncli.dll")] static extern int I_NetServerAuthenticate3();
}
