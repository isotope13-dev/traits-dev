using Microsoft.Win32;
using System;
using System.Diagnostics;
using System.IO;
using System.Reflection;

namespace DotNetInjection
{
    internal class Program
    {
        static string GetVirtualBoxInstallDir()
        {
            using (RegistryKey key = Registry.LocalMachine.OpenSubKey(@"Software\Oracle\VirtualBox"))
            {
                if (key == null)
                {
                    throw new InvalidOperationException("VirtualBox Not Installed?");
                }
                return key.GetValue("InstallDir") as string ?? throw new InvalidOperationException("Couldn't read install dir.");
            }
        }

        static Guid FindVirtualBoxClientClsid()
        {
            using (RegistryKey key = Registry.LocalMachine.OpenSubKey(@"Software\Classes\CLSID"))
            {
                foreach (var name in key.GetSubKeyNames())
                {
                    if (Guid.TryParse(name, out Guid clsid))
                    {
                        using (RegistryKey subkey = key.OpenSubKey(name))
                        {
                            if (subkey is null)
                            {
                                continue;
                            }
                            string class_name = subkey.GetValue(null) as string;
                            if (class_name == "VirtualBoxClient Class")
                            {
                                return clsid;
                            }
                        }
                    }
                }
            }
            throw new InvalidOperationException("Didn't find VirtualBox client class.");
        }

        static string GetClassKeyPath(Guid clsid)
        {
            return $@"Software\Classes\CLSID\{clsid:B}";
        }

        static string GetKeyPath()
        {
            return GetClassKeyPath(typeof(ComClass).GUID);
        }

        static void RegisterClass()
        {
            using (RegistryKey base_key = Registry.CurrentUser.CreateSubKey(GetKeyPath()))
            {
                using (RegistryKey inproc_key = base_key.CreateSubKey("InProcServer32"))
                {
                    Type type = typeof(ComClass);
                    Assembly asm = type.Assembly;
                    inproc_key.SetValue(null, "mscoree.dll");
                    inproc_key.SetValue("Class", type.FullName);
                    inproc_key.SetValue("Assembly", asm.FullName);
                    inproc_key.SetValue("RuntimeVersion", "v4.0.30319");
                    inproc_key.SetValue("CodeBase", asm.CodeBase);
                }
            }
        }

        static void DeleteKeys(Guid clsid)
        {
            Registry.CurrentUser.DeleteSubKeyTree(GetClassKeyPath(clsid), false);
            Registry.CurrentUser.DeleteSubKeyTree(GetKeyPath(), false);
        }

        static void RegisterTreatAs(Guid clsid)
        {
            using (RegistryKey base_key = Registry.CurrentUser.CreateSubKey(GetClassKeyPath(clsid)))
            {
                using (RegistryKey inproc_key = base_key.CreateSubKey("LocalSettings"))
                {
                    inproc_key.SetValue(null, typeof(ComClass).GUID.ToString("B"));
                }
            }
        }

        static void Main(string[] args)
        {
            try
            {
                if (args.Length < 1)
                {
                    throw new Exception("Please specify the name of the VM to load.");
                }
                Guid clsid = FindVirtualBoxClientClsid();
                string install_dir = GetVirtualBoxInstallDir();
                Console.WriteLine("[INFO] VirtualBoxClient CLSID: {0}", clsid);
                Console.WriteLine("[INFO] VirtualBox Install Dir: {0}", install_dir);
                try
                {
                    RegisterClass();
                    RegisterTreatAs(clsid);
                    ProcessStartInfo start_info = new ProcessStartInfo(Path.Combine(install_dir, "VBoxHeadless.exe"), $"--startvm {args[0]}")
                    {
                        UseShellExecute = false
                    };
                    using (var process = Process.Start(start_info))
                    {
                        if (!process.WaitForExit(10000))
                        {
                            throw new Exception("Process exit timed out.");
                        }
                    }
                }
                finally
                {
                    DeleteKeys(clsid);
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine("[ERROR] {0}", ex.Message);
            }
        }
    }
}
