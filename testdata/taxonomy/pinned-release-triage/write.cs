using System.IO;
class Exporter {
  static void Save(string path) {
    System.IO.File.WriteAllText(path, "export");
  }
}
