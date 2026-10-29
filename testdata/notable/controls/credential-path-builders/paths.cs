using System;
using System.IO;

class ConfigLocations {
    static void Main() {
        Console.WriteLine(Path.Combine(".config", "gh", "hosts.yml"));
        Console.WriteLine(Path.Combine(".config", "gcloud"));
    }
}
