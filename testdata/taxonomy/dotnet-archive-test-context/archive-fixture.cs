// Unit-test fixture: an archive-distributed skill bundle built to verify
// digest handling is test content, not staged C2.
using System;

public static class ArchiveFixtures
{
    public static byte[] BuildZip()
    {
        byte[] archive = new byte[] { 0x50, 0x4B, 0x03, 0x04 };
        return System.Text.Encoding.UTF8.GetBytes(Convert.ToBase64String(archive));
    }
}
