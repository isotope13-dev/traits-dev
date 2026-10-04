using System;
using System.Runtime.InteropServices;
class Bytes { public static void Copy(byte[] source, IntPtr target) { Marshal.Copy(source, 0, target, source.Length); } }
