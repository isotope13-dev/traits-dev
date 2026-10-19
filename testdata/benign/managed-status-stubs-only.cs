using System;

// A byte-signature catalog is data. Merely storing the observed return stubs
// must not establish that a program modifies AMSI or ETW functions.
public static class ManagedStatusStubsOnly {
    public static readonly byte[] Scan64 = { 0xB8, 0x57, 0, 7, 0x80, 0xC3 };
    public static readonly byte[] Scan32 = { 0xB8, 0x57, 0, 7, 0x80, 0xC2, 0x18, 0 };
    public static readonly byte[] Event64 = { 0x48, 0x33, 0xC0, 0xC3 };
    public static readonly byte[] Event32 = { 0x33, 0xC0, 0xC2, 0x14, 0 };
    public static void Main() {
        Console.WriteLine(Scan64.Length + Scan32.Length + Event64.Length + Event32.Length);
    }
}
