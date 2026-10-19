using System;
using System.Diagnostics;
using System.IO;
using System.Security.AccessControl;
using Microsoft.Win32;

// No process launch or registry write: SetValue belongs to Array.
public static class ManagedNames
{
    public static void Configure(ProcessStartInfo child, RegistryKey registry, object[] values)
    {
        child.FileName = "viewer.exe";
        Array.Reverse(values);
        values.SetValue(registry.GetValue("Theme"), 0);
    }
    public static void ApplyAcl(DirectoryInfo directory, DirectorySecurity acl)
    {
        directory.SetAccessControl(acl);
    }
}
