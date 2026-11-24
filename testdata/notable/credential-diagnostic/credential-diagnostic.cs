using System;
using System.IO;
class CredentialDiagnostic {
    static string Preview(string home) {
        var path = Path.Combine(home, ".aws/credentials");
        using var stream = File.OpenRead(path);
        var bytes = new byte[Math.Min(4096, (int)stream.Length)];
        stream.ReadExactly(bytes);
        return Convert.ToHexString(bytes);
    }
}
