using System.IO;
class LocalOperations {
 const string revision = "664996a16fa9228cfd7a55d767deb31f62a65f51";
 string label = "Path";
 string paragraph = "\r\n\r\n";
 int Copy(Stream stream, byte[] buffer) { return stream.Read(buffer, 0, buffer.Length); }
 string[] List(string root) { return Directory.GetFiles(root); }
}
