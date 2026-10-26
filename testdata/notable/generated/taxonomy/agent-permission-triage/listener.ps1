Add-Type -TypeDefinition @"
using System.Net;
using System.Net.Sockets;
public class Relay { public void Start(int port) { var s = new TcpListener(IPAddress.Any, port); s.Start(); } }
"@
