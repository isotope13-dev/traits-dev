// Inert managed-resource fixture: prints the resource, never evaluates it.
using System;
using System.IO;
using System.Reflection;
public static class Carrier {
    public static void Main() {
        using (var stream = Assembly.GetExecutingAssembly().GetManifestResourceStream("controls.ps1"))
        using (var reader = new StreamReader(stream)) Console.WriteLine(reader.ReadToEnd());
    }
}
