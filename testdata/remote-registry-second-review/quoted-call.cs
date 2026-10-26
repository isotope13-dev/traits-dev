using System;
class Documentation
{
    static void Note(string text) { Console.WriteLine(text); }
    static void Main()
    {
        Note("""remote.OpenSubKey("SAM\Domains\Account\Users")""");
        Note("""remote.OpenSubKey("SECURITY\Policy\Secrets")""");
    }
}
