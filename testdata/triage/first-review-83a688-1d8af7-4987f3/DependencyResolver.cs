using System;
using System.IO;
using System.Reflection;

// Compile as an unsigned library with a 128 KiB deterministic random resource.
// This ordinary dependency resolver satisfies the removed hostile loader rule.
public static class DependencyResolver
{
    public static Assembly Resolve(object sender, ResolveEventArgs args)
    {
        string name = new AssemblyName(args.Name).Name + ".dll";
        using (Stream resource = Assembly.GetExecutingAssembly().GetManifestResourceStream(name))
        {
            byte[] bytes = new byte[resource.Length];
            resource.Read(bytes, 0, bytes.Length);
            return Assembly.Load(bytes);
        }
    }

    public static void Setup()
    {
        AppDomain.CurrentDomain.AssemblyResolve += Resolve;
        Console.WriteLine(MethodBase.GetCurrentMethod());
        foreach (MethodInfo method in typeof(DependencyResolver).GetMethods())
            Console.WriteLine(method.Name);
    }
}
