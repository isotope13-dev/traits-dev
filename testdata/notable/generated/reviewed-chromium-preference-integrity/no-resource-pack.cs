using System.IO;
using System.Security.Cryptography;
class PreferenceEditor {
    static byte[] Edit(string profile, byte[] key) {
        byte[] resource = File.ReadAllBytes("data.bin");
        string target = Path.Combine(profile, "Secure Preferences");
        string prefs = File.ReadAllText(target);
        string fields = "protection.macs super_mac";
        using (var mac = new HMACSHA256(key)) {
            File.WriteAllText(target, prefs);
            return mac.ComputeHash(resource);
        }
    }
}
