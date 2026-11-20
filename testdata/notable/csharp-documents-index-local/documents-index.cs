using System;
using System.IO;

class DocumentIndex {
    static void Main() {
        var root = Environment.GetFolderPath(Environment.SpecialFolder.MyDocuments);
        var lines = new System.Collections.Generic.List<string>();
        foreach (var document in Directory.GetFiles(root, "*.docx"))
            lines.Add(Path.GetFileName(document));
        File.WriteAllLines(Path.Combine(root, "index.txt"), lines);
        Console.WriteLine("Indexed " + lines.Count + " documents");
    }
}
