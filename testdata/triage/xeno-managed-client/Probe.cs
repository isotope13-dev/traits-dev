// Static analysis fixture only. Compiled as a library and never executed.
using System;
using System.Diagnostics;
using System.IO;
using System.Net.Sockets;
using System.Reflection;
using System.Runtime.InteropServices;
using System.Security.Cryptography;
using System.Text;
using Microsoft.Win32;

public static class Probe
{
#if !NO_NETWORK
    public static void Network(Socket socket, SocketAsyncEventArgs args)
    {
        socket.ConnectAsync(args);
        socket.ReceiveAsync(args);
    }
#endif
#if !NO_REFLECTION
    public static object Reflect(byte[] bytes, string typeName, string methodName)
    {
        Assembly assembly = Assembly.Load(bytes);
        object instance = Activator.CreateInstance(assembly.GetType(typeName));
        return instance.GetType().GetMethod(methodName).Invoke(instance, null);
    }
#endif
#if !NO_WINDOW
    [DllImport("user32.dll")]
    public static extern IntPtr GetForegroundWindow();
    [DllImport("user32.dll")]
    public static extern int GetWindowText(IntPtr handle, StringBuilder title, int size);
#endif
#if !NO_IDLE
    [DllImport("user32.dll")]
    public static extern bool GetLastInputInfo(IntPtr info);
#endif
#if !NO_HIDDEN
    public static void Hidden(string file)
    {
        Process.Start(new ProcessStartInfo { FileName = file, CreateNoWindow = true, UseShellExecute = false });
    }
#endif
#if !NO_REMOVAL
    public static string RemovalPrefix()
    {
        return Encoding.UTF8.GetString(Convert.FromBase64String("L0MgY2hvaWNlIC9DIFkgL04gL0QgWSAvVCAzICYgRGVsICI="));
    }
#endif
#if TASK
    public static void StartupTask(string xmlPath)
    {
        File.WriteAllText(xmlPath, "<Task><Triggers><LogonTrigger><Enabled>true</Enabled></LogonTrigger></Triggers><Principals><Principal><RunLevel>HighestAvailable</RunLevel></Principal></Principals></Task>");
        Process.Start(new ProcessStartInfo { FileName = "schtasks.exe", Arguments = "/Create /TN \"Example\" /XML \"" + xmlPath + "\" /F", CreateNoWindow = true, UseShellExecute = false });
    }
#endif
#if RUNKEY
    public static void StartupKey(string name, string path)
    {
        using (RegistryKey key = Registry.CurrentUser.OpenSubKey("SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run", true))
            key.SetValue(name, path);
    }
#endif
#if AES
    public static void Transform(byte[] key, byte[] iv)
    {
        using (Aes aes = Aes.Create())
        {
            using (ICryptoTransform encrypt = aes.CreateEncryptor(key, iv))
            using (ICryptoTransform decrypt = aes.CreateDecryptor(key, iv))
            using (CryptoStream stream = new CryptoStream(new MemoryStream(), encrypt, CryptoStreamMode.Write))
                stream.FlushFinalBlock();
        }
    }
#endif
#if COMPRESS
    [DllImport("ntdll.dll")]
    public static extern uint RtlCompressBuffer(ushort format, byte[] source, uint size, byte[] output, uint capacity, uint chunk, out uint finalSize, IntPtr workspace);
#endif
}
