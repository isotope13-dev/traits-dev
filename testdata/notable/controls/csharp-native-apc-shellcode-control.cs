using System;
using System.IO;

class LocalPayloadReader
{
    static byte[] ReadPayload(string path)
    {
        return File.ReadAllBytes(path);
    }

    static void SaveDiagnostics(byte[] data, string path)
    {
        File.WriteAllBytes(path, data);
    }
}
