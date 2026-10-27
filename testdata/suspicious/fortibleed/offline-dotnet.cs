using System;
using System.Text;
using System.Security.Cryptography;
using System.Text.RegularExpressions;
class Recovery {
    static byte[] Recover(string config) {
        var m = Regex.Match(config, @"set (?:password|passwd) ENC (\S+)");
        var raw = Convert.FromBase64String(m.Groups[1].Value);
        var iv = new byte[16];
        Array.Copy(raw, iv, 4);
        using (var aes = Aes.Create()) {
            aes.Key = Encoding.ASCII.GetBytes("Mary had a littl");
            aes.IV = iv;
            aes.Mode = CipherMode.CBC;
            aes.Padding = PaddingMode.None;
            return aes.CreateDecryptor().TransformFinalBlock(raw, 4, raw.Length - 4);
        }
    }
}
